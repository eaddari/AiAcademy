import os
from typing import Type, Union, Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, field_validator

from src.rag.qdrant_rag import (
    SETTINGS, get_llm, simulate_corpus, split_documents, get_qdrant_client,
    recreate_collection_for_rag, upsert_chunks, hybrid_search, 
    format_docs_for_prompt, build_rag_chain
)
from langchain_openai import AzureOpenAIEmbeddings


class QdrantRAGInput(BaseModel):
    query: Union[str, dict] = Field(..., description="The question or query to search for in the knowledge base.")
    
    @field_validator('query', mode='before')
    @classmethod
    def validate_query(cls, v) -> str:
        if isinstance(v, dict):
            # Extract query from dict if it's in 'description' or 'query' key
            if 'query' in v:
                return str(v['query'])
            elif 'description' in v:
                return str(v['description'])
            else:
                raise ValueError("Dictionary input must contain 'query' or 'description' key")
        elif isinstance(v, str):
            return v
        else:
            return str(v)  # Convert other types to string


class QdrantRAGTool(BaseTool):
    name: str = "qdrant_rag_search"
    description: str = (
        "Search medical knowledge base using RAG with Qdrant vector database. "
        "Answers medical questions with source citations."
    )
    args_schema: Type[BaseModel] = QdrantRAGInput
    
    def __init__(self):
        super().__init__()
        self._initialized = False
        self._chain = None  # Initialize _chain to None
    
    def _initialize_rag_system(self):
        if self._initialized:
            return
            
        self._embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            model="text-embedding-ada-002"
        )
        
        self._llm = get_llm(SETTINGS)
        self._client = get_qdrant_client(SETTINGS)
        
        try:
            collection_info = self._client.get_collection(SETTINGS.collection)
            if collection_info.points_count == 0:
                self._setup_knowledge_base()
        except Exception:
            self._setup_knowledge_base()
        
        if self._llm:
            self._chain = build_rag_chain(self._llm)
        else:
            self._chain = None  # Ensure _chain is set even if LLM fails
        
        self._initialized = True
    
    def _setup_knowledge_base(self):
        documents = simulate_corpus()
        chunks = split_documents(documents, SETTINGS)
        
        sample_embedding = self._embeddings.embed_query("test")
        vector_size = len(sample_embedding)
        
        recreate_collection_for_rag(self._client, SETTINGS, vector_size)
        upsert_chunks(self._client, SETTINGS, chunks, self._embeddings)

    def _run(self, query: str) -> str:
        # Skip empty queries
        if not query or not query.strip():
            return "Error: Query cannot be empty."
        
        self._initialize_rag_system()
        
        retrieved_points = hybrid_search(self._client, SETTINGS, query, self._embeddings)
        
        if not retrieved_points:
            return "No relevant information found."
        
        context = format_docs_for_prompt(retrieved_points)
        
        if self._chain:
            return self._chain.invoke({"context": context, "question": query})
        
        return f"Retrieved context:\n\n{context}"
