"""
Mathematical Problem Solving Crew for CrewAI Multi-Agent System.

This module implements a specialized crew focused on solving mathematical
equations and performing complex calculations. The crew utilizes advanced
mathematical tools and Azure OpenAI capabilities for accurate problem solving.

Classes
-------
Math : CrewBase
    Main crew class that coordinates mathematical agents for solving
    equations and performing mathematical analysis.

Notes
-----
The crew integrates with custom mathematical tools and includes SSL
configuration for secure operations. Specialized for numerical computations
and equation solving tasks.
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.custom_tool import MathEquationsTool
import ssl
import httpx

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

@CrewBase
class Math():
    """
    Mathematical problem solving crew implementation.
    
    This crew specializes in solving mathematical equations, performing
    calculations, and providing step-by-step mathematical analysis. The
    crew uses specialized mathematical tools for accurate computations.
    
    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized mathematical agents within the crew.
    tasks : List[Task]
        List of mathematical tasks that the crew can execute.
        
    Methods
    -------
    math_tool_agent()
        Creates a mathematical agent equipped with calculation tools.
    math_task()
        Defines the mathematical problem-solving task configuration.
    crew()
        Assembles and configures the complete mathematical crew.
        
    Examples
    --------
    >>> math_crew = Math()
    >>> math_agent = math_crew.math_tool_agent()
    >>> result = math_agent.execute_task(math_crew.math_task())
    
    Notes
    -----
    The crew uses YAML configuration files for agent and task definitions,
    enabling flexible customization of mathematical problem-solving approaches.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def math_tool_agent(self) -> Agent:
        """
        Create a mathematical agent equipped with calculation tools.
        
        Initializes an agent specialized in mathematical problem solving
        with access to advanced mathematical tools for equations,
        calculations, and numerical analysis.
        
        Returns
        -------
        Agent
            Configured agent instance with mathematical capabilities
            and access to MathEquationsTool for complex calculations.
            
        Notes
        -----
        The agent is equipped with specialized mathematical tools and
        configured for verbose operation to provide detailed solution
        steps and mathematical reasoning.
        """
        return Agent(
            config=self.agents_config['math_tool_agent'], # type: ignore[index]
            verbose=True,
            tools=[MathEquationsTool()]
        )

    @task
    def math_task(self) -> Task:
        """
        Define the mathematical problem-solving task configuration.
        
        Creates a task that processes mathematical equations, performs
        calculations, and provides step-by-step solutions with detailed
        explanations of mathematical reasoning.
        
        Returns
        -------
        Task
            Configured task instance for mathematical problem solving
            with appropriate input processing and solution formatting.
            
        Notes
        -----
        Task configuration is loaded from YAML files allowing for
        flexible customization of mathematical problem types, solution
        formats, and output requirements.
        """
        return Task(
            config=self.tasks_config['math_task'] # type: ignore[index]
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Assemble and configure the complete Mathematical crew.
        
        Creates a crew instance that coordinates mathematical agents
        in a sequential workflow for solving equations, performing
        calculations, and providing comprehensive mathematical analysis.
        
        Returns
        -------
        Crew
            Configured crew instance with agents, tasks, and process
            definition for mathematical problem solving operations.
            
        Notes
        -----
        The crew uses sequential processing to ensure proper mathematical
        analysis and solution verification. Verbose logging is enabled
        for monitoring calculation processes and solution accuracy.
        """

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )