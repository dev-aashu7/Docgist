"""
DocGist — PDF Processing Module
Extracts text locally from PDF documents using pypdf.
Validates empty, encrypted, or scanned (image-only) files without storing files to disk.
"""

from io import BytesIO
from typing import Any, Dict, List, Union
import pypdf
from pypdf.errors import FileNotDecryptedError, PdfReadError


def extract_text_from_pdf(file_source: Union[str, BytesIO, Any]) -> Dict[str, Any]:
    """
    Extracts text locally and safely from a PDF file.

    Parameters:
        file_source: File path, BytesIO object, or Streamlit UploadedFile.

    Returns:
        dict containing:
            - success (bool): True if readable text was extracted, False otherwise.
            - text (str): The extracted text across all pages.
            - page_count (int): Total number of pages in the PDF.
            - char_count (int): Total characters in extracted text.
            - word_count (int): Total words in extracted text.
            - pages (list): List of dicts with per-page text: [{'page_number': 1, 'text': '...', 'char_count': ...}]
            - error (str or None): Beginner-friendly error description if extraction fails.
    """
    if file_source is None:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "word_count": 0,
            "pages": [],
            "error": "No PDF file provided for extraction."
        }

    # Reset stream cursor if the object supports seeking
    if hasattr(file_source, "seek"):
        try:
            file_source.seek(0)
        except Exception:
            pass

    try:
        reader = pypdf.PdfReader(file_source)
    except PdfReadError as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "word_count": 0,
            "pages": [],
            "error": f"Unable to read this file as a valid PDF. It may be corrupted or not a standard PDF format ({str(e)})."
        }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "word_count": 0,
            "pages": [],
            "error": f"An unexpected error occurred while reading the PDF: {str(e)}"
        }

    # Check for password protection
    if reader.is_encrypted:
        try:
            # Some PDFs are marked encrypted with an empty password
            decrypted = reader.decrypt("")
            if not decrypted:
                return {
                    "success": False,
                    "text": "",
                    "page_count": len(reader.pages) if hasattr(reader, "pages") else 0,
                    "char_count": 0,
                    "word_count": 0,
                    "pages": [],
                    "error": "This PDF is password-protected. Please upload an unlocked PDF file."
                }
        except (FileNotDecryptedError, Exception):
            return {
                "success": False,
                "text": "",
                "page_count": 0,
                "char_count": 0,
                "word_count": 0,
                "pages": [],
                "error": "This PDF is password-protected. Please upload an unlocked PDF file."
            }

    # Validate page count
    total_pages = len(reader.pages)
    if total_pages == 0:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "word_count": 0,
            "pages": [],
            "error": "The uploaded PDF document contains 0 pages."
        }

    # Extract text page by page
    extracted_pages: List[Dict[str, Any]] = []
    text_chunks: List[str] = []

    for page_idx, page in enumerate(reader.pages, start=1):
        try:
            raw_page_text = page.extract_text() or ""
        except Exception as e:
            raw_page_text = ""

        cleaned_page_text = raw_page_text.strip()
        extracted_pages.append({
            "page_number": page_idx,
            "text": cleaned_page_text,
            "char_count": len(cleaned_page_text),
            "word_count": len(cleaned_page_text.split()) if cleaned_page_text else 0
        })

        if cleaned_page_text:
            text_chunks.append(cleaned_page_text)

    combined_text = "\n\n".join(text_chunks).strip()

    # Detect scanned image-only PDFs (where no digital text could be extracted)
    if not combined_text:
        return {
            "success": False,
            "text": "",
            "page_count": total_pages,
            "char_count": 0,
            "word_count": 0,
            "pages": extracted_pages,
            "error": (
                "No readable text found in this PDF. It appears to be a scanned image or photo. "
                "OCR (Optical Character Recognition) is not supported yet. "
                "Please paste the text manually using the 'Paste Text' tab, or upload a searchable digital PDF."
            )
        }

    return {
        "success": True,
        "text": combined_text,
        "page_count": total_pages,
        "char_count": len(combined_text),
        "word_count": len(combined_text.split()),
        "pages": extracted_pages,
        "error": None
    }


def create_sample_text_pdf(text_lines: List[str]) -> bytes:
    """
    Creates a valid, lightweight PDF with extractable text lines in pure Python.
    Useful for testing PDF uploads without external PDF generation libraries.
    """
    stream_content = "BT\n/F1 11 Tf\n50 750 Td\n14 TL\n"
    for line in text_lines:
        safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_content += f"({safe_line}) '\n"
    stream_content += "ET"
    stream_bytes = stream_content.encode("latin-1", "replace")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        f"5 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii") + stream_bytes + b"\nendstream\nendobj\n"
    ]

    header = b"%PDF-1.4\n"
    body = b""
    offsets = [0]
    curr_offset = len(header)
    for obj in objects:
        offsets.append(curr_offset)
        body += obj
        curr_offset += len(obj)

    xref_offset = len(header) + len(body)
    xref = f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii")
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("ascii")

    trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    return header + body + xref + trailer


def create_blank_scanned_pdf_simulation() -> bytes:
    """
    Creates a valid PDF containing blank pages (0 extractable text characters)
    to simulate a scanned image-only PDF and test OCR validation handling.
    """
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()

