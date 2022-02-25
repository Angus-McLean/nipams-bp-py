from utils.constants import *


from sklearn.base import BaseEstimator

# https://scikit-learn.org/stable/developers/develop.html
class TSAI_InceptionTime(BaseEstimator):
  def __init__(self, target='sbp', k1=700., k2=100.):
    self.k1 = k1
    self.k2 = k2
    self.target = target

    # https://colab.research.google.com/drive/16f2Rs7fQ0e3DBPcK_dSS9jylT8ZjOnOi#scrollTo=1aPV-4xPNc7-
    # learn = load_learner(MODEL_PATH, cpu=False)
    



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
    
    return np.array(y_preds).clip(40,180)
  
  ## TODO : proper scoring method
  ## TODO : also this breaks the mvd method somehow?
  def score(self, rows, y):
    # return 1
    return np.abs((self.predict(rows))-y).fillna(0).mean()

