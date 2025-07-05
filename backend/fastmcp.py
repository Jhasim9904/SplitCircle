class ModelNode:
    def __init__(self, name: str):
        self.name = name

    def run(self, **kwargs):
        raise NotImplementedError("Each model node must implement its run() method.")

class FastMCP:
    def __init__(self):
        self.models = {}

    def register_model(self, model: ModelNode):
        self.models[model.name] = model

    def run_model(self, name: str, **kwargs):
        if name not in self.models:
            raise ValueError(f"Model '{name}' not found! Registered models: {list(self.models.keys())}")

        try:
            result = self.models[name].run(**kwargs)
            return result
        except Exception as e:
            # 👇 You can log the exception to console for debugging
            print(f"[FastMCP] Error running model '{name}': {e}")
            return {"error": f"Model '{name}' failed to run: {str(e)}"}
