"""
Automated unit and integration test suite for DocGist Phase 2.
Tests local PDF processing (valid text, scanned image simulation, corrupted, encrypted)
and verifies the Streamlit AppTest interface.
"""

import io
import pypdf
from pdf_processor import (
    extract_text_from_pdf,
    create_sample_text_pdf,
    create_blank_scanned_pdf_simulation
)
from streamlit.testing.v1 import AppTest


def test_pdf_extraction_valid_text():
    sample_lines = [
        "HOUSE / PG RENTAL AGREEMENT",
        "Monthly rent: INR 12,000 payable on 1st of month.",
        "Security deposit: INR 36,000.",
        "Lock-in period: 6 months."
    ]
    pdf_bytes = create_sample_text_pdf(sample_lines)
    result = extract_text_from_pdf(io.BytesIO(pdf_bytes))

    assert result["success"] is True, f"Extraction failed: {result.get('error')}"
    assert result["page_count"] == 1, f"Expected 1 page, got {result['page_count']}"
    assert "HOUSE / PG RENTAL AGREEMENT" in result["text"]
    assert "INR 12,000" in result["text"]
    assert result["word_count"] > 10
    print("PASS: Valid text PDF extracted accurately with correct page count and text.")


def test_pdf_extraction_scanned_blank_image():
    # Simulates a scanned image-only PDF with 0 extractable text characters
    blank_bytes = create_blank_scanned_pdf_simulation()
    result = extract_text_from_pdf(io.BytesIO(blank_bytes))

    assert result["success"] is False, "Scanned PDF should fail extraction"
    assert "OCR" in result["error"], f"Error should explain OCR is not supported: {result['error']}"
    assert "scanned image" in result["error"].lower()
    print("PASS: Scanned PDF correctly flagged with informative OCR explanation.")


def test_pdf_extraction_encrypted():
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt("mypassword")
    buf = io.BytesIO()
    writer.write(buf)

    result = extract_text_from_pdf(io.BytesIO(buf.getvalue()))
    assert result["success"] is False, "Encrypted PDF should fail"
    assert "password" in result["error"].lower()
    print("PASS: Password-protected PDF correctly handled.")


def test_pdf_extraction_corrupted_bytes():
    result = extract_text_from_pdf(io.BytesIO(b"random corrupted bytes not a pdf"))
    assert result["success"] is False
    assert "corrupted" in result["error"].lower() or "valid pdf" in result["error"].lower()
    print("PASS: Corrupted PDF input gracefully handled.")


def test_streamlit_app_phase2_rendering():
    at = AppTest.from_file("app.py", default_timeout=20)
    at.run()
    assert not at.exception, f"App crashed on load: {at.exception}"
    print("PASS: Phase 2 Streamlit UI loaded cleanly.")


def test_streamlit_app_sample_preset():
    at = AppTest.from_file("app.py", default_timeout=20)
    at.run()

    # at.radio[0] is the document input method selector in the main view
    # options: ["📄 Upload PDF Document", "✍️ Paste Text Directly", "📚 Try Sample Presets"]
    input_selector = at.radio[0]
    input_selector.set_value(input_selector.options[2]).run()
    assert not at.exception, f"Crash switching to presets: {at.exception}"

    # Click Analyze button
    at.button[0].click().run()
    assert not at.exception, f"Crash analyzing preset: {at.exception}"
    print("PASS: Sample preset analyzed cleanly through UI.")


def test_streamlit_app_pasted_text():
    at = AppTest.from_file("app.py", default_timeout=20)
    at.run()

    input_selector = at.radio[0]
    input_selector.set_value(input_selector.options[1]).run()
    assert not at.exception, f"Crash switching to pasted text: {at.exception}"

    # Input custom text
    at.text_area[0].input("This is a custom test tenancy document with 30-day notice.").run()
    at.button[0].click().run()
    assert not at.exception, f"Crash analyzing pasted text: {at.exception}"
    print("PASS: Pasted text analyzed cleanly through UI.")


if __name__ == "__main__":
    print("=" * 60)
    print("Running DocGist Phase 2 Automated Test Suite")
    print("=" * 60)
    test_pdf_extraction_valid_text()
    test_pdf_extraction_scanned_blank_image()
    test_pdf_extraction_encrypted()
    test_pdf_extraction_corrupted_bytes()
    test_streamlit_app_phase2_rendering()
    test_streamlit_app_sample_preset()
    test_streamlit_app_pasted_text()
    print("=" * 60)
    print("ALL PHASE 2 TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
