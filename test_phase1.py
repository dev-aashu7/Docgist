"""
Automated unit test for DocGist Phase 1 functionality.
Uses Streamlit's official AppTest framework to verify rendering and preset analyses.
"""

from streamlit.testing.v1 import AppTest

def test_app_loads_without_exceptions():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    assert not at.exception, f"App crashed with exceptions: {at.exception}"
    print("PASS: App initialized and rendered initial view successfully.")

def test_sample_rental_selection():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    
    # Switch to presets
    at.radio[0].set_value(at.radio[0].options[2]).run()
    at.button[0].click().run()
    
    assert not at.exception, f"Crash on selecting rental: {at.exception}"
    print("PASS: Rental Agreement sample loaded and analyzed cleanly.")

def test_analyze_button_interaction():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    
    at.radio[0].set_value(at.radio[0].options[2]).run()
    at.button[0].click().run()
    assert not at.exception, f"Crash on clicking analyze: {at.exception}"
    print("PASS: Analyze button clicked and executed cleanly.")

if __name__ == "__main__":
    print("Running automated tests for DocGist Phase 1...")
    test_app_loads_without_exceptions()
    test_sample_rental_selection()
    test_analyze_button_interaction()
    print("\nALL PHASE 1 TESTS PASSED SUCCESSFULLY!")
