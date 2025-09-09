# src/mainflow/crews/web_crew/crew.py
from __future__ import annotations

import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from src.mainflow.tools.custom_tool import SerperSearchTool
from typing import List
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv("C:\\desktopnoonedrive\\gruppo-finale\\AiAcademy\\mainflow\\.env")
search_tool = SerperSearchTool()
@CrewBase
class WebCrew:
    """
    Web Research Crew for Educational Resource Discovery.

    This crew specializes in enhancing study plans with relevant web resources
    by leveraging advanced search capabilities. It takes study plans from the
    planning crew and systematically searches for high-quality educational
    resources, official documentation, tutorials, and learning materials.

    The web research process involves:
    - Analyzing study plan topics and learning objectives
    - Conducting targeted web searches using Serper search tool
    - Evaluating and filtering search results for educational value
    - Curating trustworthy and relevant learning resources
    - Organizing resources by topic and difficulty level

    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agent instances for web research
    tasks : List[Task]
        List of task instances to be executed by the crew
    agents_config : str
        Path to the agents configuration YAML file (config/agents.yaml)
    tasks_config : str
        Path to the tasks configuration YAML file (config/tasks.yaml)
    model : str
        Azure OpenAI model configuration string in format "azure/{deployment_name}"
    search_tool : SerperSearchTool
        Custom search tool instance for web research

    Methods
    -------
    web_researcher() -> Agent
        Creates the web researcher agent with search capabilities
    web_search_task() -> Task
        Creates the web search task for resource discovery
    crew() -> Crew
        Creates and returns the complete crew configuration

    Examples
    --------
    >>> web_crew = WebCrew()
    >>> inputs = {"plan": "Python programming study plan for beginners"}
    >>> result = web_crew.crew().kickoff(inputs=inputs)
    >>> print(result.raw)  # Contains curated web resources

    Notes
    -----
    This crew uses the Serper search API for web searches, requiring proper
    API key configuration. The crew focuses on finding trustworthy educational
    resources and filters out low-quality or inappropriate content.
    SSL warnings are disabled for development purposes.
    """
    
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        """
        Initialize the WebCrew.

        Sets up Azure OpenAI configuration, search tools, and environment
        variables required for web research operations.

        Parameters
        ----------
        None

        Raises
        ------
        KeyError
            If required environment variables are not set
        ValueError
            If environment variables contain invalid values
        ConnectionError
            If unable to connect to Azure OpenAI or Serper API

        Notes
        -----
        Requires the following environment variables:
        - AZURE_OPENAI_API_KEY : str
            The API key for Azure OpenAI service
        - AZURE_OPENAI_ENDPOINT : str
            The endpoint URL for Azure OpenAI service
        - AZURE_DEPLOYMENT_NAME : str
            The name of the Azure OpenAI deployment
        - SERPER_API_KEY : str
            The API key for Serper search service

        The initialization also disables SSL warnings for urllib3 to handle
        development environment certificate issues.
        """
        # Set up Azure OpenAI environment variables
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string for Azure OpenAI
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"

    @agent
    def web_researcher(self) -> Agent:
        """
        Create the web researcher agent.

        This agent specializes in conducting intelligent web searches to find
        relevant educational resources based on study plan requirements. It uses
        the Serper search tool to perform targeted searches and evaluate results.

        Returns
        -------
        Agent
            The web researcher agent instance configured with Serper search tool
            and Azure OpenAI model from agents_config["web_researcher"]

        Notes
        -----
        The web researcher agent is responsible for:
        - Analyzing study plan topics to identify search queries
        - Conducting systematic web searches using Serper API
        - Evaluating search results for educational relevance and quality
        - Filtering out inappropriate or low-quality content
        - Prioritizing official documentation and trusted educational sources
        - Organizing findings by topic and difficulty level

        The agent uses the SerperSearchTool for web searches and is configured
        with the Azure OpenAI model for intelligent content processing.
        """
        return Agent(
            config=self.agents_config["web_researcher"],
            tools=[search_tool],
            llm=self.model,
        )

    @task
    def web_search_task(self) -> Task:
        """
        Create the web search task.

        This task handles the systematic search and curation of web resources
        based on the study plan provided by the planning crew. It focuses on
        finding high-quality educational materials and learning resources.

        Returns
        -------
        Task
            The web search task instance using configuration from
            tasks_config["web_search_task"]

        Notes
        -----
        The web search task performs the following operations:
        - Parses the input study plan to extract key topics and concepts
        - Generates targeted search queries for each topic
        - Executes web searches using the Serper search tool
        - Evaluates and filters search results for educational value
        - Curates a list of high-quality learning resources
        - Organizes resources by relevance and learning progression
        - Provides descriptions and recommendations for each resource

        The task outputs a structured collection of web resources that
        complement and enhance the original study plan.
        """
        return Task(
            config=self.tasks_config["web_search_task"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Web Research Crew.

        Assembles the web researcher agent and search task into a sequential
        crew for systematic educational resource discovery and curation.

        Returns
        -------
        Crew
            The Web Research Crew instance with the web researcher agent and
            search task configured for sequential processing with verbose logging

        Notes
        -----
        The crew uses sequential processing where the web search task is
        executed by the web researcher agent. Verbose mode is enabled for
        detailed logging of the search and curation process.

        The crew workflow:
        1. Receives study plan input from planning crew
        2. Analyzes plan topics and learning objectives
        3. Conducts targeted web searches for relevant resources
        4. Evaluates and curates high-quality educational materials
        5. Outputs organized list of web resources with descriptions

        The crew is designed to enhance study plans with practical,
        accessible web resources that support the learning objectives.

        Examples
        --------
        >>> crew_instance = self.crew()
        >>> inputs = {"plan": "Data Science fundamentals study plan"}
        >>> result = crew_instance.kickoff(inputs=inputs)
        >>> # Result contains curated web resources for data science learning
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
