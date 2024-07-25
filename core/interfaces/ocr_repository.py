from abc import ABC, abstractmethod

class OCRRepositoryInterface(ABC):
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        pass
