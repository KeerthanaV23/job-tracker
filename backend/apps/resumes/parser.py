import io

import pdfplumber


class ResumeParseError(ValueError):
    pass


def extract_text_from_pdf(file_obj) -> str:
    """Extract text from an uploaded PDF (file-like object)."""
    try:
        data = file_obj.read()
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            pages = [(page.extract_text() or "") for page in pdf.pages]
    except Exception as exc:  # corrupt / not a pdf
        raise ResumeParseError("Could not read the PDF. Upload a valid text-based PDF.") from exc
    text = "\n".join(pages).strip()
    if not text:
        raise ResumeParseError("No text found in PDF (scanned images are not supported).")
    return text
