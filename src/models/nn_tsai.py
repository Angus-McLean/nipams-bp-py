from sklearn.base import BaseEstimator
from tsai.all import *


# https://scikit-learn.org/stable/developers/develop.html
class TSAI_InceptionTime(BaseEstimator):
  def __init__(self, target='sbp', n_epoch=10):
    self.target = target
    self.n_epoch = n_epoch

  def setup_dls(self, X, y):
    tfms  = [None, [TSRegression()]]
    batch_tfms = TSStandardize(by_var=True)
    splits = TrainValidTestSplitter(valid_size=0.2, shuffle=True)(y)

    dls = get_ts_dls(X, y, splits=splits, tfms=tfms, batch_tfms=batch_tfms, bs=20)
    return dls


  def fit(self, X, y):
    print('TSAI.fit X', X.dtype, X.shape)
    print('TSAI.fit y', y.dtype, y.shape)
    
    X = X[:,1:,:].astype(np.float32)
    y = y.values
    
    print('TSAI.fit X', X.dtype, X.shape)
    print('TSAI.fit y', y.dtype, y.shape)
    self.y_train = y
    y = (y - y.mean()) / y.std()

    self.dls = self.setup_dls(X, y)
    
    # self.learn = ts_learner(self.dls, InceptionTime, metrics=[mae, rmse], cbs=ShowGraph())
    self.learn = ts_learner(self.dls, InceptionTime, metrics=[mae, rmse])
    self.learn.fit_one_cycle(self.n_epoch, 1e-3)

    return self

  def predict(self, X):
    # X = X[:,:,1:].astype(np.float32)
    X = X[:,1:,:].astype(np.float32)
    
    probas, _, preds = self.learn.get_X_preds(X)
    yPreds = self.unnorm_y(np.array(preds).flatten())
    return np.array(yPreds).clip(40,180)
    

  def unnorm_y(self, ser):
    return (ser*self.y_train.std()+self.y_train.mean())

  ## TODO : proper scoring method
  ## TODO : also this breaks the mvd method somehow?
  def score(self, rows, y):
    # return 1
    return np.abs((self.predict(rows))-y).fillna(0).mean()