from infrastructure.pdf.native_strategy import NativeExtractionStrategy
from infrastructure.ocr.tesseract_strategy import TesseractOCRStrategy
from infrastructure.ai.layoutlm_strategy import LayoutLMv3Strategy
import logging

class ExtractionFactory:
    @staticmethod
    def extract_with_fallback(file_bytes: bytes) -> str:
        # Strategy 1: Native Extraction (FAST)
        native = NativeExtractionStrategy()
        text = native.extract(file_bytes)
        
        # If Native fails or returns tiny text, try OCR
        if not text or len(text.strip()) < 50:
            logging.info("Native extraction failed or low quality. Falling back to OCR.")
            ocr = TesseractOCRStrategy()
            text = ocr.extract(file_bytes)
            
        # If text is still suspicious or if this is a Form, use LayoutLM (INTELLIGENT)
        # Here we could add a logic to detect if it's a known form type
        # For now, let's keep it as an option or based on a flag
        
        return text

    @staticmethod
    def extract_intelligent(file_bytes: bytes) -> str:
        """
        Force the use of LayoutLM for complex documents.
        """
        ai_strategy = LayoutLMv3Strategy()
        return ai_strategy.extract(file_bytes)
