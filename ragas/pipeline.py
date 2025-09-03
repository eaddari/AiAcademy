import json
import os
from pathlib import Path
from typing import Dict, Any, List

from evaluator import RAGAS, EvaluationResult


class EvaluationPipeline:
    
    def __init__(self):
        print("Initializing RAGAS evaluator...")
        self.evaluator = RAGAS()
        print("RAGAS evaluator initialized.")
        # Use absolute path to ensure correct file location
        self.dataset_path = Path(__file__).parent / "eval_dataset.json"
        print(f"Dataset path: {self.dataset_path}")
    
    def load_eval_dataset(self) -> List[Dict[str, Any]]:
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_evaluation(self) -> EvaluationResult:
        print("Loading evaluation dataset...")
        dataset = self.load_eval_dataset()
        print(f"Loaded {len(dataset)} evaluation questions.")
        print("Starting RAG pipeline evaluation...")
        return self.evaluator.evaluate_rag_pipeline(dataset)
    
    def save_results(self, results: EvaluationResult, output_path: str = None):
        if output_path is None:
            # Fix the path - save in the current ragas directory
            output_dir = Path(__file__).parent
            output_path = output_dir / "ragas_evaluation_results.json"
        
        print(f"Saving results to: {output_path}")
        
        results_dict = {
            "faithfulness": results.faithfulness,
            "answer_relevancy": results.answer_relevancy,
            "context_precision": results.context_precision,
            "context_recall": results.context_recall,
            "answer_similarity": results.answer_similarity,
            "answer_correctness": results.answer_correctness,
            "overall_score": results.overall_score
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results_dict, f, indent=2, ensure_ascii=False)
            print(f"Results successfully saved to: {output_path}")
        except Exception as e:
            print(f"Error saving results: {e}")