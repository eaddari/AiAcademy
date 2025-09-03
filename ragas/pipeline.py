import json
import os
from pathlib import Path
from typing import Dict, Any, List

from evaluator import RAGAS, EvaluationResult


class EvaluationPipeline:
    
    def __init__(self):
        self.evaluator = RAGAS()
        # Use absolute path to ensure correct file location
        self.dataset_path = Path(__file__).parent / "eval_dataset.json"
    
    def load_eval_dataset(self) -> List[Dict[str, Any]]:
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_evaluation(self) -> EvaluationResult:
        dataset = self.load_eval_dataset()
        return self.evaluator.evaluate_rag_pipeline(dataset)
    
    def save_results(self, results: EvaluationResult, output_path: str = None):
        if output_path is None:
            output_dir = Path(__file__).parent.parent.parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "ragas_evaluation_results.json"
        
        results_dict = {
            "faithfulness": results.faithfulness,
            "answer_relevancy": results.answer_relevancy,
            "context_precision": results.context_precision,
            "context_recall": results.context_recall,
            "answer_similarity": results.answer_similarity,
            "answer_correctness": results.answer_correctness,
            "overall_score": results.overall_score
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        print(f"Risultati salvati in: {output_path}")