"""
DocGist — Phase 6 Automated Test Suite
Verifies:
1. Bilingual Internationalization (English and Hindi catalogs in translations.py)
2. Safe string retrieval via get_text() for both languages
3. Localized preset analyses (get_localized_analysis) preserving verbatim quotations for anti-hallucination verification
4. Bilingual exportable Markdown report generation (generate_downloadable_report)
5. Streamlit AppTest verification of language switching, Hindi UI rendering, and report download button
"""

import unittest
from sample_data import SAMPLE_DOCUMENTS, SAMPLE_ANALYSES
from translations import (
    UI_STRINGS,
    HINDI_SAMPLE_ANALYSES,
    get_text,
    get_localized_analysis,
    generate_downloadable_report
)
from gemini_analyzer import verify_quotation, evaluate_profile_eligibility


class TestPhase6Translations(unittest.TestCase):
    def test_ui_strings_catalog_completeness(self):
        """Ensure all required translation keys exist in both English and Hindi."""
        en_keys = set(UI_STRINGS["English"].keys())
        hi_keys = set(UI_STRINGS["हिंदी (Hindi)"].keys())
        
        self.assertTrue(len(en_keys) >= 40, f"Expected at least 40 UI keys, found {len(en_keys)}")
        # Every English key must have a Hindi equivalent
        missing_in_hindi = en_keys - hi_keys
        self.assertEqual(len(missing_in_hindi), 0, f"Missing Hindi translations for: {missing_in_hindi}")

    def test_get_text_fallback_behavior(self):
        """get_text should return correct translations or graceful fallbacks."""
        self.assertEqual(get_text("app_title", "English"), "DocGist — Understand Before You Sign")
        self.assertIn("डॉकगिस्ट", get_text("app_title", "हिंदी (Hindi)"))
        
        # Non-existent key should return key itself
        self.assertEqual(get_text("unknown_key_xyz", "English"), "unknown_key_xyz")
        # Unknown language should default to English
        self.assertEqual(get_text("analyze_btn", "French"), "🔍 Analyze Document")

    def test_hindi_sample_analyses_preserves_verbatim_quotes(self):
        """
        Critical Anti-Hallucination Guardrail:
        Hindi sample analyses must translate titles and explanations into Hindi,
        while strictly preserving original English exact_quote fields so programmatic
        quotation verification remains 100% accurate.
        """
        for sample_key in ["PG / Rental Agreement (Sample)", "Internship Offer Letter (Sample)", "Scholarship Notice (Sample)"]:
            hi_analysis = HINDI_SAMPLE_ANALYSES[sample_key]
            orig_doc = SAMPLE_DOCUMENTS[sample_key]
            
            # Check 5-point summary is in Hindi
            self.assertEqual(len(hi_analysis["five_point_summary"]), 5)
            
            # Check every risk quote against original document text
            for risk in hi_analysis["risks"]:
                quote = risk["exact_quote"]
                v_res = verify_quotation(orig_doc, quote)
                self.assertTrue(
                    v_res["is_verified"],
                    f"Hindi preset quote failed verification: '{quote}'"
                )
                self.assertEqual(v_res["badge_color"], "green")

    def test_get_localized_analysis_integration(self):
        """get_localized_analysis returns Hindi dictionary when requested, and passes through in English."""
        mock_data = {"document_type": "Original"}
        key = "PG / Rental Agreement (Sample)"
        
        # English: should return original dict unchanged
        en_res = get_localized_analysis(mock_data, key, "English")
        self.assertEqual(en_res["document_type"], "Original")
        
        # Hindi: should return rich Hindi preset
        hi_res = get_localized_analysis(mock_data, key, "हिंदी (Hindi)")
        self.assertIn("किराया", hi_res["document_type"])
        self.assertEqual(len(hi_res["five_point_summary"]), 5)

    def test_generate_downloadable_report_bilingual(self):
        """Test Markdown report generation in both English and Hindi."""
        sample_key = "Scholarship Notice (Sample)"
        sample_doc = SAMPLE_DOCUMENTS[sample_key]
        sample_analysis = SAMPLE_ANALYSES[sample_key]
        profile = {
            "course": "B.Tech / B.E. (Engineering)",
            "year": "3rd Year",
            "state": "Maharashtra",
            "category": "OBC (Non-Creamy Layer)",
            "income": "Below ₹2.5 Lakhs / year"
        }
        eval_res = evaluate_profile_eligibility(
            "Scholarship Notice",
            sample_analysis["eligibility"],
            profile,
            sample_doc,
            language="English"
        )
        
        # English report
        en_md = generate_downloadable_report(
            sample_analysis,
            "Scholarship Notice",
            profile,
            sample_analysis["risks"],
            eval_res,
            lang="English"
        )
        self.assertIn("# DocGist — Document Analysis Report", en_md)
        self.assertIn("Important Legal Disclaimer", en_md)
        self.assertIn("5-Point Executive Summary", en_md)
        self.assertIn("Evidence-Based Risk Evaluation", en_md)
        self.assertIn("Profile Eligibility Evaluation", en_md)
        self.assertIn("Eligible", en_md)

        # Hindi report
        eval_res_hi = evaluate_profile_eligibility(
            "छात्रवृत्ति अधिसूचना",
            HINDI_SAMPLE_ANALYSES[sample_key]["eligibility"],
            profile,
            sample_doc,
            language="हिंदी (Hindi)"
        )
        hi_md = generate_downloadable_report(
            HINDI_SAMPLE_ANALYSES[sample_key],
            "छात्रवृत्ति अधिसूचना",
            profile,
            HINDI_SAMPLE_ANALYSES[sample_key]["risks"],
            eval_res_hi,
            lang="हिंदी (Hindi)"
        )
        self.assertIn("# DocGist (डॉकगिस्ट) — दस्तावेज़ विश्लेषण रिपोर्ट", hi_md)
        self.assertIn("कानूनी अस्वीकरण (Disclaimer)", hi_md)
        self.assertIn("5-पॉइंट मुख्य सारांश", hi_md)
        self.assertIn("जोखिम एवं खंड मूल्यांकन", hi_md)
        self.assertIn("प्रोफ़ाइल पात्रता जाँच", hi_md)


class TestStreamlitAppTestPhase6(unittest.TestCase):
    def test_streamlit_ui_language_toggle_and_hindi_rendering(self):
        """Test toggling language in Streamlit sidebar re-renders the whole interface in Hindi."""
        from streamlit.testing.v1 import AppTest

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()
        self.assertFalse(at.exception)

        # Find the language radio in sidebar
        lang_radio = None
        for r in at.sidebar.radio:
            if "Display Language" in r.label:
                lang_radio = r
                break
        self.assertIsNotNone(lang_radio, "Display Language radio not found in sidebar")
        self.assertEqual(lang_radio.value, "English")

        # Verify English title is rendered initially
        html_en = "".join([m.value for m in at.markdown])
        self.assertIn("DocGist — Understand Before You Sign", html_en)

        # Toggle to Hindi
        lang_radio.set_value("हिंदी (Hindi)")
        at.run()
        self.assertFalse(at.exception)

        # Verify Hindi title, badge, disclaimer, and footer rendered
        html_hi = "".join([m.value for m in at.markdown])
        self.assertIn("DocGist (डॉकगिस्ट)", html_hi)
        self.assertIn("हस्ताक्षर करने से पहले समझें", html_hi)
        self.assertIn("कानूनी अस्वीकरण", html_hi)
        self.assertIn("गोपनीयता एवं डेटा सुरक्षा", html_hi)
        print("PASS: Streamlit language toggle seamlessly converts UI between English and Hindi.")

    def test_streamlit_ui_hindi_sample_analysis_and_report_download(self):
        """Test analyzing a sample preset in Hindi renders Hindi tabs, metrics, and download report button."""
        from streamlit.testing.v1 import AppTest

        at = AppTest.from_file("app.py", default_timeout=30)
        at.run()

        # Switch to Hindi
        for r in at.sidebar.radio:
            if "Display Language" in r.label:
                r.set_value("हिंदी (Hindi)")
                break
        at.run()
        self.assertFalse(at.exception)

        # Switch to Sample Presets (at.radio[0])
        preset_opt_hi = get_text("input_presets", "हिंदी (Hindi)")
        at.radio[0].set_value(preset_opt_hi)
        at.run()
        self.assertFalse(at.exception)

        # Select Internship Offer Letter
        sample_sb = None
        for sb in at.selectbox:
            if "Internship Offer Letter (Sample)" in sb.options:
                sample_sb = sb
                break
        self.assertIsNotNone(sample_sb)
        sample_sb.set_value("Internship Offer Letter (Sample)")
        at.run()
        self.assertFalse(at.exception)

        # Verify Hindi tabs, metrics, and risk descriptions rendered
        html_analysis = "".join([m.value for m in at.markdown])
        self.assertIn("खंड-दर-खंड साक्ष्य-आधारित जोखिम मूल्यांकन", html_analysis)
        self.assertIn("गैर-प्रतिस्पर्धा", html_analysis)

        # Verify Download Report button rendered
        dl_buttons = at.get("download_button")
        self.assertGreaterEqual(len(dl_buttons), 1, "Download button not found")
        print("PASS: Hindi sample analysis and report download button verified in Streamlit AppTest.")


if __name__ == "__main__":
    print("=" * 60)
    print("Running DocGist Phase 6 Automated Test Suite")
    print("=" * 60)
    unittest.main(verbosity=1)
