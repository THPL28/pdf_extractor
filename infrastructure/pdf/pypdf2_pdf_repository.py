import PyPDF2
from core.interfaces.pdf_repository import PDFRepositoryInterface
from io import BytesIO

class PyPDF2PDFRepository(PDFRepositoryInterface):
    def extract_text(self, pdf_bytes: bytes) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
