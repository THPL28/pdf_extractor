import pytesseract
from PIL import Image
from io import BytesIO
from core.interfaces.ocr_repository import OCRRepositoryInterface
from config.config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class TesseractOCRService(OCRRepositoryInterface):
    def extract_text(self, image_bytes: bytes) -> str:
        try:
            image = Image.open(BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""
