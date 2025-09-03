# Configuration

The project uses YAML-based configuration for defining agents and tasks across all crews.

## Agent Configuration

Agents are configured in `agents.yaml` files within each crew's config directory:

```yaml
agent_name:
  role: >
    Agent's primary role description
  goal: >
    What the agent aims to achieve
  backstory: >
    Agent's background and expertise
  llm: Azure/gpt-4.1
```

### Common Agent Properties

- **Role**: Defines the agent's primary function and responsibility
- **Goal**: Specifies what the agent is trying to accomplish
- **Backstory**: Provides context about the agent's expertise and personality
- **LLM**: Specifies which language model to use (typically Azure GPT models)

## Task Configuration

Tasks are defined in `tasks.yaml` files:

```yaml
task_name:
  description: >
    Detailed description of what the task should accomplish
  expected_output: >
    Description of the expected output format and content
  agent: agent_name
```

### Task Properties

- **Description**: Clear instructions for task execution
- **Expected Output**: Specification of desired results
- **Agent**: Which agent should execute the task
- **Context**: Optional context from other tasks
- **Output File**: Optional file output specification

## Environment Variables

The project uses environment variables for API configuration:

```bash
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2024-02-01
MODEL=gpt-4
```

## Crew-Specific Configurations

### DocGen Crew
- Focuses on document generation agents
- Configured for structured output creation

### Math Crew
- Specialized for mathematical problem solving
- Includes tool configurations for math operations

### OCR Crew
- Configured for image processing and generation
- Includes DALL-E tool integration

### Summarization Crew
- Optimized for document summarization
- Configured for content analysis and condensation

### WebRAG Crew
- Combines web research with RAG capabilities
- Includes local document search configurations

### Summary Crew
- Multi-agent explanation system
- Hierarchical task structure for comprehensive explanations

## Configuration Best Practices

1. **Clear Descriptions**: Use descriptive and specific language
2. **Consistent Naming**: Follow naming conventions across crews
3. **Model Selection**: Choose appropriate models for task complexity
4. **Tool Integration**: Properly configure tools for agent capabilities
5. **Output Specifications**: Define clear output formats and expectations

## Dynamic Configuration

The system supports dynamic configuration through:
- Runtime parameter passing
- Context-aware task execution
- Flexible crew assembly
- Environment-based model selection
