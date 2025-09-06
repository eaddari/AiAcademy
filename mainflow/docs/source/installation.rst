Installation
============

Requirements
------------

* Python 3.8+
* CrewAI
* LangChain
* UV package manager
* API access for web search and AI models

Installation Steps
------------------

1. Clone the repository
2. Install dependencies using UV: ``uv install``
3. Set up environment variables
4. Configure YAML files in crew config directories

Environment Variables
---------------------

Set these environment variables for API access:

.. code-block:: bash

   export OPENAI_API_KEY="your-openai-key"
   export SERPER_API_KEY="your-serper-key"
   # Add other API keys as needed

Project Structure
-----------------

The project uses UV for dependency management and has the following structure:

* ``src/mainflow/`` - Main package
* ``src/mainflow/crews/`` - AI agent crews
* ``src/mainflow/tools/`` - Custom tools
* ``src/mainflow/utils/`` - Utility functions
