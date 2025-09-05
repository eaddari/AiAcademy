# Medical RAG Evaluation Crew

Welcome to the Medical RAG Evaluation project, powered by [crewAI](https://crewai.com). This project is designed to evaluate medical knowledge using Retrieval-Augmented Generation (RAG) with Azure OpenAI and vector search capabilities. The system uses AI agents to research and analyze medical information with proper source citations.

## Features

- **Medical RAG System**: Utilizes Qdrant vector database for medical document retrieval
- **Azure OpenAI Integration**: Powered by Azure OpenAI for intelligent analysis
- **CrewAI Multi-Agent System**: Specialized agents for research and analysis
- **DeepEval Integration**: Evaluation and monitoring of AI agent performance
- **Source Citations**: Proper attribution of medical information sources

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/evaluation/config/agents.yaml` to define your agents
- Modify `src/evaluation/config/tasks.yaml` to define your tasks
- Modify `src/evaluation/crew.py` to add your own logic, tools and specific args
- Modify `src/evaluation/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the evaluation Flow as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The evaluation Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
