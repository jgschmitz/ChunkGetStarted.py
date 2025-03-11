import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file with fallback handling."""
    reader = PdfReader(pdf_path)
    text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

    # Fallback for better text extraction
    if not text.strip():
        with pdfplumber.open(pdf_path) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    return text
