from .train_model import preprocessInputs

def predict(model, raw_inputs):
  return model.predict(preprocessInputs(raw_inputs))
