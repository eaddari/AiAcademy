"""
Custom Tools package for CrewAI Multi-Agent System.

This package provides custom tools that extend the capabilities of CrewAI
agents, including local RAG functionality, mathematical computation tools,
and vision-based image generation capabilities.

Modules
-------
custom_tool : module
    Core custom tools including LocalRag and MathEquationsTool.
vision_tools : module
    Vision and image generation tools using DALL-E integration.

Classes
-------
LocalRag : BaseTool
    Tool for local Retrieval-Augmented Generation using FAISS.
MathEquationsTool : BaseTool  
    Tool for solving mathematical equations and calculations.
DallETool : BaseTool
    Tool for generating images from textual descriptions.

Examples
--------
Using the LocalRag tool:
    >>> from esercizio_esteso.tools.custom_tool import LocalRag
    >>> rag_tool = LocalRag()
    >>> result = rag_tool._run("What is machine learning?")

Using the MathEquationsTool:
    >>> from esercizio_esteso.tools.custom_tool import MathEquationsTool
    >>> math_tool = MathEquationsTool()
    >>> result = math_tool._run("Solve: 2x + 5 = 15")

Notes
-----
All tools require proper environment configuration and API access
for full functionality. See individual tool documentation for
specific requirements and usage patterns.
"""

# Import main tool classes for easier access
try:
    from .custom_tool import LocalRag, MathEquationsTool
    from .vision_tools import DallETool
except ImportError:
    # Handle cases where some tools might not be available
    pass

__all__ = [
    'LocalRag',
    'MathEquationsTool', 
    'DallETool'
]