# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))
# Also add the parent directory to handle 'src.mainflow' imports
sys.path.insert(0, os.path.abspath('..'))

# Mock external dependencies that we don't need for documentation
import sys
from unittest.mock import MagicMock

class MockModule(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


# Mock all CrewAI modules and submodules
crewai_modules = [
    'crewai',
    'crewai.flow',
    'crewai.tools',
    'crewai.project',
    'crewai.agents',
    'crewai.agents.agent_builder',
    'crewai.agents.agent_builder.base_agent',
    'crewai.crew',
    'crewai.task',
    'crewai.agent',
]

for module in crewai_modules:
    sys.modules[module] = MockModule()

# Configure the basic project information
project = 'EY Junior Accelerator'
copyright = '2025, Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'
author = 'Emanuele Addari, Michele Bruno, Anna Setzu, Giosue Sglavo'


# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]


napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False


autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'show-inheritance': True,
}

autodoc_typehints = 'both'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
