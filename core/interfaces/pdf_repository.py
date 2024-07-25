from abc import ABC, abstractmethod

class PDFRepositoryInterface(ABC):
    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        pass
