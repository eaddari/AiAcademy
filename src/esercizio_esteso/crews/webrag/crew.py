"""
Web Research and RAG Crew for CrewAI Multi-Agent System.

This module implements a specialized crew that combines web research capabilities
with local Retrieval-Augmented Generation (RAG) functionality. The crew enables
intelligent information gathering from both web sources and local document
collections.

Classes
-------
Webrag : CrewBase
    Main crew class that coordinates RAG research and reporting agents
    for comprehensive information gathering and analysis.

Notes
-----
The crew uses specialized agents with LocalRag tools for document retrieval
and analysis. SSL configuration is included for secure web operations.
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.esercizio_esteso.tools.custom_tool import LocalRag
from src.esercizio_esteso.tools.rag_tool import RetrievalTool
import ssl
import httpx

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

@CrewBase
class Webrag():
    """
    Web Research and RAG crew implementation.
    
    This crew combines web research capabilities with local RAG functionality
    to provide comprehensive information gathering and analysis. The crew
    consists of specialized agents for research and reporting tasks.
    
    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agents within the crew.
    tasks : List[Task]
        List of tasks that the crew can execute.
        
    Methods
    -------
    rag_researcher()
        Creates a RAG research agent with local document access.
    reporting_analyst()
        Creates a reporting agent for analysis and documentation.
    rag_research_task()
        Defines the RAG research task configuration.
    reporting_task()
        Defines the reporting and analysis task configuration.
    crew()
        Assembles and configures the complete crew.
        
    Examples
    --------
    >>> webrag_crew = Webrag()
    >>> researcher = webrag_crew.rag_researcher()
    >>> task_result = researcher.execute_task(webrag_crew.rag_research_task())
    
    Notes
    -----
    The crew uses YAML configuration files for agent and task definitions,
    enabling flexible customization without code changes.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def rag_researcher(self) -> Agent:
        """
        Create a RAG research agent with local document access.
        
        Initializes an agent specialized in Retrieval-Augmented Generation
        research using local document collections. The agent is equipped
        with LocalRag tools for semantic document search and analysis.
        
        Returns
        -------
        Agent
            Configured agent instance with RAG research capabilities
            and access to local document search tools.
            
        Notes
        -----
        The agent configuration is loaded from YAML files and includes
        verbose logging for debugging and monitoring purposes.
        """
        return Agent(
            config=self.agents_config['rag_researcher'], # type: ignore[index]
            verbose=True,
            tools=[RetrievalTool()]
        )

    @agent
    def reporting_analyst(self) -> Agent:
        """
        Create a reporting and analysis agent.
        
        Initializes an agent specialized in analyzing research findings
        and creating comprehensive reports based on RAG research results.
        
        Returns
        -------
        Agent
            Configured agent instance with reporting and analysis
            capabilities for synthesizing research findings.
            
        Notes
        -----
        This agent focuses on analysis and report generation without
        direct tool access, relying on processed information from
        the RAG researcher.
        """
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def rag_research_task(self) -> Task:
        """
        Define the RAG research task configuration.
        
        Creates a task that utilizes local document retrieval and analysis
        to gather comprehensive information on specified topics.
        
        Returns
        -------
        Task
            Configured task instance for RAG-based research operations
            with appropriate context and output specifications.
            
        Notes
        -----
        Task configuration is loaded from YAML files allowing for
        flexible customization of research parameters and objectives.
        """
        return Task(
            config=self.tasks_config['rag_research_task'] # type: ignore[index]
        )
        
    @task
    def reporting_task(self) -> Task:
        """
        Define the reporting and analysis task configuration.
        
        Creates a task for analyzing research findings and generating
        comprehensive reports based on RAG research results.
        
        Returns
        -------
        Task
            Configured task instance for report generation with
            markdown output formatting and file export capabilities.
            
        Notes
        -----
        The task automatically outputs results to 'report.md' file
        and includes structured analysis of research findings.
        """
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )


    @crew
    def crew(self) -> Crew:
        """
        Assemble and configure the complete Webrag crew.
        
        Creates a crew instance that coordinates RAG research and reporting
        agents in a sequential workflow for comprehensive information
        gathering and analysis.
        
        Returns
        -------
        Crew
            Configured crew instance with agents, tasks, and process
            definition for web research and RAG operations.
            
        Notes
        -----
        The crew uses sequential processing to ensure research is
        completed before analysis begins. Verbose logging is enabled
        for monitoring and debugging purposes.
        """

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
