"""
Crews package for Esercizio Esteso CrewAI Multi-Agent System.

This package contains all the specialized AI crews that work together to handle
different aspects of the documentation generation and research workflow.

Modules
-------
docgen : module
    Document generation crew for creating structured documentation.
mathcrew : module
    Mathematical problem solving crew with specialized calculation tools.
ocr_crew : module
    Optical Character Recognition and image processing crew.
rag : module
    Retrieval-Augmented Generation tools and utilities.
summarization_crew : module
    Document summarization and content condensation crew.
summary : module
    Summary and explanation crew for comprehensive topic coverage.
webrag : module
    Web research and RAG-enabled information gathering crew.
crew_local_saver : module
    Local file saving and persistence utilities for crew operations.

Notes
-----
Each crew is designed as a specialized unit with specific agents, tasks, and
tools tailored to their domain of expertise. The crews can work independently
or be orchestrated together through the flow system.
"""

# Import main crew classes for easier access
try:
    from .docgen.crew import Docgen
    from .mathcrew.crew import Math
    from .summary.crew import ExplanationCrew
    from .webrag.crew import Webrag
    from .summarization_crew.summarization_crew import SummarizationCrew
except ImportError:
    # Handle cases where some crews might not be available
    pass

__all__ = [
    'Docgen',
    'Math', 
    'ExplanationCrew',
    'Webrag',
    'SummarizationCrew'
]
