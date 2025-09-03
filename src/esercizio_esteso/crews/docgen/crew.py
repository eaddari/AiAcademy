"""
Document Generation Crew for CrewAI Multi-Agent System.

This module implements a specialized crew focused on generating high-quality
technical documentation from research findings and structured inputs. The crew
utilizes Azure OpenAI capabilities for professional document creation.

Classes
-------
Docgen : CrewBase
    Main crew class that coordinates document generation agents for
    creating comprehensive technical documentation.

Notes
-----
The crew integrates with Azure OpenAI services and includes SSL configuration
for secure operations. Tools can be optionally enabled for enhanced capabilities.
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from langchain_openai import AzureChatOpenAI
import os
import ssl
import httpx

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

@CrewBase
class Docgen():
    """
    Document Generation crew implementation.
    
    This crew specializes in creating professional technical documentation
    from research findings, analysis results, and structured inputs. The
    crew uses advanced language models for high-quality document generation.
    
    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agents within the crew.
    tasks : List[Task]
        List of tasks that the crew can execute.
        
    Methods
    -------
    generation_agent()
        Creates a document generation agent with advanced writing capabilities.
    document_generation_task()
        Defines the document generation task configuration.
    crew()
        Assembles and configures the complete crew.
        
    Examples
    --------
    >>> docgen_crew = Docgen()
    >>> generator = docgen_crew.generation_agent()
    >>> task_result = generator.execute_task(docgen_crew.document_generation_task())
    
    Notes
    -----
    The crew uses YAML configuration files for agent and task definitions,
    enabling flexible customization of documentation styles and requirements.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def generation_agent(self) -> Agent:
        """
        Create a document generation agent with advanced writing capabilities.
        
        Initializes an agent specialized in creating high-quality technical
        documentation with professional formatting and comprehensive content
        organization.
        
        Returns
        -------
        Agent
            Configured agent instance with document generation capabilities
            and optional tool integration for enhanced functionality.
            
        Notes
        -----
        The agent configuration is loaded from YAML files and supports
        optional tool integration (currently disabled). Verbose logging
        is enabled for monitoring document generation processes.
        """
        return Agent(
            config=self.agents_config['generation_agent'], # type: ignore[index]
            verbose=True,
            # tools=[SerperDevTool()] possibilità di usare tool al momento disattivata
        )
    
    @task
    def document_generation_task(self) -> Task:
        """
        Define the document generation task configuration.
        
        Creates a task that transforms research findings and structured
        inputs into comprehensive technical documentation with professional
        formatting and organization.
        
        Returns
        -------
        Task
            Configured task instance for document generation with
            appropriate input processing and output formatting.
            
        Notes
        -----
        Task configuration is loaded from YAML files allowing for
        flexible customization of documentation templates, styles,
        and output requirements.
        """
        return Task(
            config=self.tasks_config['document_generation_task'] # type: ignore[index]
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Assemble and configure the complete Document Generation crew.
        
        Creates a crew instance that coordinates document generation agents
        in a sequential workflow for creating comprehensive technical
        documentation from various inputs.
        
        Returns
        -------
        Crew
            Configured crew instance with agents, tasks, and process
            definition for professional document generation.
            
        Notes
        -----
        The crew uses sequential processing to ensure proper document
        structure and content organization. Verbose logging is enabled
        for monitoring generation progress and quality assurance.
        """

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )