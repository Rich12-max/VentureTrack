"""
Tests for Streamlit App and All 10 Views via Streamlit AppTest
"""
import pytest
from streamlit.testing.v1 import AppTest
from app import NAV_PAGES


@pytest.mark.parametrize("page_name", NAV_PAGES)
def test_all_pages_render_without_exception(page_name):
    """
    Simulates navigating to each of the 10 application views and asserts
    that each page renders with zero uncaught exceptions.
    """
    at = AppTest.from_file("app.py")
    at.run(timeout=10)
    
    # Switch page via sidebar radio
    at.sidebar.radio[0].set_value(page_name)
    at.run(timeout=10)
    
    assert len(at.exception) == 0, f"Page '{page_name}' threw exceptions: {at.exception}"

