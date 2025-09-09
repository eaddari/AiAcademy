# DeepEval Integration with CrewAI Medical RAG System

This project integrates DeepEval with your CrewAI medical RAG system to provide comprehensive evaluation and monitoring capabilities.

## 🚀 Features

- **Automatic Tracing**: All CrewAI agent interactions are automatically traced
- **Comprehensive Metrics**: Multiple evaluation metrics for medical RAG quality
- **Medical-Specific Evaluation**: Tailored evaluation dataset for medical queries
- **Dashboard Integration**: Optional integration with Confident AI dashboard
- **Local Evaluation**: Run evaluations locally without external dependencies

## 📋 Prerequisites

Make sure you have DeepEval installed:
```bash
pip install -U deepeval
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root with the following variables:

```env
# Required for your existing Azure OpenAI setup
MODEL=your-model-name
OPENAI_BASE_URL=your-azure-openai-endpoint
AZURE_OPENAI_API_KEY=your-azure-api-key

# Required for DeepEval metrics evaluation
OPENAI_API_KEY=your-openai-api-key

# Optional - for Confident AI dashboard integration
CONFIDENT_API_KEY=your-confident-ai-api-key
```

### Evaluation Metrics

The system uses the following metrics by default:

1. **Answer Relevancy** (threshold: 0.7) - Measures how relevant the answer is to the question
2. **Faithfulness** (threshold: 0.7) - Measures how factual the answer is based on the retrieved context
3. **Hallucination** (threshold: 0.3) - Measures if the answer contains hallucinated information
4. **Contextual Precision** (threshold: 0.7) - Measures precision of retrieved context
5. **Contextual Recall** (threshold: 0.7) - Measures recall of retrieved context

## 🏃‍♂️ Usage

### Single Query Execution

Run a single medical query with tracing:

```bash
python src/evaluation/main.py
```

This will:
- Execute the default medical query about hypertension
- Generate traces visible on Confident AI dashboard
- Save results to `medical_analysis.txt`

### Comprehensive Evaluation

Run the full evaluation suite:

```bash
python src/evaluation/main.py --evaluate
```

This will:
- Execute 8 different medical test cases
- Evaluate each response using multiple metrics
- Generate detailed evaluation report
- Save results to `deepeval_medical_results.txt`
- Display summary statistics

### Advanced Evaluation

For more advanced metrics (including bias and toxicity detection):

```python
from deepeval_config import config

# Get advanced metrics
advanced_metrics = config.get_advanced_metrics()

# Use in your crew initialization
```

## 📊 Evaluation Results

### Local Results

Results are saved to `deepeval_medical_results.txt` with:
- Input queries
- Expected outputs
- Actual agent responses
- Success/failure status
- Error details (if any)

### Confident AI Dashboard

If `CONFIDENT_API_KEY` is configured, you can view:
- Real-time traces of agent interactions
- Metric scores and trends
- Performance analytics
- Comparison between different runs

Visit: https://app.confident.ai/

## 🧪 Test Cases

The evaluation includes medical queries covering:

1. **Hypertension** - Symptoms and treatment options
2. **Cardiovascular Disease** - Risk factors and prevention
3. **Type 2 Diabetes** - Diagnosis and management
4. **Antibiotics** - Common side effects
5. **Stroke** - Warning signs and emergency response
6. **Anxiety Disorders** - Symptoms and manifestations
7. **Wound Care** - Basic first aid for minor injuries
8. **Vaccination** - Benefits and risks

## 🔧 Customization

### Adding New Test Cases

Edit `deepeval_config.py` to add new medical scenarios:

```python
Golden(
    input="Your medical question",
    expected_output="Expected comprehensive answer",
    context=["Relevant context 1", "Relevant context 2"]
)
```

### Adjusting Metrics

Modify thresholds in `deepeval_config.py`:

```python
def get_core_metrics(self) -> List:
    return [
        AnswerRelevancyMetric(
            threshold=0.8,  # Increase for stricter evaluation
            model="gpt-4o-mini",
            include_reason=True
        )
    ]
```

### Custom Metrics

Add domain-specific metrics:

```python
from deepeval.metrics import CustomMetric

class MedicalAccuracyMetric(CustomMetric):
    def measure(self, test_case):
        # Implement medical-specific evaluation logic
        pass
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure OPENAI_API_KEY is set for metric evaluation
2. **Azure Connection**: Verify Azure OpenAI credentials are correct
3. **Model Access**: Ensure you have access to the specified models
4. **Import Errors**: Verify DeepEval is properly installed

### Error Messages

- `Warning: Missing environment variables`: Set required API keys
- `Error in test case X`: Check individual test case details in output
- `Model access denied`: Verify API key permissions and model availability

## 📈 Performance Tips

1. **Batch Evaluation**: Use the `--evaluate` flag for comprehensive testing
2. **Metric Selection**: Choose appropriate metrics for your use case
3. **Threshold Tuning**: Adjust thresholds based on your quality requirements
4. **Context Quality**: Ensure your RAG retrieval provides relevant context

## 🔗 Additional Resources

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [CrewAI Integration Guide](https://www.confident-ai.com/docs/integrations/third-party/crew-ai)
- [Confident AI Dashboard](https://app.confident.ai/)
- [Medical RAG Best Practices](https://docs.confident-ai.com/docs/llm-evaluation/metrics)

## 🤝 Contributing

To extend the evaluation system:

1. Add new metrics in `deepeval_config.py`
2. Extend test cases for better coverage
3. Implement domain-specific evaluation logic
4. Add custom visualization and reporting

## 📝 License

This integration follows your existing project license terms.
