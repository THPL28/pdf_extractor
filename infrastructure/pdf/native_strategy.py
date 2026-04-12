import PyPDF2
from io import BytesIO
import logging
from core.interfaces.extraction_strategy import ExtractionStrategy

logger = logging.getLogger(__name__)

class NativeExtractionStrategy(ExtractionStrategy):
    def extract(self, file_bytes: bytes) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            
            clean_text = text.strip()
            if not clean_text:
                logger.info("Native extraction returned empty text.")
                return ""
            
            return clean_text
        except Exception as e:
            logger.error(f"Error in native PDF extraction: {e}")
            return ""
