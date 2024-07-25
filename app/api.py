from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from core.use_cases.extract_text import ExtractTextUseCase
from infrastructure.pdf.pypdf2_pdf_repository import PyPDF2PDFRepository
from infrastructure.ocr.tesseract_ocr import TesseractOCRService

app = FastAPI()

# Configure o caminho do executável do Tesseract OCR
tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Atualize com o caminho correto

# Crie instâncias dos serviços
pdf_repository = PyPDF2PDFRepository()
ocr_service = TesseractOCRService(tesseract_cmd)
extract_text_use_case = ExtractTextUseCase(pdf_repository, ocr_service)

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text_use_case.execute(contents)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
