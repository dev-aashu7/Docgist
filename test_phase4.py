"""
Automated unit and integration test suite for DocGist Phase 4.
Tests evidence-based risk assessment, exact quotation verification (anti-hallucination guardrail),
Pydantic risk schemas, and Streamlit UI risk tab rendering.
"""

from pydantic import ValidationError
from gemini_analyzer import (
    verify_quotation,
    mock_analyze_document,
    RiskClauseSchema,
    DocumentAnalysisSchema
)
from streamlit.testing.v1 import AppTest


SAMPLE_DOC = """HOUSE / PG RENTAL AGREEMENT
Monthly rent shall be INR 12,000 payable in advance on or before the 1st of every calendar month.
Delay will attract a penalty of INR 200 per day.
The Tenant deposits a sum of INR 36,000 as refundable security deposit.
The Landlord reserves the absolute right to terminate this tenancy with 24 hours verbal notice.
"""


def test_quotation_exact_match():
    quote = "Delay will attract a penalty of INR 200 per day."
    res = verify_quotation(SAMPLE_DOC, quote)
    assert res["is_verified"] is True
    assert res["match_type"] == "exact"
    assert res["score"] == 1.0
    assert "Verified" in res["badge_text"]
    print("PASS: Exact verbatim quotation verified with 100% score.")


def test_quotation_normalized_whitespace_match():
    # Quote with modified line breaks/spaces (common in PDF extraction)
    quote = "Monthly rent shall be INR 12,000\npayable in advance on or before the 1st\n   of every calendar month."
    res = verify_quotation(SAMPLE_DOC, quote)
    assert res["is_verified"] is True
    assert res["match_type"] == "normalized"
    assert res["score"] == 1.0
    print("PASS: Quotation with line breaks normalized and verified.")


def test_quotation_hallucination_detection():
    fake_quote = "Tenant must pay 6 months advance rent upon signing and no refunds shall be granted."
    res = verify_quotation(SAMPLE_DOC, fake_quote)
    assert res["is_verified"] is False
    assert res["match_type"] == "unverified"
    assert "Unverified" in res["badge_text"]
    print("PASS: Fabricated / hallucinated quote successfully caught and marked unverified.")


def test_quotation_empty_handling():
    res = verify_quotation(SAMPLE_DOC, "")
    assert res["is_verified"] is False
    assert res["match_type"] == "empty"
    print("PASS: Empty quotation safely handled.")


def test_risk_schema_validation():
    valid_risk = {
        "level": "red",
        "title": "24-Hour Verbal Eviction Notice",
        "explanation": "Standard leases require 30 days written notice.",
        "exact_quote": "The Landlord reserves the absolute right to terminate this tenancy with 24 hours verbal notice."
    }
    parsed = RiskClauseSchema(**valid_risk)
    assert parsed.level == "red"
    assert len(parsed.title) > 0

    # Ensure missing quote triggers validation error
    try:
        RiskClauseSchema(level="red", title="Test", explanation="Test")
        assert False, "Should fail without exact_quote"
    except ValidationError:
        pass
    print("PASS: RiskClauseSchema strictly enforces exact_quote presence.")


def test_mock_analyzer_risks_and_verification():
    res = mock_analyze_document(SAMPLE_DOC)
    assert res["success"] is True
    risks = res["data"]["risks"]
    assert len(risks) > 0

    # Verify every risk item has a programmatic verification result
    for r in risks:
        assert "verification" in r
        assert r["level"] in ["red", "yellow", "green"]
        assert len(r["exact_quote"]) > 0

    print("PASS: Mock analyzer populates risks with programmatic verification.")


def test_streamlit_phase4_ui_risk_rendering():
    at = AppTest.from_file("app.py", default_timeout=20)
    at.run()
    assert not at.exception, f"Crash on load: {at.exception}"

    # Select preset sample
    at.radio[0].set_value(at.radio[0].options[2]).run()
    at.button[0].click().run()
    assert not at.exception, f"Crash running analysis: {at.exception}"

    # Verify risk metrics / chips rendered
    assert len(at.metric) >= 3
    print("PASS: Streamlit UI renders Phase 4 risk tally chips and cards cleanly.")


if __name__ == "__main__":
    print("=" * 60)
    print("Running DocGist Phase 4 Automated Test Suite")
    print("=" * 60)
    test_quotation_exact_match()
    test_quotation_normalized_whitespace_match()
    test_quotation_hallucination_detection()
    test_quotation_empty_handling()
    test_risk_schema_validation()
    test_mock_analyzer_risks_and_verification()
    test_streamlit_phase4_ui_risk_rendering()
    print("=" * 60)
    print("ALL PHASE 4 TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
