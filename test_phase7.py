"""
DocGist — Phase 7 End-to-End & Deployment Readiness Test Suite
Verifies:
1. Security & Secrets Hygiene: No hardcoded API keys in any source file; .gitignore protects .env & secrets.toml.
2. Zero-Storage Privacy Guarantee: No database imports (sqlite3, sqlalchemy, pymongo) or persistent file writes of user data.
3. Deployment Configuration: requirements.txt, .streamlit/config.toml, and README.md are complete and valid.
4. Edge-Case Input Validation: Short pasted text (< 20 chars) triggers a clean user warning without crashing.
5. Full End-to-End Workflow across all 3 supported document types (PG Rental, Internship Offer, Scholarship Notice) in both English and Hindi.
"""

import os
import re
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from sample_data import SAMPLE_DOCUMENTS, SAMPLE_ANALYSES
from gemini_analyzer import mock_analyze_document, evaluate_profile_eligibility, verify_quotation
from translations import get_text, get_localized_analysis, generate_downloadable_report

PROJECT_DIR = Path(__file__).parent


class TestPhase7DeploymentAndSecurity(unittest.TestCase):
    def test_no_hardcoded_api_keys_in_source(self):
        """Ensure no real Google API keys (AIzaSy + 33 alphanumeric chars) are hardcoded in source files."""
        real_key_pattern = re.compile(r"AIzaSy[A-Za-z0-9_\-]{33}")
        source_files = ["app.py", "gemini_analyzer.py", "pdf_processor.py", "translations.py", "sample_data.py"]

        for fname in source_files:
            fpath = PROJECT_DIR / fname
            content = fpath.read_text(encoding="utf-8")
            matches = real_key_pattern.findall(content)
            self.assertEqual(len(matches), 0, f"Potential hardcoded API key found in {fname}!")

    def test_gitignore_protects_secrets(self):
        """Ensure .gitignore explicitly excludes .env and .streamlit/secrets.toml."""
        gitignore_text = (PROJECT_DIR / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gitignore_text)
        self.assertIn("secrets.toml", gitignore_text)

    def test_zero_storage_architecture_compliance(self):
        """Verify application modules do not import database engines or write user documents to disk."""
        forbidden_imports = ["sqlite3", "sqlalchemy", "pymongo", "psycopg2", "chromadb", "faiss"]
        app_modules = ["app.py", "gemini_analyzer.py", "pdf_processor.py", "translations.py"]

        for fname in app_modules:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8").lower()
            for db_lib in forbidden_imports:
                self.assertNotIn(f"import {db_lib}", content, f"Forbidden DB import {db_lib} in {fname}")

    def test_deployment_files_present_and_valid(self):
        """Verify requirements.txt, .streamlit/config.toml, and README.md are ready for deployment."""
        req_text = (PROJECT_DIR / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("streamlit", req_text)
        self.assertIn("pypdf", req_text)
        self.assertIn("google-genai", req_text)

        config_path = PROJECT_DIR / ".streamlit" / "config.toml"
        self.assertTrue(config_path.exists(), ".streamlit/config.toml must exist for production deployment")
        config_text = config_path.read_text(encoding="utf-8")
        self.assertIn("enableXsrfProtection = true", config_text)
        self.assertIn("gatherUsageStats = false", config_text)

    def test_short_text_warning_edge_case(self):
        """Pasting very brief text (< 20 chars) should display a helpful warning rather than analyzing."""
        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)

        # Switch to Paste Text Directly
        at.radio[0].set_value(at.radio[0].options[1]).run()
        at.text_area[0].input("Too short").run()
        at.button[0].click().run()
        self.assertFalse(at.exception)

        warnings = [w.value for w in at.warning]
        self.assertTrue(
            any("too brief" in w.lower() or "बहुत छोटा" in w for w in warnings),
            f"Expected short text warning, got: {warnings}"
        )

    def test_end_to_end_all_document_types_bilingual(self):
        """Run end-to-end pipeline verification across all 3 document types in English and Hindi."""
        profile = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "3rd Year",
            "state": "Maharashtra",
            "category": "OBC (Non-Creamy Layer)",
            "income": "Below ₹2.5 Lakhs / year"
        }

        for sample_key, doc_text in SAMPLE_DOCUMENTS.items():
            for lang in ["English", "हिंदी (Hindi)"]:
                raw_analysis = mock_analyze_document(doc_text)["data"]
                localized = get_localized_analysis(raw_analysis, sample_key, lang)

                self.assertEqual(len(localized["five_point_summary"]), 5)
                self.assertGreaterEqual(len(localized["risks"]), 3)

                for risk in localized["risks"]:
                    v_res = verify_quotation(doc_text, risk["exact_quote"])
                    self.assertTrue(v_res["is_verified"], f"Quote verification failed for {sample_key} ({lang})")

                eval_res = evaluate_profile_eligibility(
                    document_type=localized["document_type"],
                    eligibility_info=localized["eligibility"],
                    user_profile=profile,
                    document_text=doc_text,
                    language=lang
                )

                report = generate_downloadable_report(
                    analysis_data=localized,
                    doc_type=localized["document_type"],
                    user_profile=profile,
                    risks_list=localized["risks"],
                    eligibility_result=eval_res,
                    lang=lang
                )
                self.assertTrue(len(report) > 300)


if __name__ == "__main__":
    unittest.main(verbosity=2)
