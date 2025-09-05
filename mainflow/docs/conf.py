# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# Mock external dependencies that we don't need for documentation
import sys
from unittest.mock import MagicMock

class MockModule(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

# Mock crewai and its submodules
sys.modules['crewai'] = MockModule()
sys.modules['crewai.project'] = MockModule()
sys.modules['crewai.agents'] = MockModule()
sys.modules['crewai.agents.agent_builder'] = MockModule()
sys.modules['crewai.agents.agent_builder.base_agent'] = MockModule()

# Configure the basic project information
project = 'EY Junior Accelerator'
copyright = '2025, Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'
author = 'Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'
release = 'v1'
copyright = '2025, Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'
author = 'Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'
release = 'v1'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

# Napoleon settings for numpy-style docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'show-inheritance': True,
}

# Templates and static files
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
