class NoImagesException(Exception):
    def __init__(self, directory, message=""):
        self.directory = directory
        self.message = f"No images found in {directory}!"
        super().__init__(self.message)

