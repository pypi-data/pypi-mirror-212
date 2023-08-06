class CompressionBase:
    def __init__(self, compression_method, available_layers, model_id):
        self.compression_method = compression_method
        self.available_layers = available_layers
        self.model_id = model_id


class CompressionInfo(CompressionBase):
    def __init__(self, compression_info, model_id):
        super().__init__(compression_info.compression_method, compression_info.available_layers, model_id)
        self.new_model_id = compression_info.new_model_id
        self.compression_id = compression_info.compression_id
