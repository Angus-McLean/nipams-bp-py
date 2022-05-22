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


from sklearn.base import TransformerMixin, BaseEstimator
class Debug(BaseEstimator, TransformerMixin):
    def transform(self, X, name=None):
        print(f'PipelineDebug:{name or ""}: {X.shape}')
        self.shape = X.shape
        self.head = X[:5]
        # what other output you want
        return X

    def fit(self, X, y=None, **fit_params):
        return self
