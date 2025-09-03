"""
Summarization Crew package.

This package contains the SummarizationCrew implementation for document
summarization and content condensation tasks.

Classes
-------
SummarizationCrew : class
    Main crew class for document summarization operations.

Notes
-----
The summarization crew specializes in analyzing documents and creating
concise, meaningful summaries while preserving key information and context.
"""

# Import the main crew class
try:
    from .summarization_crew import SummarizationCrew
except ImportError:
    # Handle import errors gracefully
    pass

__all__ = ['SummarizationCrew']
