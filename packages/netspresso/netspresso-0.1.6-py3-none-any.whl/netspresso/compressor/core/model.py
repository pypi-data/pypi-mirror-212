class Model:
    def __init__(self, model_info) -> None:
        self.model_id = model_info.model_id
        self.model_name = model_info.model_name
        self.framework = model_info.framework
        self.task = model_info.task
        self.spec = model_info.spec


class CompressedModel(Model):
    def __init__(self, model_info) -> None:
        super().__init__(model_info)
        self.compression_id = model_info.original_compression_id
        self.original_model_id = model_info.original_model_id
