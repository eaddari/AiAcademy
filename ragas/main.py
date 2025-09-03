from pipeline import EvaluationPipeline


def main():

    pipeline = EvaluationPipeline()
    results = pipeline.run_evaluation()
    pipeline.save_results(results)

if __name__ == "__main__":
    main()