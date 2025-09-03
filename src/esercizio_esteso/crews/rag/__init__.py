"""
RAG (Retrieval-Augmented Generation) utilities package.

This package provides tools and utilities for implementing local RAG
functionality using FAISS vector database and Azure OpenAI embeddings.

Modules
-------
faiss_rag : module
    Core FAISS-based RAG implementation with vector search and retrieval.

Notes
-----
The RAG system enables semantic search over local document collections,
providing context-aware responses by combining retrieved information
with language model generation capabilities.

The docs/ subdirectory contains example documents that can be indexed
and searched using the RAG system.
"""

# Import main RAG functions if available
try:
    from .faiss_rag import *
except ImportError:
    # Handle cases where faiss_rag might not be available
    pass
