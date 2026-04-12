from abc import ABC, abstractmethod

class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, file_bytes: bytes) -> str:
        """
        Extracts text from PDF bytes.
        
        Args:
            file_bytes: Raw bytes of the PDF file.
            
        Returns:
            str: Extracted text content.
        """
        pass
