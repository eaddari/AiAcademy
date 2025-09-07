# Frontend Structure

This directory contains all frontend-related assets for the Streamlit application.

## Directory Structure

```
frontend/
├── __init__.py                 # Package initialization
├── styles/                     # CSS stylesheets
│   └── main.css               # Main application styles (dark theme with gold accents)
└── utils/                     # Frontend utility functions
    ├── __init__.py            # Utils package initialization
    └── style_manager.py       # Style loading and management utilities
```

## Color Scheme

The main theme uses:
- **Background**: `#1a1a24` (dark black)
- **Text**: `#f9f9f9` (snow white)  
- **Accents**: `#ffe600` (gold)

## Usage

From the main application:

```python
from frontend.utils.style_manager import apply_custom_styles

# Apply default styles
apply_custom_styles()

# Or apply a specific theme
apply_theme("dark")
```

## Adding New Themes

1. Create a new CSS file in `styles/` directory (e.g., `light.css`)
2. Update the `theme_map` in `style_manager.py`
3. Use `apply_theme("your_theme_name")` in your app

## CSS Organization

The CSS is organized into logical sections:
- App background and layout
- Typography (titles, headers, text)
- Form elements (inputs, buttons)
- Interactive components (tabs, expanders)
- Status messages (success, error, warning)
- Special components (progress bars, spinners)

Each section is clearly commented for easy maintenance.
