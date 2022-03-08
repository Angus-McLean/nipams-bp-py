from utils.constants import *
from sklearn.preprocessing import FunctionTransformer

def vectorize_mean_std(input_series, indicies=INDICIES, data_cols=IMU_DATA_COLS):
  dfTsVect = input_series[indicies + data_cols].groupby(indicies, sort=False).agg(['mean','std']).fillna(0)
  dfTsVect.columns = ['_'.join(col).strip() for col in dfTsVect.columns.values]
  return dfTsVect
# VectMeanStd = FunctionTransformer(vectorize_mean_std)

