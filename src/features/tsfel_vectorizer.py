import tsfel
from sklearn.preprocessing import FunctionTransformer
from utils.constants import *

def VectorLookup(dfVectors):
  def vectLookup(input_series):
    indInput = input_series.groupby(INDICIES, sort=False).count().index.to_frame().drop(INDICIES, axis=1)
    dfTsVects = pd.merge(indInput, dfVectors, how='left', left_index=True, right_index=True)
    # dfTsVects = pd.merge(indInput, dfVectors, how='left', on=INDICIES)
    print('output_series.shape',dfTsVects.shape, dfTsVects.isna().sum(axis=1).value_counts())
    return dfTsVects.replace((np.inf, -np.inf), np.NaN).fillna(0).select_dtypes(np.number)
  return vectLookup

def vectorize_tsfel(input_series, cfg='statistical'):
  print('input_series.shape',input_series.shape)
  dfTsVects = input_series[INDICIES + IMU_DATA_COLS]\
    .groupby(INDICIES, sort=False)[IMU_DATA_COLS]\
    .apply(
      lambda x : tsfel.time_series_features_extractor(tsfel.get_features_by_domain(cfg), x)
    )
  # indInput = input_series.groupby(INDICIES, sort=False).count().index.to_frame().drop(INDICIES, axis=1)
  # dfTsVects = pd.merge(indInput, dfTsfelVects_stat, how='left', left_index=True, right_index=True)
  print('output_series.shape',dfTsVects.shape)
  return dfTsVects.replace((np.inf, -np.inf), np.NaN).fillna(0)

# dfVects = pd.read_feather("/content/drive/My Drive/BP ML data/cached data/dfImuVects-"+"HLV"+".feather").set_index(['file','heartbeat'])
def transform_vectorLookup(dfVects):
  tsfelVectTransform = FunctionTransformer(VectorLookup(dfVects))
  return tsfelVectTransform

def transform_selectFeatures(selected_features):
  def selectFeatures(x, features=[]):
    selFeats = np.intersect1d(x.columns, features)
    # print("transform_selectFeatures : ", x[selFeats].shape, x[selFeats].dropna().shape,  selFeats)
    return x[selFeats]

  vectFeatureSelection = FunctionTransformer(partial(selectFeatures, features=selected_features))
  return vectFeatureSelection

def panelTSDataToVectors(data, indicies=INDICIES, data_columns=IMU_DATA_COLS, domains=['statistical','temporal','spectral']):
    arrDfs = []
    for i in domains:
        cfg = tsfel.get_features_by_domain(i)
        dfTsfelVects = data.groupby(indicies, sort=False)[data_columns].apply(lambda x : tsfel.time_series_features_extractor(cfg, x))
        dfTsfelVects = dfTsfelVects.reset_index(level=2, drop=True)
        arrDfs.append(dfTsfelVects)

    return pd.concat(arrDfs, axis=1).replace((np.inf, -np.inf), np.NaN).fillna(0)