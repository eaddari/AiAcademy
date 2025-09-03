import argparse
from src.esercizio_esteso.evaluation.evaluation_pipeline import EvaluationPipeline


def main():
    parser = argparse.ArgumentParser(description="Valuta il sistema RAG usando RAGAS")
    parser.add_argument(
        "--dataset", 
        type=str, 
    )
    parser.add_argument(
        "--output", 
        type=str, 
    )
    
    args = parser.parse_args()
    
    pipeline = EvaluationPipeline(args.dataset)
    
    results = pipeline.run_evaluation()

    pipeline.save_results(results, args.output)


if __name__ == "__main__":
    main()