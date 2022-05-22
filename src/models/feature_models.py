from utils.constants import *
import sklearn
from data import preprocess;
from sklearn import pipeline, ensemble
from sklearn.pipeline import Pipeline

from features import simple as features_simple


pipe_vect_simple = Pipeline([
    ('transform', preprocess.FunctionTransformer(partial(features_simple.vectorize_mean_std))),
    ('model', sklearn.ensemble.RandomForestRegressor())
])

