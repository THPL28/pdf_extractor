class Document:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = ""

    def add_text(self, text: str):
        self.text += text
