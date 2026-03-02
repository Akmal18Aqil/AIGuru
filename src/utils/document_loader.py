import os
from pypdf import PdfReader
from docx import Document

def load_document_text(filepath: str) -> str:
    """
    Extracts text from PDF or DOCX file.
    """
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    
    try:
        if ext == '.pdf':
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif ext in ['.docx', '.doc']:
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            return f"Unsupported file format: {ext}"
            
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"
