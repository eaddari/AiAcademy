EY Junior Accelerator Documentation
===================================

Welcome to the EY Junior Accelerator project documentation. This project contains various AI crews 
for study planning and document generation using the CrewAI framework.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index

Overview
--------

The project consists of several crew modules that work together to create comprehensive study plans:

* **Planning Crew**: Handles the initial planning, writing, and reviewing of study plans
* **Study Plan Crew**: Creates and formats the final study plans
* **Document Generation Crew**: Generates final documentation
* **Web Crew**: Web-related functionality  
* **Input Crew**: Handles input processing

Each crew consists of specialized agents that work together using tasks to accomplish their goals.

Quick Start
-----------

To use any of the crews in your project:

.. code-block:: python

   from mainflow.crews.planner_crew.crew import PlanningCrew
   
   # Initialize the crew
   crew = PlanningCrew()
   
   # Get the configured crew instance
   planning_crew = crew.crew()

Architecture
------------

The project uses the CrewAI framework to orchestrate multiple AI agents working together 
to accomplish complex tasks. Each crew is defined as a class with:

* **Agents**: Individual AI agents with specific roles and capabilities
* **Tasks**: Specific jobs that agents need to accomplish  
* **Configuration**: YAML files that define agent behaviors and task parameters

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`