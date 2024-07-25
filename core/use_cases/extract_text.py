from core.interfaces.pdf_repository import PDFRepositoryInterface
from core.interfaces.ocr_repository import OCRRepositoryInterface

class ExtractTextUseCase:
    def __init__(self, pdf_repository: PDFRepositoryInterface, ocr_service: OCRRepositoryInterface):
        self.pdf_repository = pdf_repository
        self.ocr_service = ocr_service

    def execute(self, pdf_bytes: bytes) -> str:
        text = self.pdf_repository.extract_text(pdf_bytes)
        if not text:
            text = self.ocr_service.extract_text(pdf_bytes)
        return text
