from pipeline import EvaluationPipeline


def main():
    try:
        print("Starting RAGAS evaluation...")
        pipeline = EvaluationPipeline()
        print("Pipeline initialized successfully.")
        
        print("Running evaluation...")
        results = pipeline.run_evaluation()
        print("Evaluation completed.")
        
        print("Saving results...")
        pipeline.save_results(results)
        print("Done!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()