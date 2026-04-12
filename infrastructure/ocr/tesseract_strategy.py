import pytesseract
from PIL import Image
from io import BytesIO
import logging
from core.interfaces.extraction_strategy import ExtractionStrategy

logger = logging.getLogger(__name__)

class TesseractOCRStrategy(ExtractionStrategy):
    def __init__(self, tesseract_cmd: str = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract(self, file_bytes: bytes) -> str:
        """
        Extracts text using OCR.
        Note: For real multi-page PDFs, extra conversion from PDF to Image 
        (e.g., using pdf2image) is required here.
        """
        try:
            # Simplified: Assuming image bytes or single page conversion logic
            image = Image.open(BytesIO(file_bytes))
            text = pytesseract.image_to_string(image, lang='por+eng')
            return text.strip()
        except Exception as e:
            logger.error(f"Error in OCR extraction: {e}")
            return ""
