Quick Start
===========

Basic Usage
-----------

.. code-block:: python

   from src.mainflow.main import MainFlow
   
   # Initialize and run the main flow
   flow = MainFlow()
   result = flow.kickoff()

Example Flow
------------

1. User provides input topic and preferences
2. Input validation crew validates the request
3. Planner crew creates an execution plan
4. Web crew searches for relevant information
5. Paper crew analyzes academic papers
6. Study plan crew generates final learning plan
7. Results are saved to output files

Workflow Components
-------------------

The system consists of several specialized crews:

* **Input Validation Crew** - Validates and processes user input
* **Planner Crew** - Creates execution plans
* **Web Crew** - Performs web research
* **Paper Crew** - Analyzes academic papers
* **Study Plan Crew** - Generates comprehensive study plans

Configuration
-------------

Each crew has its own configuration files:

* ``agents.yaml`` - Defines agent roles and capabilities
* ``tasks.yaml`` - Defines tasks and workflows

Make sure these files are properly configured for your use case.
