"""
Esercizio Esteso - CrewAI Multi-Agent System.

This package implements a comprehensive multi-agent system using CrewAI for
automated documentation generation, research workflows, and intelligent content
creation. The system coordinates multiple specialized AI crews to handle
different aspects of information gathering, analysis, and synthesis.

Key Features
------------
- Multi-agent workflows with intelligent routing
- RAG-based document research and analysis
- Mathematical problem solving capabilities
- Web research and information gathering
- Document generation and synthesis
- OCR and image processing
- Comprehensive reporting and visualization

Modules
-------
crews : package
    Specialized AI crews for different domains and tasks.
tools : package
    Custom tools and utilities for enhanced agent capabilities.
flow_copy : module
    Generic research flow with intelligent routing.
flow_documentation : module
    Documentation-specific workflow implementation.
main : module
    Main entry point for the application.

Examples
--------
Run the documentation flow:
    >>> from esercizio_esteso import main
    >>> main.run_flow()

Generate flow visualization:
    >>> main.plot_flow()

Notes
-----
The system requires proper Azure OpenAI configuration and depends on
various Python packages for full functionality. See the README.md
for detailed setup instructions.
"""

from .main import run_flow, plot_flow

__version__ = "0.1.0"
__author__ = "AI Academy Group"

__all__ = [
    'run_flow',
    'plot_flow',
]