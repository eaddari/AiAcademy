import os
from typing import List, Dict, Any
from dataclasses import dataclass

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_similarity,
    answer_correctness
)
from datasets import Dataset
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

from src.esercizio_esteso.tools.rag_tool import RetrievalTool


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
        self.retrieval_tool = RetrievalTool()
        self.llm = self._get_llm()
        self.embeddings = self._get_embeddings()
        
    def get_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4"),
            temperature=0
        )
    
    def get_embeddings(self) -> AzureOpenAIEmbeddings:
        return AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            model="text-embedding-ada-002"
        )
    
    def evaluate_rag_pipeline(
        self, 
        test_dataset: List[Dict[str, Any]]
    ) -> EvaluationResult:

        evaluation_data = []
        
        for item in test_dataset:
            question = item["question"]
            ground_truth = item["ground_truth"]
            
            retrieved_contexts = self.retrieval_tool._run(question)
            contexts = [i for i in retrieved_contexts.split('\n\n') if i.strip()]
            
            prompt = f"Contesto: {retrieved_contexts}\n\nDomanda: {question}\n\nRisposta:"
            answer = self.llm.invoke(prompt).content
            
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
            embeddings=self.embeddings
        )
        
        scores = result.to_pandas()
        overall_score = scores.mean().mean()
        
        return EvaluationResult(
            faithfulness=scores['faithfulness'].mean(),
            answer_relevancy=scores['answer_relevancy'].mean(),
            context_precision=scores['context_precision'].mean(),
            context_recall=scores['context_recall'].mean(),
            answer_similarity=scores['answer_similarity'].mean(),
            answer_correctness=scores['answer_correctness'].mean(),
            overall_score=overall_score
        )