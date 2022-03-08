from utils.constants import *

from sklearn.dummy import DummyRegressor

class RandomRegressor():
  def fit(self, X, Y):
    self.serY = pd.Series(Y)
    return self
  def predict(self, rows, *args):
    return self.serY.sample(len(rows), replace=True).values
  def score(self, rows, y):
    return np.abs((self.predict(rows))-y)