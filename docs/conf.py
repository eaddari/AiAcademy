# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document) are in another directory,
# add these directories to sys.path here.
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
project = 'Esercizio Esteso - CrewAI Multi-Agent System'
copyright = '2025, AI Academy Group'
author = 'AI Academy Group'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'autoapi.extension',
    'myst_parser',
]

# AutoAPI configuration
autoapi_dirs = ['../src']
autoapi_type = 'python'
autoapi_file_patterns = ['*.py']
autoapi_generate_api_docs = True
autoapi_add_toctree_entry = False
autoapi_member_order = 'groupwise'
autoapi_ignore = [
    '**/flow_copy.py',  # Exclude due to syntax/encoding issues
    '**/__pycache__/**',
]
autoapi_options = [
    'members',
    'show-inheritance',
    'show-module-summary',
]
# Removed 'undoc-members' and 'special-members' to reduce duplicates
autoapi_keep_files = False  # Don't keep generated files to avoid conflicts
autoapi_python_class_content = 'class'  # Only show class docstring, not __init__

# Suppress duplicate object warnings
suppress_warnings = [
    'autoapi.duplicate_object',
    'toc.not_included',
    'autoapi.python_domain',
    'docutils',
    'autoapi',
    'autosectionlabel.*',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '__pycache__']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Todo extension
todo_include_todos = True

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# MyST Parser configuration
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_admonition",
    "html_image",
]

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'exclude-members': '__weakref__'
}
# Removed 'special-members' and 'undoc-members' to reduce conflicts

# Add custom CSS
html_css_files = [
    'custom.css',
]

# Custom AutoAPI event handlers to prevent duplicates
def skip_duplicate_members(app, what, name, obj, skip, options):
    """Skip duplicate members that cause warnings."""
    if skip:
        return True
    
    # Skip common tool properties that cause duplicates
    if what == 'attribute' and name.split('.')[-1] in ['args_schema', 'description', 'name']:
        return True
    
    # Skip properties that are also defined as methods to prevent duplicates
    if what == 'method' and hasattr(obj, '__annotations__'):
        return True
    
    return False

def setup(app):
    app.connect('autoapi-skip-member', skip_duplicate_members)
