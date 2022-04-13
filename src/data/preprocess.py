
from utils.constants import *

from datetime import timedelta
from scipy import signal, interpolate
import warnings

#@title Implement Filter Split
def get_cycles(dfBp,dfImu,t_cc=0.1):
  dfBp = dfBp.copy()
  dfImu = dfImu.copy()
  ind_cc_bp = []
  ind_cc_imu = []

  dfBp['Rpk'] = dfBp['ecgTs'].round()==4
  tccs = dfBp.query('Rpk').index-timedelta(seconds=t_cc)
  dfBp['tsCC'] = False
  dfImu['tsCC'] = False
  for tcc_now in tccs:
    ind_cc_bp.append(dfBp.index.get_loc(tcc_now, method='nearest'))
    ind_cc_imu.append(dfImu.index.get_loc(tcc_now, method='nearest'))

  # dfBp['tsCC'].iloc[ind_cc_bp] = True
  # dfImu['tsCC'].iloc[ind_cc_imu] = True
  dfBp.iloc[ind_cc_bp, dfBp.columns.get_loc('tsCC')] = True
  dfImu.iloc[ind_cc_imu, dfImu.columns.get_loc('tsCC')] = True


  dfBp['heartbeat'] = dfBp['tsCC'].cumsum()
  dfImu['heartbeat'] = dfImu['tsCC'].cumsum()
  #todo: drop ecgTs,Rpk, tsCC

  return dfBp, dfImu

def myInterp_Fs(df_now, COLS=IMU_DATA_COLS+['heartbeat'], fs=200):
  start = df_now.index[0].total_seconds()
  end = df_now.index[-1].total_seconds()
  dt = 1/fs
  ts_new = dt*np.arange(0,int(np.ceil((end-start)/dt)))+start
  td = pd.to_timedelta(ts_new,unit='s')
  f = interpolate.interp1d(df_now.index.total_seconds().to_list(),df_now[COLS], axis=0,fill_value="extrapolate")
  y = f(ts_new)
  df_new = pd.DataFrame(data=y,index=td, columns=COLS)
  NonNumCols = df_now.columns[~df_now.columns.isin(COLS)]
  for col in NonNumCols:
    df_new[col] = df_now[col][0]
  return df_new

def filterSplit(dfBpCont, dfImuCont,fs=200):
  # display(dfBpAll) 
  bp_groups = dfBpCont.groupby('file')
  imu_groups = dfImuCont.groupby('file')

  dfBpAll = pd.DataFrame()
  dfImuRawAll = pd.DataFrame()
  dfImuFiltLpAll = pd.DataFrame()
  dfImuFiltHpAll = pd.DataFrame()
  for name, dfBp_now in bp_groups:
    # display(name)
    # display(dfBp_now)
    dfImu_now = imu_groups.get_group(name)

    # Get Cardiac Cycles
    warnings.filterwarnings('ignore')
    dfBp_now, dfImu_now = get_cycles(dfBp_now,dfImu_now, t_cc = 0.1)
    warnings.filterwarnings('default')
    
    # Remove 1st/last
    dfBp_now = dfBp_now[dfBp_now['heartbeat'] != 0]; dfBp_now = dfBp_now[dfBp_now['heartbeat'] != max(dfBp_now['heartbeat'])]
    dfImu_now = dfImu_now[dfImu_now['heartbeat'] != 0]; dfImu_now = dfImu_now[dfImu_now['heartbeat'] != max(dfImu_now['heartbeat'])]
    
    # Interpolate to standard fs
    dfImuSamp = myInterp_Fs(dfImu_now.interpolate(),fs=fs)
    dfBpSamp = myInterp_Fs(dfBp_now,COLS=BP_COLS+['heartbeat'],fs=fs)
    # dfImuSamp, dfBpSamp = nm.load.interpolateDatasets(dfImu_now, dfBp_now)

    dfImuSamp['heartbeat'] = np.floor(dfImuSamp['heartbeat'])
    dfBpSamp['heartbeat'] = np.floor(dfBpSamp['heartbeat'])
    
    # Filter IMU
    dfImuSamp = dfImuSamp.fillna(method = 'ffill').fillna(method = 'bfill')
    # dfImuFiltLp = filter_df(dfImuSamp,filt_type='bandstop',fc=fc)
    # dfImuFiltHp = filter_df(dfImuSamp,filt_type='high',fc=fc)
    
    # Remove BP Nans (and in IMU)
    del_hb = dfBpSamp['heartbeat'][dfBpSamp.sbp.isna()].unique()
    dfBpSamp = dfBpSamp[~dfBpSamp['heartbeat'].isin(del_hb)]
    dfImuSamp = dfImuSamp[~dfImuSamp['heartbeat'].isin(del_hb)]
    # dfImuFiltLp = dfImuFiltLp[~dfImuFiltLp['heartbeat'].isin(del_hb)]
    # dfImuFiltHp = dfImuFiltHp[~dfImuFiltHp['heartbeat'].isin(del_hb)]
    # todo: Re-number HBs to 0:len?
    # Make BP Targets (single value)
    try:
      BpTargets = dfBpSamp.groupby('heartbeat').apply(lambda x: x[BP_COLS].mean())
      BpTargets['file'] = dfBpSamp.reset_index().file[0]
      BpTargets['test_type'] = dfBpSamp.test_type[0]
      BpTargets['test_num'] = dfBpSamp.test_num[0]
      BpTargets['patient'] = dfBpSamp.patient[0]
        # Make IMU raw feats (500 values)
        # dfImuRaw = interpBeats(dfImuSamp)
        # Make IMU filt feats(500 values)
        # dfImuFreqFiltLp = interpBeats(dfImuFiltLp)
        # dfImuFreqFiltHp = interpBeats(dfImuFiltHp)
        # Append BP, imu raw, imu filt
      dfBpAll = pd.concat([dfBpAll , BpTargets])
      dfImuRawAll = pd.concat([dfImuRawAll , dfImuSamp])
      # dfImuFiltLpAll = dfImuFiltLpAll.append(dfImuFreqFiltLp)
      # dfImuFiltHpAll = dfImuFiltHpAll.append(dfImuFreqFiltHp)
    except Exception as e:
      print("Error with file", print(name), str(e))
    
  return dfBpAll, dfImuRawAll#, dfImuFiltLpAll#, dfImuFiltHpAll


#### CLEAN, FIND HBs AND UNIFY VCG & BP ####
def merge_imu_vcg_with_heartbeats(dfBpAll, dfImuAll):
  dfBp, dfImuRaw = filterSplit(dfBpAll.set_index('ts'), dfImuAll.set_index('ts'))
  dfImuRaw['ts'] = dfImuRaw.index.total_seconds()
  dfImuRaw = dfImuRaw.reset_index(drop=True)
  dfImuRaw = dfImuRaw.set_index('file')

  dfAll = dfImuRaw.merge(dfBp, how='left', on=INDICIES, suffixes=('','_drop'))
  dfAll.ts = pd.to_timedelta(dfAll.ts*1e9)
  dfAll = dfAll.drop(dfAll.columns[dfAll.columns.str.contains('_drop')], axis=1)

  return dfAll


def interpolateDatasets(dfImu, dfBp, freq='5ms', groupbyCol='file', method='linear'):
  dfBpSamp = dfBp.groupby(groupbyCol).apply(lambda x:x.resample(freq).interpolate(method=method))#.reset_index(groupbyCol, drop=True)
  dfImuSamp = dfImu.groupby(groupbyCol).apply(lambda x:x.resample(freq).interpolate(method=method))#.reset_index(groupbyCol, drop=True)#.drop('file', axis=1).reset_index()
  
  # interpolation doesn't work from strings.. fill in the NaNs
  serBpNonNumCols = dfBpSamp.columns[~dfBpSamp.columns.isin(BP_COLS)]
  dfBpSamp[serBpNonNumCols] = dfBpSamp[serBpNonNumCols].fillna(method='ffill')
  serImuNonNumCols = dfImuSamp.columns[~dfImuSamp.columns.isin(IMU_DATA_COLS)]
  dfImuSamp[serImuNonNumCols] = dfImuSamp[serImuNonNumCols].fillna(method='ffill')

  return dfImuSamp, dfBpSamp



#@title Preprocessors - Enforce 3d shape
from sklearn.preprocessing import StandardScaler, FunctionTransformer

def forceShape(x, nsteps=300):
  x = x[:nsteps]
  return np.pad(x, ((0,nsteps-x.shape[0]),(0,0)))

# arrData = np.array(list(dfAll.groupby(INDICIES).apply(lambda x : forceShape(x[['az','ax']].values))))
import itertools
def explode_3d(dfImu, indicies=INDICIES, data_cols=IMU_DATA_COLS, nsteps=190):
  '''
    Converts timeseries signals dataframe into 3d matrix of ts samples
  '''
  dfInds = dfImu.groupby(indicies).first()

  df_ = pd.DataFrame(itertools.product(dfInds.index, range(nsteps)), columns=['ind','step'])
  df_ = pd.concat([df_, pd.DataFrame(df_['ind'].to_list(), columns=indicies)], axis=1).drop('ind', axis=1)

  dfImu['step'] = dfImu.groupby(indicies).file.cumcount()
  dfOut = df_.merge(dfImu, on=INDICIES+['step'], how='left').set_index(INDICIES)
  dfOut[IMU_DATA_COLS] = dfOut[IMU_DATA_COLS].fillna(method='ffill')
  # dfOut[TS] = dfOut.groupby(INDICIES)[TS].interpolate()
  dfOut[TS] = dfOut[TS].fillna(method='ffill')
  dfOut = dfOut[[TS]+data_cols]
  arrOut = dfOut.values.reshape(-1, nsteps, len(dfOut.columns))
  return arrOut

def Explode_3D_Transformer(indicies=INDICIES, data_cols=IMU_DATA_COLS, nsteps=190):
  tsExplodeTransform = FunctionTransformer(partial(explode_3d, indicies=indicies, data_cols=data_cols, nsteps=nsteps))
  return tsExplodeTransform


def explode_3d_old(input_series, indicies=INDICIES, data_cols=IMU_DATA_COLS, nsteps=170):
  '''
    Converts timeseries signals dataframe into 3d matrix of ts samples
  '''
  # dfTsVect = input_series[indicies + data_cols].groupby(indicies, sort=False).fillna(0)
  arrTsExp = np.array(list(
      input_series\
        .groupby(indicies, sort=False)\
        .apply(lambda x : forceShape(x[['ts']+data_cols].values, nsteps).T)
      )
  )
  return arrTsExp


from functools import partial
TransformerTimeSeriesTo3D = partial(FunctionTransformer, explode_3d)