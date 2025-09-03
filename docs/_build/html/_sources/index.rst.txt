===============================================================
Esercizio Esteso - CrewAI Multi-Agent System Documentation
===============================================================

Welcome to the documentation for the **Esercizio Esteso** project, a sophisticated multi-agent AI system built with `CrewAI <https://crewai.com>`_.

Project Overview
================

This project implements a complex workflow system using CrewAI flows and multiple specialized AI crews that collaborate to handle various types of research and documentation tasks.

Key Features
------------

- **Multi-Agent Flows**: Orchestrated workflows that coordinate multiple AI agents
- **Specialized Crews**: Different crews for specific tasks (math, research, documentation, etc.)
- **RAG Integration**: Retrieval-Augmented Generation for document-based research
- **Web Research**: Automated web-based information gathering
- **Mathematical Problem Solving**: Dedicated agents for mathematical computations
- **Document Generation**: Automated documentation and report creation

System Architecture
-------------------

The system is organized into several key components:

1. **Flows**: Main orchestration logic that coordinates different workflows
2. **Crews**: Specialized teams of agents for specific domains
3. **Tools**: Custom tools for enhanced agent capabilities
4. **Configuration**: YAML-based configuration for agents and tasks

Quick Start
===========

To run the project::

    crewai run

This will initialize the esercizio_esteso Flow and begin execution.

Documentation Structure
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   flows
   crews
   tools
   configuration
   autoapi/src/index

API Reference
=============

The complete API reference is automatically generated from the source code and can be found in the `API Documentation <autoapi/index.html>`_ section.

Project Structure
=================

::

    src/esercizio_esteso/
    ├── flow_copy.py           # Main generic flow implementation
    ├── flow_documentation.py # Documentation flow
    ├── main.py               # Entry point
    ├── crews/               # Specialized agent crews
    │   ├── docgen/         # Document generation crew
    │   ├── mathcrew/       # Mathematical problem solving crew
    │   ├── ocr_crew/       # OCR and image processing crew
    │   ├── rag/            # RAG-based research tools
    │   ├── summarization_crew/ # Document summarization crew
    │   ├── summary/        # Summary and explanation crew
    │   └── webrag/         # Web research and RAG crew
    └── tools/              # Custom tools and utilities
        ├── custom_tool.py  # Local RAG and math tools
        └── vision_tools.py # Vision and image processing tools

Contributing
============

This project is part of the AI Academy group exercise. For questions or contributions, please refer to the project maintainers.

License
=======

This project is developed as part of an educational exercise within the AI Academy program.
