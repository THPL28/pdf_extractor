from fastapi import FastAPI, File, UploadFile
from core.use_cases.extract_text import ExtractTextUseCase
from infrastructure.pdf.pypdf2_pdf_repository import PyPDF2PDFRepository
from infrastructure.ocr.tesseract_ocr import TesseractOCRService
from config.config import TESSERACT_CMD

app = FastAPI()

# Initialize the use case with repositories
pdf_repository = PyPDF2PDFRepository()
ocr_service = TesseractOCRService()
extract_text_use_case = ExtractTextUseCase(pdf_repository, ocr_service)

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_use_case.execute(pdf_bytes)
    return {"text": text}
