"""
Quick test script for DeepEval integration
This script tests the basic functionality of DeepEval with your CrewAI setup.
"""

import os
import sys
from deepeval.integrations.crewai import instrument_crewai

def test_deepeval_setup():
    """Test basic DeepEval setup"""
    print("🧪 Testing DeepEval Integration Setup...")
    
    # Test 1: Import check
    try:
        from deepeval.metrics import AnswerRelevancyMetric
        from deepeval.integrations.crewai import Agent
        print("✅ DeepEval imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("   These are required for metric evaluation")
    else:
        print("✅ Required environment variables found")
    
    # Test 3: Instrumentation
    try:
        instrument_crewai()
        print("✅ CrewAI instrumentation successful")
    except Exception as e:
        print(f"❌ Instrumentation error: {e}")
        return False
    
    # Test 4: Metric creation
    try:
        metric = AnswerRelevancyMetric(
            threshold=0.7,
            model="gpt-4o-mini",
            include_reason=True
        )
        print("✅ Metric creation successful")
    except Exception as e:
        print(f"❌ Metric creation error: {e}")
        return False
    
    # Test 5: Agent creation with metrics
    try:
        from crewai import LLM
        
        # Test with basic configuration
        agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            metrics=[metric],
            verbose=False
        )
        print("✅ DeepEval Agent creation successful")
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False
    
    print("\n🎉 All tests passed! DeepEval integration is ready.")
    return True


def test_configuration():
    """Test the custom configuration"""
    print("\n🔧 Testing Custom Configuration...")
    
    try:
        from deepeval_config import config, setup_deepeval_environment
        
        # Test configuration loading
        metrics = config.get_core_metrics()
        print(f"✅ Core metrics loaded: {len(metrics)} metrics")
        
        dataset = config.get_medical_test_dataset()
        print(f"✅ Test dataset loaded: {len(dataset.goldens)} test cases")
        
        # Test environment setup
        env_ok = setup_deepeval_environment()
        if env_ok:
            print("✅ Environment setup complete")
        else:
            print("⚠️  Environment setup has warnings (see above)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def run_quick_test():
    """Run a quick end-to-end test"""
    print("\n🚀 Running Quick End-to-End Test...")
    
    try:
        # Import your crew
        from src.evaluation.crews.rag_crew.crew import RagCrew
        
        # Create a simple test query
        test_query = "What is hypertension?"
        
        print(f"Testing query: {test_query}")
        
        # Create crew and run
        crew_instance = RagCrew()
        crew = crew_instance.crew()
        
        result = crew.kickoff(inputs={"medical_query": test_query})
        
        print("✅ Crew execution successful")
        print(f"📝 Result preview: {str(result.raw)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test error: {e}")
        return False


if __name__ == "__main__":
    print("🔍 DeepEval Integration Test Suite")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Basic Setup", test_deepeval_setup),
        ("Configuration", test_configuration),
        ("End-to-End", run_quick_test)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your DeepEval integration is ready to use.")
        print("\nNext steps:")
        print("1. Run: python src/evaluation/main.py --evaluate")
        print("2. Check the results in deepeval_medical_results.txt")
        print("3. Visit Confident AI dashboard if CONFIDENT_API_KEY is configured")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above and:")
        print("1. Ensure all required packages are installed")
        print("2. Set required environment variables")
        print("3. Check your configuration files")
