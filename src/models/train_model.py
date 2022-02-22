#@title Define Training Loop
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def preprocessInputs(df):
  return preprocessing.StandardScaler().fit_transform(df)

def trainModelForDf(df, inputCols, targetCol, test_size=0.33):
  X = preprocessInputs(df[inputCols])
  y = df[targetCol]

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

  model = RandomForestClassifier(max_depth=2, random_state=0)
  model.fit(X_train, y_train)
  print('model.score',model.score(X_test, y_test))
  return model
