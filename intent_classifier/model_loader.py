class MLModelLoader:
  def __init__(self, model_path: None):
    self.model_path = None
    if model_path:
      self.load(model_path) 

      
  def load(self, model_path: str):
    pass

  def predict(self, text: str):
    return None