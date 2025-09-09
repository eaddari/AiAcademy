Configuration
=============

Project Configuration
----------------------

The project uses several configuration files:

* ``pyproject.toml`` - Project metadata and dependencies
* ``uv.lock`` - Locked dependency versions

Crew Configuration
------------------

Each crew has its own configuration directory with:

* ``agents.yaml`` - Agent definitions
* ``tasks.yaml`` - Task definitions

Agent Configuration
-------------------

Agents are defined with:

* Role and goal
* Backstory and context
* Tools and capabilities
* LLM configuration

Task Configuration
------------------

Tasks define:

* Description and expected output
* Agent assignments
* Dependencies and context
* Output formats

Environment Variables
---------------------

Required environment variables:

.. code-block:: bash

   # OpenAI API
   OPENAI_API_KEY=your_key_here
   
   # Search API
   SERPER_API_KEY=your_key_here
   
   # Other APIs as needed
