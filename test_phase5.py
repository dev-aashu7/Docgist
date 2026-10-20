"""
DocGist — Phase 5 Automated Test Suite
Verifies:
1. Personalized Profile Eligibility Engine (evaluate_profile_eligibility)
2. Accurate matching across courses, academic years, domicile states, categories, and income caps
3. Verbatim quotation verification on extracted eligibility criteria
4. Graceful handling of rental/non-applicable documents
5. Streamlit AppTest UI rendering of Phase 5 personalized eligibility cards & dynamic updates
"""

import sys
import unittest
from sample_data import SAMPLE_DOCUMENTS, SAMPLE_ANALYSES
from gemini_analyzer import (
    evaluate_profile_eligibility,
    mock_analyze_document,
    verify_quotation,
    EligibilityCriterionSchema,
    DocumentEligibilitySchema
)


class TestPhase5Eligibility(unittest.TestCase):
    def setUp(self):
        self.scholarship_doc = SAMPLE_DOCUMENTS["Scholarship Notice (Sample)"]
        self.scholarship_eligibility = SAMPLE_ANALYSES["Scholarship Notice (Sample)"]["eligibility"]
        self.rental_doc = SAMPLE_DOCUMENTS["PG / Rental Agreement (Sample)"]
        self.internship_doc = SAMPLE_DOCUMENTS["Internship Offer Letter (Sample)"]

    def test_scholarship_fully_eligible(self):
        """User profile matching all criteria (B.Tech 3rd Yr, MH, OBC, <2.5L) should be fully eligible."""
        profile = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "3rd Year",
            "state": "Maharashtra",
            "category": "OBC (Non-Creamy Layer)",
            "income": "Below ₹2.5 Lakhs / year"
        }
        res = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile,
            self.scholarship_doc
        )
        self.assertTrue(res["applicable"])
        self.assertEqual(res["status_color"], "green")
        self.assertIn("Eligible", res["overall_status"])
        self.assertEqual(len(res["criteria_breakdown"]), 4)

        # Ensure all criteria have verified verbatim quotes
        for crit in res["criteria_breakdown"]:
            self.assertTrue(crit["quote_verification"]["is_verified"])
            self.assertEqual(crit["verdict_color"], "green")
        print("PASS: Fully eligible scholarship profile verified with green status and 100% quote verification.")

    def test_scholarship_state_mismatch(self):
        """Non-Maharashtra resident should be flagged as Ineligible for state domicile."""
        profile = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "3rd Year",
            "state": "Delhi",
            "category": "OBC (Non-Creamy Layer)",
            "income": "Below ₹2.5 Lakhs / year"
        }
        res = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile,
            self.scholarship_doc
        )
        self.assertTrue(res["applicable"])
        self.assertEqual(res["status_color"], "red")
        self.assertIn("Ineligible", res["overall_status"])

        # Check domicile row specifically
        domicile_row = next(c for c in res["criteria_breakdown"] if "Domicile" in c["criterion"])
        self.assertEqual(domicile_row["verdict_color"], "red")
        self.assertIn("State Mismatch", domicile_row["verdict_badge"])
        print("PASS: State domicile mismatch correctly flagged with red status.")

    def test_scholarship_income_exceeds_cap(self):
        """Income > 2.5L should be flagged as exceeding the income cap."""
        profile = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "2nd Year",
            "state": "Maharashtra",
            "category": "SC",
            "income": "₹5 Lakhs – ₹8 Lakhs / year"
        }
        res = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile,
            self.scholarship_doc
        )
        self.assertTrue(res["applicable"])
        self.assertEqual(res["status_color"], "red")
        income_row = next(c for c in res["criteria_breakdown"] if "Income" in c["criterion"])
        self.assertEqual(income_row["verdict_color"], "red")
        self.assertIn("Exceeds Cap", income_row["verdict_badge"])
        print("PASS: Income cap violation correctly detected and explained.")

    def test_scholarship_course_and_year_mismatch(self):
        """Non-engineering degree or wrong year should be caught."""
        # Course mismatch (B.Com)
        profile_bcom = {
            "course": "B.Com / BBA (Commerce / Management)",
            "year": "3rd Year",
            "state": "Maharashtra",
            "category": "ST",
            "income": "Below ₹2.5 Lakhs / year"
        }
        res_bcom = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile_bcom,
            self.scholarship_doc
        )
        course_row = next(c for c in res_bcom["criteria_breakdown"] if "Course" in c["criterion"])
        self.assertEqual(course_row["verdict_color"], "red")
        self.assertIn("Course Mismatch", course_row["verdict_badge"])

        # Year mismatch (1st Year)
        profile_1styr = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "1st Year",
            "state": "Maharashtra",
            "category": "ST",
            "income": "Below ₹2.5 Lakhs / year"
        }
        res_1st = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile_1styr,
            self.scholarship_doc
        )
        course_row2 = next(c for c in res_1st["criteria_breakdown"] if "Course" in c["criterion"])
        self.assertEqual(course_row2["verdict_color"], "red")
        self.assertIn("Year Mismatch", course_row2["verdict_badge"])
        print("PASS: Course and academic year mismatches correctly evaluated.")

    def test_scholarship_general_category_reservation_check(self):
        """General category student applying for SC/ST/OBC scholarship should be flagged."""
        profile_gen = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "2nd Year",
            "state": "Maharashtra",
            "category": "General / Unreserved",
            "income": "Below ₹2.5 Lakhs / year"
        }
        res_gen = evaluate_profile_eligibility(
            "Scholarship Notice",
            self.scholarship_eligibility,
            profile_gen,
            self.scholarship_doc
        )
        cat_row = next(c for c in res_gen["criteria_breakdown"] if "Category" in c["criterion"])
        self.assertEqual(cat_row["verdict_color"], "red")
        self.assertIn("Category Mismatch", cat_row["verdict_badge"])
        print("PASS: Reservation category mismatch correctly evaluated.")

    def test_rental_agreement_not_applicable(self):
        """Tenancy contracts must return applicable=False."""
        rental_eligibility = SAMPLE_ANALYSES["PG / Rental Agreement (Sample)"]["eligibility"]
        res = evaluate_profile_eligibility(
            "PG / Rental Agreement",
            rental_eligibility,
            {"course": "B.Tech", "year": "1st Year", "state": "Delhi", "category": "General", "income": "Above 8L"},
            self.rental_doc
        )
        self.assertFalse(res["applicable"])
        self.assertEqual(res["status_color"], "gray")
        self.assertEqual(res["overall_status"], "Not Applicable")
        print("PASS: Rental agreement properly bypassed with 'Not Applicable' status.")

    def test_mock_analyzer_includes_eligibility(self):
        """Mock analyzer must return eligibility structure for all documents."""
        m_scholarship = mock_analyze_document(self.scholarship_doc)
        self.assertIn("eligibility", m_scholarship["data"])
        self.assertTrue(m_scholarship["data"]["eligibility"]["applicable"])
        self.assertGreaterEqual(len(m_scholarship["data"]["eligibility"]["criteria_list"]), 2)

        m_rental = mock_analyze_document(self.rental_doc)
        self.assertIn("eligibility", m_rental["data"])
        self.assertFalse(m_rental["data"]["eligibility"]["applicable"])
        print("PASS: Mock analyzer populates document eligibility structures cleanly.")


class TestStreamlitAppTestPhase5(unittest.TestCase):
    def test_streamlit_ui_phase5_eligibility_rendering(self):
        """Test Streamlit AppTest renders Phase 5 personalized eligibility tab and dynamic updates."""
        from streamlit.testing.v1 import AppTest

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)

        # Switch to Sample Presets (at.radio[0])
        at.radio[0].set_value("📚 Try Sample Presets")
        at.run()
        self.assertFalse(at.exception)

        # Select Scholarship Notice (selectbox[2] in main or sidebar)
        # Find the sample selector
        sample_sb = None
        for sb in at.selectbox:
            if "Scholarship Notice (Sample)" in sb.options:
                sample_sb = sb
                break
        self.assertIsNotNone(sample_sb)
        sample_sb.set_value("Scholarship Notice (Sample)")
        at.run()
        self.assertFalse(at.exception)

        # Verify Phase 5 badge and eligibility headers rendered
        html_content = "".join([m.value for m in at.markdown])
        self.assertTrue("PHASE 5 ACTIVE" in html_content or "PHASE 6 ACTIVE" in html_content)
        self.assertIn("Evaluating Stated Criteria Against Your Profile", html_content)
        self.assertIn("Clause-by-Clause Criterion Breakdown", html_content)
        self.assertIn("Domicile State", html_content)
        self.assertIn("Tahsildar", html_content)

        # Dynamic profile test: change domicile state to Delhi in sidebar
        state_sb = None
        for sb in at.sidebar.selectbox:
            if "Permanent Domicile (State)" in sb.label:
                state_sb = sb
                break
        self.assertIsNotNone(state_sb)
        state_sb.set_value("Delhi")
        at.run()
        self.assertFalse(at.exception)

        html_after_delhi = "".join([m.value for m in at.markdown])
        self.assertIn("State Mismatch", html_after_delhi)
        print("PASS: Streamlit UI renders Phase 5 personalized eligibility cards and responds dynamically to sidebar profile changes.")


if __name__ == "__main__":
    print("=" * 60)
    print("Running DocGist Phase 5 Automated Test Suite")
    print("=" * 60)
    unittest.main(verbosity=1)
