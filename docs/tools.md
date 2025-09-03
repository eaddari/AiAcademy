# Tools

The project includes several custom tools that enhance agent capabilities.

## Custom Tools (`custom_tool.py`)

### LocalRag Tool

A custom Retrieval-Augmented Generation tool for searching local document collections.

**Features:**
- FAISS-based vector search
- Local document indexing
- Semantic similarity matching
- Configurable search parameters

**Usage:**
Used by research crews to find relevant information in local document collections, particularly effective for domain-specific knowledge bases.

### MathEquationsTool

Specialized tool for solving mathematical equations and performing calculations.

**Features:**
- Equation parsing and solving
- Mathematical computation capabilities
- Structured output formatting

**Usage:**
Integrated with the mathematical crew for solving complex mathematical problems and equations.

## Vision Tools (`vision_tools.py`)

### DallETool

Image generation tool using DALL-E API for creating visual content.

**Features:**
- Text-to-image generation
- High-quality visual output
- Integration with Azure OpenAI services

**Usage:**
Used by the OCR crew for generating images based on textual descriptions and visual content requirements.

## Tool Integration

Tools are integrated into crews through the CrewAI framework:

```python
@agent
def agent_with_tools(self) -> Agent:
    return Agent(
        config=self.agents_config['agent_name'],
        tools=[CustomTool()]
    )
```

## Tool Configuration

Tools can be configured with:
- API keys and endpoints
- Custom parameters
- SSL configurations for secure connections
- Error handling and retry logic

## Custom Tool Development

The project demonstrates how to create custom tools that extend agent capabilities:

1. **Inherit from BaseTool**: All custom tools inherit from CrewAI's BaseTool
2. **Define Tool Schema**: Specify input parameters and descriptions
3. **Implement _run Method**: Core tool functionality
4. **Handle Errors**: Robust error handling and logging
5. **Documentation**: Clear docstrings and usage examples
