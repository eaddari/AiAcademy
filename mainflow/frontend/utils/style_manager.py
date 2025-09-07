import streamlit as st
from pathlib import Path


def load_css(file_path: str) -> str:
    """Load CSS from a file and return it as a string"""
    css_file_path = Path(__file__).parent.parent / "styles" / file_path
    try:
        with open(css_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")
        return ""
    except Exception as e:
        st.error(f"Error loading CSS file: {e}")
        return ""


def apply_custom_styles(css_file: str = "main.css"):
    """Apply custom CSS styles to the Streamlit app"""
    css_content = load_css(css_file)
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def apply_theme(theme_name: str = "default"):
    """Apply a specific theme to the app"""
    theme_map = {
        "default": "main.css",
        "dark": "main.css",  # You can add more themes here
        # "light": "light.css",
        # "blue": "blue.css",
    }
    
    css_file = theme_map.get(theme_name, "main.css")
    apply_custom_styles(css_file)
