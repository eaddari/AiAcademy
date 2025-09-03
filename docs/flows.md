# Flows

The system implements several sophisticated flows that orchestrate multi-agent collaboration.

## Generic Flow

The `GenericFlow` is the main workflow orchestrator that handles different types of research requests:

- **Input Collection**: Gathers user requirements and research topics
- **Research Planning**: Creates structured plans for research execution
- **Orchestration**: Determines the appropriate research method (RAG, Web, or Math)
- **Execution**: Executes the chosen research methodology
- **Synthesis**: Combines findings and generates final reports

### Flow States

The flow maintains state through `GenericFlowState` which tracks:
- User input and topic
- Research plans and decisions
- Results from different research methods
- Final report structure

### Research Routing

The flow intelligently routes requests to appropriate crews:
- **Math Path**: For mathematical equations and calculations
- **RAG Path**: For queries about specific document collections (e.g., Minecraft dirt blocks)
- **Web Path**: For general web-based research

## Documentation Flow

The `DocumentationFlow` specializes in creating documentation from research findings:

- Utilizes web research crews for information gathering
- Employs document generation crews for structured output
- Maintains documentation-specific state management

## Flow Execution

Flows are executed using CrewAI's flow decorators:
- `@start()`: Entry points for flow execution
- `@listen()`: Event-based flow continuation
- `@router()`: Conditional flow routing
- `@or_()`: Multiple path convergence
