class ModelNode:
    def __init__(self, name: str):
        self.name = name

    def run(self, **kwargs):
        raise NotImplementedError

class FastMCP:
    def __init__(self):
        self.models = {}

    def register_model(self, model: ModelNode):
        self.models[model.name] = model

    def run_model(self, name: str, **kwargs):
        if name not in self.models:
            raise ValueError(f"Model '{name}' not found!")
        return self.models[name].run(**kwargs)
