"""
DeepEval Configuration for Medical RAG System
This file contains configuration settings and utility functions for DeepEval integration.
"""

import os
from typing import List, Dict, Any
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    HallucinationMetric,
    BiasMetric,
    ToxicityMetric
)
from deepeval.dataset import EvaluationDataset, Golden


class MedicalRAGEvaluationConfig:
    """Configuration class for medical RAG system evaluation"""
    
    def __init__(self):
        self.model = "gpt-4o-mini"  # You can change this to your preferred model
        self.base_threshold = 0.7
        self.hallucination_threshold = 0.3  # Lower is better for hallucination
        
    def get_core_metrics(self) -> List:
        """Get core evaluation metrics for medical RAG"""
        return [
            AnswerRelevancyMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            ),
            FaithfulnessMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            ),
            HallucinationMetric(
                threshold=self.hallucination_threshold,
                model=self.model,
                include_reason=True
            )
        ]
    
    def get_advanced_metrics(self) -> List:
        """Get advanced evaluation metrics including context-aware metrics"""
        metrics = self.get_core_metrics()
        metrics.extend([
            ContextualPrecisionMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            ),
            ContextualRecallMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            ),
            BiasMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            ),
            ToxicityMetric(
                threshold=self.base_threshold,
                model=self.model,
                include_reason=True
            )
        ])
        return metrics
    
    def get_medical_test_dataset(self) -> EvaluationDataset:
        """Get comprehensive medical test dataset"""
        return EvaluationDataset(
            goldens=[
                Golden(
                    input="What are the symptoms and treatment options for hypertension?",
                    expected_output="Hypertension symptoms may include headaches, shortness of breath, nosebleeds, fatigue, and chest pain. Treatment options include lifestyle modifications (reduced sodium intake, regular exercise, weight management, stress reduction) and medications such as ACE inhibitors, ARBs, beta-blockers, calcium channel blockers, and diuretics.",
                    context=[
                        "Hypertension is defined as blood pressure consistently above 140/90 mmHg",
                        "Lifestyle modifications are first-line treatment for mild hypertension",
                        "Multiple drug classes are available for hypertension management"
                    ]
                ),
                Golden(
                    input="What are the risk factors for cardiovascular disease?",
                    expected_output="Cardiovascular disease risk factors include modifiable factors (high blood pressure, high cholesterol, smoking, diabetes, obesity, physical inactivity, poor diet) and non-modifiable factors (age, gender, family history, ethnicity). Prevention focuses on managing modifiable risk factors.",
                    context=[
                        "Cardiovascular disease is the leading cause of death globally",
                        "Risk factors can be categorized as modifiable and non-modifiable",
                        "Primary prevention strategies focus on lifestyle modifications"
                    ]
                ),
                Golden(
                    input="How is diabetes type 2 diagnosed and managed?",
                    expected_output="Type 2 diabetes is diagnosed using fasting plasma glucose (≥126 mg/dL), HbA1c (≥6.5%), or oral glucose tolerance test (≥200 mg/dL at 2 hours). Management includes lifestyle modifications (diet, exercise), blood glucose monitoring, and medications like metformin, sulfonylureas, or insulin as needed.",
                    context=[
                        "Type 2 diabetes affects insulin sensitivity and glucose metabolism",
                        "Early diagnosis and management prevent complications",
                        "Lifestyle interventions are cornerstone of treatment"
                    ]
                ),
                Golden(
                    input="What are the common side effects of antibiotics?",
                    expected_output="Common antibiotic side effects include gastrointestinal issues (nausea, vomiting, diarrhea, abdominal pain), allergic reactions (rash, itching, anaphylaxis), secondary infections (candidiasis), and potential for antibiotic resistance. Specific side effects vary by antibiotic class.",
                    context=[
                        "Antibiotics can disrupt normal bacterial flora",
                        "Allergic reactions can range from mild to severe",
                        "Antibiotic resistance is a growing concern globally"
                    ]
                ),
                Golden(
                    input="What are the warning signs of a stroke?",
                    expected_output="Stroke warning signs include sudden face drooping, arm weakness, speech difficulty (FAST acronym), along with sudden severe headache, confusion, vision loss, dizziness, loss of coordination, and difficulty walking. Immediate emergency medical care is crucial.",
                    context=[
                        "Stroke is a medical emergency requiring immediate treatment",
                        "FAST acronym helps identify common stroke symptoms",
                        "Time is critical for stroke treatment effectiveness"
                    ]
                ),
                Golden(
                    input="What are the symptoms of anxiety disorders?",
                    expected_output="Anxiety disorder symptoms include excessive worry, restlessness, fatigue, difficulty concentrating, irritability, muscle tension, sleep disturbances, panic attacks, and physical symptoms like rapid heartbeat, sweating, and shortness of breath. Symptoms interfere with daily functioning.",
                    context=[
                        "Anxiety disorders are among the most common mental health conditions",
                        "Symptoms can be psychological and physical",
                        "Treatment includes therapy and medication options"
                    ]
                ),
                Golden(
                    input="How should minor cuts and wounds be treated?",
                    expected_output="Minor cuts should be cleaned with soap and water, bleeding controlled with direct pressure, antiseptic applied, and covered with a sterile bandage. Monitor for signs of infection (redness, swelling, warmth, pus). Seek medical attention for deep cuts, excessive bleeding, or signs of infection.",
                    context=[
                        "Proper wound care prevents infection",
                        "Basic first aid principles apply to minor injuries",
                        "Signs of infection require medical evaluation"
                    ]
                ),
                Golden(
                    input="What are the benefits and risks of vaccination?",
                    expected_output="Vaccination benefits include preventing serious diseases, reducing disease spread, protecting vulnerable populations through herd immunity, and eliminating diseases (like polio). Risks are generally minimal and include mild side effects (soreness, low fever) with serious adverse events being extremely rare.",
                    context=[
                        "Vaccines are one of the most successful public health interventions",
                        "Benefits far outweigh risks for approved vaccines",
                        "Herd immunity protects entire communities"
                    ]
                )
            ]
        )


def setup_deepeval_environment():
    """Setup environment variables for DeepEval"""
    # These should be set in your .env file or environment
    required_vars = [
        "OPENAI_API_KEY",  # For DeepEval metrics evaluation
        "CONFIDENT_API_KEY"  # For Confident AI dashboard (optional)
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {missing_vars}")
        print("Please set these in your .env file for full DeepEval functionality")
    
    return len(missing_vars) == 0


def print_evaluation_summary(results: List[Dict[str, Any]]):
    """Print a summary of evaluation results"""
    total_tests = len(results)
    successful_tests = len([r for r in results if not r.get("error")])
    failed_tests = total_tests - successful_tests
    
    print("\n" + "="*60)
    print("📊 DEEPEVAL MEDICAL RAG EVALUATION SUMMARY")
    print("="*60)
    print(f"Total Test Cases: {total_tests}")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    print("="*60)
    
    if failed_tests > 0:
        print("\n⚠️  Failed test cases:")
        for i, result in enumerate(results):
            if result.get("error"):
                print(f"  - Test {i+1}: {result['input'][:50]}...")


# Export configuration instance
config = MedicalRAGEvaluationConfig()
