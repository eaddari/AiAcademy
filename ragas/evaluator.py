import os
from typing import List, Dict, Any
from dataclasses import dataclass
import pandas as pd

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_similarity,
    answer_correctness
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.qdrant_rag import (
    SETTINGS, get_embeddings, get_qdrant_client, simulate_corpus,
    split_documents, recreate_collection_for_rag, upsert_chunks, hybrid_search,
    format_docs_for_prompt, build_rag_chain   # <<< AGGIUNTO
)


@dataclass
class EvaluationResult:
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float
    answer_similarity: float
    answer_correctness: float
    overall_score: float


class RAGAS:
    
    def __init__(self):
        self.settings = SETTINGS
        self.embeddings = get_embeddings(self.settings)
        self.client = get_qdrant_client(self.settings)
        
        # Initialize Azure OpenAI LLM and Embeddings according to RAGAS documentation
        self.azure_llm = self.get_azure_llm()
        self.azure_embeddings = self.get_azure_embeddings()
        
        # Wrap with RAGAS wrappers
        self.llm = LangchainLLMWrapper(self.azure_llm)
        self.ragas_embeddings = LangchainEmbeddingsWrapper(self.azure_embeddings)
    
        docs = self.load_medical_docs()
        chunks = split_documents(docs, self.settings)
        vector_size = 1536
        recreate_collection_for_rag(self.client, self.settings, vector_size)
        upsert_chunks(self.client, self.settings, chunks, self.embeddings)
    
    def load_medical_docs(self):
        from pathlib import Path
        from langchain.schema import Document
        
        docs = []
        project_root = Path(__file__).parent.parent
        input_docs_path = project_root / "rag" / "input_docs"
        
        for file_path in input_docs_path.glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    docs.append(Document(page_content=content, metadata={"source": file_path.name}))
        return docs
        
    def get_azure_llm(self) -> AzureChatOpenAI:
        """Create Azure OpenAI LLM according to RAGAS documentation pattern"""
        return AzureChatOpenAI(
            openai_api_version=os.getenv("OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4.1"),
            model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4.1"),
            validate_base_url=False,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0
        )
    
    def get_azure_embeddings(self) -> AzureOpenAIEmbeddings:
        """Create Azure OpenAI Embeddings according to RAGAS documentation pattern"""
        return AzureOpenAIEmbeddings(
            openai_api_version=os.getenv("OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
            model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
    
    def evaluate_rag_pipeline(
        self, 
        test_dataset: List[Dict[str, Any]]
    ) -> EvaluationResult:

        evaluation_data = []
        
        for item in test_dataset:
            question = item["question"]
            ground_truth = item["ground_truth"]

            hits = hybrid_search(self.client, self.settings, question, self.embeddings)
            contexts = [hit.payload.get('text', '') for hit in hits]  # <- resta: serve a RAGAS

            # 1) crea il testo CONTENUTO con tag [source:...]
            context_str = format_docs_for_prompt(hits)

            # 2) costruisci la chain usando l'LLM Azure già creato in __init__
            gen_chain = build_rag_chain(self.azure_llm)

            # 3) genera la risposta fedele al CONTENUTO (fallback se vuoto)
            if context_str.strip():
                answer = gen_chain.invoke({"question": question, "context": context_str})
            else:
                answer = "Non ho trovato l'informazione nei documenti forniti."
            
            evaluation_data.append({
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "ground_truth": ground_truth
            })

        dataset = Dataset.from_list(evaluation_data)

        metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_similarity,
            answer_correctness
        ]
        
        result = evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=self.llm,
            embeddings=self.ragas_embeddings
        )
        
        scores = result.to_pandas()
        
        # Handle potential non-numeric values in the results
        numeric_scores = {}
        overall_scores = []
        
        # List of expected metric columns
        expected_metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 
                           'context_recall', 'answer_similarity', 'answer_correctness']
        
        for metric in expected_metrics:
            if metric in scores.columns:
                # Convert to numeric, replacing non-numeric values with NaN
                numeric_values = pd.to_numeric(scores[metric], errors='coerce')
                # Calculate mean, ignoring NaN values
                mean_score = numeric_values.mean()
                numeric_scores[metric] = mean_score if not pd.isna(mean_score) else 0.0
                
                if not pd.isna(mean_score):
                    overall_scores.append(mean_score)
            else:
                print(f"Warning: {metric} not found in results")
                numeric_scores[metric] = 0.0
        
        # Calculate overall score from successfully computed metrics
        overall_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
        
        print(f"\nEvaluation Results Summary:")
        for metric, score in numeric_scores.items():
            print(f"{metric}: {score:.4f}")
        print(f"Overall Score: {overall_score:.4f}")
        
        return EvaluationResult(
            faithfulness=numeric_scores.get('faithfulness', 0.0),
            answer_relevancy=numeric_scores.get('answer_relevancy', 0.0),
            context_precision=numeric_scores.get('context_precision', 0.0),
            context_recall=numeric_scores.get('context_recall', 0.0),
            answer_similarity=numeric_scores.get('answer_similarity', 0.0),
            answer_correctness=numeric_scores.get('answer_correctness', 0.0),
            overall_score=overall_score
        )