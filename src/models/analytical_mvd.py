#@title Helper Methods

from utils.constants import *

########################## DATA HELPERS ##########################
## Return the IMU & BP data for a specific heartbeat
def get_vcg_data_for_hb(selectedFile, selectedHb, dfAll):
  # Get data for individual heartbeat
  selected_data = dfAll[(dfAll.file.str.contains(selectedFile)) &\
                                  (dfAll['heartbeat'] == selectedHb)]
  selected_data = selected_data.set_index('ts')
  # selected_data = selected_data.fillna(method='ffill').fillna(method='bfill')
  return selected_data


########################## MATH HELPERS ##########################
## Return the Double Integral of Signal (aka Vector)
from scipy import integrate
def displacement(vcg_sig):
  vcg_sig = vcg_sig - vcg_sig.mean()   # TODO : Remove 'accelerometer drift'?

  # Double Integral
  serX=vcg_sig.index.astype(int)/1e9
  vz = integrate.cumtrapz(y=vcg_sig,x=serX)-vcg_sig.mean()   ## TODO : is this the best approach?
  # serVzX=vz.index.astype(int)/1e9
  dz = integrate.cumtrapz(y=vz-vz.mean(), x=serX[1:])
  return dz, vz


## Calculate RMS Envelope -- TODO : use timestamp for pd.rolling instead of np.convolve
def window_rms(a, window_size):
  a2 = np.power(a,2)
  window = np.ones(window_size)/float(window_size)
  return np.sqrt(np.convolve(a2, window, 'valid'))


########################## Plugin HELPERS ##########################
## Plugin function to allow 'ingecting' code snippets during execution
def plugin(name, pluginFns, localDict):
  fns = pluginFns.get(name, [])
  fns = [fns] if isinstance(fns, str) else fns
  [
      exec(fn['fn'], globals(), {**localDict, **fn['context']}) if isinstance(fn, dict)
      else exec(fn, globals(), localDict) 
      for fn in fns]

## Take snapshots of important data while executing..
def DataLog():
  db = {}
  def save(name, data):
    if name not in db : db[name] = []
    db[name].append(data)
  return db, save



#@title Implement Physical-Mathematical Model
## Input : Data-VCG for single heartbeat. Output : Calculated BP
def calculate_BP_from_VCG(df_vcg, params={'k1':1.,'k2':1.}, pluginFns={}):
  plugin('start',pluginFns, locals())
  
  ##### Get Vectors (signals) from df_vcg #####
  vcg_xp = df_vcg['az']
  # vcg_aar = df_vcg['ax']    # TODO : Fetch VCG_Aar, using ax for now..
  plugin('vcg',pluginFns, locals())

  ##### Acceleration -> Displacement #####
  dXp, vXp = displacement(vcg_xp)
  # dXp_y, vXp_y = displacement(df_vcg['ay'])
  dXp_z, vXp_z = displacement(df_vcg['az'])
  # dXp_Norm = np.linalg.norm(np.array([dXp,dXp_y,dXp_z]), axis=0)
  dXp_Norm = np.linalg.norm(np.array([np.nan_to_num(dXp,1.),np.nan_to_num(dXp_z,1.)]), axis=0)
  # dXp_Norm = np.array([np.nan_to_num(dXp,1.)])
  
  # dAar, vAar = displacement(vcg_aar)
  # deltaDisp = dXp - dAar
  deltaDisp = dXp_Norm
  plugin('disp',pluginFns, locals())

  ##### Respiration Volume #####
  RV = window_rms(vcg_xp, 20).max()
  plugin('RV',pluginFns, locals())

  ##### BP at Aorta #####
  bp_Aar = params['k1'] * deltaDisp / RV    ## TODO : is trimming this to size okay?

  ##### Beat to Beat #####
  BTB = (vcg_xp.index.max() - vcg_xp.index.min()).total_seconds()

  BP_f = BTB * bp_Aar + params['k2']
  
  ##### Finalize SBP and DBP #####
  SBP = BP_f.max()
  DBP = BP_f.min()
  plugin('BP',pluginFns, locals())
  
  ##### End #####
  plugin('end',pluginFns, locals())
  return SBP, DBP


from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.base import BaseEstimator

# https://scikit-learn.org/stable/developers/develop.html
class AnalyticalBPEstimatorFixed(BaseEstimator):
  def __init__(self, target='sbp', k1=700., k2=100.):
    self.k1 = k1
    self.k2 = k2
    self.target = target

  def fit(self, X, y):
    ## GridSearch Params
    
    # self.X_ = X
    # self.y_ = y
    # Return the classifier
    return self

  def predict(self, X):

    # closest = np.argmin(euclidean_distances(X, self.X_), axis=1)
    y_preds = []
    # print('AnalyticalBPEstimator.predict', X.shape)
    for row in X:
      dfHeartBeat = pd.DataFrame(row, columns=['ts','az','ax']).replace(0, np.NaN).set_index('ts').dropna()
      y_pred = calculate_BP_from_VCG(dfHeartBeat[dfHeartBeat.index!=0], params={'k1':self.k1, 'k2':self.k2})
      y_preds.append(y_pred[0] if self.target=='sbp' else y_pred[1])
    
    return np.array(y_preds).clip(40,180)
  
  def score(self, rows, y):
    return 1
    # return np.abs((self.predict(rows))-y).fillna(0).mean()


from sklearn.model_selection import GridSearchCV

class AnalyticalBPEstimator(AnalyticalBPEstimatorFixed):
  def __init__(self, target='sbp', k1_range=(1e4,1e7), k2_range=(45,160), nsteps=5, k1=0., k2=0.):
    self.k1_range = k1_range
    self.k1 = k1_range[0]
    self.k2_range = k2_range
    self.k2 = k2_range[0]
    self.target = target
    self.nsteps = nsteps
  
  def fit(self, X, y):
    ## GridSearch Params
    
    reg = GridSearchCV(AnalyticalBPEstimatorFixed(target=self.target), {
        'k1':np.arange(self.k1_range[0], self.k1_range[1],(self.k1_range[1]-self.k1_range[0])/self.nsteps),
        'k2':np.arange(self.k2_range[0], self.k2_range[1], (self.k2_range[1]-self.k2_range[0])/self.nsteps)
    }, scoring='r2')

    inds = (np.random.rand(30)*y.shape).astype(int)
    reg.fit(X[inds],y[inds])
    print('Fitted Parameters : ', reg.best_params_)
    self.set_params(**reg.best_params_)
    return self
