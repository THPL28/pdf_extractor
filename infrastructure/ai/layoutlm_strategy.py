from core.interfaces.extraction_strategy import ExtractionStrategy
from pdf2image import convert_from_bytes
import pytesseract
from transformers import LayoutLMv3Processor, LayoutLMv3ForSequenceClassification
import torch
import json

class LayoutLMv3Strategy(ExtractionStrategy):
    """
    Intelligent extraction using LayoutLMv3 for document understanding.
    This strategy can be used to classify documents or extract specific fields 
    based on their spatial location.
    """
    def __init__(self):
        # We initialize the model. In production, this should be done using a singleton
        # or loaded outside the main loop to avoid overhead.
        self.processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
        # Note: For real field extraction, you'd use ForTokenClassification
        self.model = LayoutLMv3ForSequenceClassification.from_pretrained("microsoft/layoutlmv3-base")

    def extract(self, file_bytes: bytes) -> str:
        # 1. Convert PDF to images (one per page)
        pages = convert_from_bytes(file_bytes)
        
        results = []
        for i, page in enumerate(pages):
            # 2. Process image with LayoutLMv3
            # LayoutLMv3 can use Tesseract internally if configured
            encoding = self.processor(page, return_tensors="pt")
            
            # 3. Model Inference
            with torch.no_grad():
                outputs = self.model(**encoding)
            
            # Since this is a base implementation, we'll return a structured summary
            # In a real use case, here we would map extracted tokens to fields (Name, Date, Total)
            results.append({
                "page": i + 1,
                "layout_analysis": "Completed",
                "text_content": pytesseract.image_to_string(page)
            })
            
        return json.dumps(results, indent=2)
