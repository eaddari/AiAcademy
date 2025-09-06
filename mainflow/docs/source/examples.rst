Examples
========

Basic Study Plan Generation
----------------------------

.. code-block:: python

   from src.mainflow.main import MainFlow
   
   # Create a study plan for machine learning
   flow = MainFlow()
   result = flow.kickoff()

Advanced Usage
--------------

Customizing Crews
^^^^^^^^^^^^^^^^^

You can customize crew behavior by modifying the YAML configuration files:

.. code-block:: yaml

   # Example agent configuration
   researcher:
     role: "Research Specialist"
     goal: "Conduct thorough research on specified topics"
     backstory: "Expert researcher with deep knowledge"

Working with Results
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Access generated study plan
   with open('output/final_study_plan.md', 'r') as f:
       study_plan = f.read()
   
   # Process the results
   print(study_plan)

API Examples
------------

Using Individual Crews
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from src.mainflow.crews.input_crew.input_validation_crew import InputValidationCrew
   
   # Use input validation crew directly
   crew = InputValidationCrew()
   result = crew.crew().kickoff(inputs={"topic": "machine learning"})

Custom Tools
^^^^^^^^^^^^

.. code-block:: python

   from src.mainflow.tools.custom_tool import CustomTool
   
   # Use custom tools
   tool = CustomTool()
   result = tool.run("search query")
