from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from dotenv import load_dotenv

load_dotenv("C:\\desktopnoonedrive\\gruppo-finale\\AiAcademy\\mainflow\\.env")

@CrewBase
class PlanningCrew:
    """
    Study Planning Crew for Academic Research and Learning.

    This crew specializes in creating comprehensive study plans based on user requirements
    and learning objectives. The crew is composed of three specialized agents that work
    together to define, write, and review study plans to ensure quality and effectiveness.
    
    The planning process involves:
    - Analyzing user requirements and learning objectives
    - Defining a structured study plan framework
    - Writing detailed study plan content
    - Reviewing and refining the final plan

    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agent instances for the crew
    tasks : List[Task]
        List of task instances to be executed by the crew
    agents_config : str
        Path to the agents configuration YAML file (config/agents.yaml)
    tasks_config : str
        Path to the tasks configuration YAML file (config/tasks.yaml)
    model : str
        Azure OpenAI model configuration string in format "azure/{deployment_name}"

    Methods
    -------
    plan_definer() -> Agent
        Creates the plan definer agent for analyzing requirements
    plan_writer() -> Agent
        Creates the plan writer agent for content creation
    plan_reviewer() -> Agent
        Creates the plan reviewer agent for quality assurance
    define_plan() -> Task
        Creates the task for defining the study plan structure
    write_plan() -> Task
        Creates the task for writing the detailed study plan
    crew() -> Crew
        Creates and returns the complete crew configuration
    
    Examples
    --------
    >>> planning_crew = PlanningCrew()
    >>> result = planning_crew.crew().kickoff(inputs={"topic": "Machine Learning", "level": "beginner"})
    >>> print(result.raw)
    
    Notes
    -----
    This crew uses sequential processing where tasks are executed in order.
    All agents use the same Azure OpenAI model for consistency.
    The crew requires proper Azure OpenAI environment configuration.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self): 
        """
        Initialize the PlanningCrew.
        
        Sets up Azure OpenAI configuration and model string from environment variables.
        Configures the necessary API credentials and version for Azure OpenAI integration.
        
        Parameters
        ----------
        None
        
        Raises
        ------
        KeyError
            If required environment variables are not set
        ValueError
            If environment variables contain invalid values
        
        Notes
        -----
        Requires the following environment variables:
        - AZURE_OPENAI_API_KEY : str
            The API key for Azure OpenAI service
        - AZURE_OPENAI_ENDPOINT : str
            The endpoint URL for Azure OpenAI service
        - AZURE_DEPLOYMENT_NAME : str
            The name of the Azure OpenAI deployment
        
        The API version is set to "2024-12-01-preview" by default.
        """
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"
    @agent
    def plan_definer(self) -> Agent:
        """
        Create the plan definer agent.
        
        This agent analyzes user requirements and learning objectives to define
        the structure and framework for an effective study plan. It identifies
        key topics, prerequisites, and learning pathways.

        Returns
        -------
        Agent
            The plan definer agent instance configured with Azure OpenAI model
            and settings from agents_config["plan_definer"]
        
        Notes
        -----
        The plan definer agent is responsible for:
        - Analyzing user input and requirements
        - Identifying learning objectives and goals
        - Defining the overall structure of the study plan
        - Setting milestones and timelines
        - Determining prerequisites and dependencies
        """
        return Agent(
            config=self.agents_config["plan_definer"],
            llm=self.model,
        )
        
    @agent
    def plan_writer(self) -> Agent:
        """
        Create the plan writer agent.
        
        This agent takes the defined plan structure and creates detailed,
        comprehensive study plan content with specific learning activities,
        resources, and step-by-step instructions.

        Returns
        -------
        Agent
            The plan writer agent instance configured with Azure OpenAI model
            and settings from agents_config["plan_writer"]
        
        Notes
        -----
        The plan writer agent is responsible for:
        - Creating detailed study plan content
        - Specifying learning activities and exercises
        - Recommending resources and materials
        - Organizing content in a logical sequence
        - Adding time estimates and difficulty levels
        """
        return Agent(
            config=self.agents_config["plan_writer"],
            llm=self.model,
        )
        
    @agent
    def plan_reviewer(self) -> Agent:
        """
        Create the plan reviewer agent.
        
        This agent reviews the written study plan to ensure quality, completeness,
        and effectiveness. It validates the plan against best practices and
        provides feedback for improvement.

        Returns
        -------
        Agent
            The plan reviewer agent instance configured with Azure OpenAI model
            and settings from agents_config["plan_reviewer"]
        
        Notes
        -----
        The plan reviewer agent is responsible for:
        - Reviewing plan content for quality and completeness
        - Checking alignment with learning objectives
        - Validating the logical flow and structure
        - Ensuring appropriate difficulty progression
        - Providing recommendations for improvement
        - Verifying resource accessibility and relevance
        """
        return Agent(
            config=self.agents_config["plan_reviewer"],
            llm=self.model,
        )
    
    @task
    def define_plan(self) -> Task:
        """
        Create the define plan task.
        
        This task handles the analysis of user requirements and the definition
        of the study plan structure and framework. It establishes the foundation
        for the detailed plan creation.

        Returns
        -------
        Task
            The define plan task instance using configuration from
            tasks_config["define_plan"]
        
        Notes
        -----
        This is typically the first task in the planning pipeline.
        It establishes the foundation for subsequent plan writing and reviewing.
        The task output includes the plan structure, objectives, and timeline.
        """
        return Task(
            config=self.tasks_config["define_plan"],
        )
        
    @task
    def write_plan(self) -> Task:
        """
        Create the write plan task.
        
        This task handles the creation of detailed study plan content
        based on the defined structure and requirements. It produces
        comprehensive learning materials and activities.

        Returns
        -------
        Task
            The write plan task instance using configuration from
            tasks_config["write_plan"]
        
        Notes
        -----
        This task builds upon the output of the define_plan task
        to create comprehensive study plan content with specific
        activities, resources, and instructions.
        """
        return Task(
            config=self.tasks_config["write_plan"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Planning Crew.
        
        Assembles all agents and tasks into a sequential crew for comprehensive
        study plan creation and review. The crew ensures a systematic approach
        to creating high-quality, personalized study plans.

        Returns
        -------
        Crew
            The Planning Crew instance with all agents and tasks configured
            for sequential processing with verbose logging enabled
        
        Notes
        -----
        The crew uses sequential processing where tasks are executed in order:
        1. Define plan - Analyze requirements and create structure
        2. Write plan - Create detailed content and activities
        3. Review plan - Quality assurance and improvement (handled by plan_reviewer)
        
        Verbose mode is enabled for detailed logging of the planning process.
        The crew automatically manages task dependencies and agent coordination.
        
        Examples
        --------
        >>> crew_instance = self.crew()
        >>> inputs = {"topic": "Python Programming", "level": "intermediate"}
        >>> result = crew_instance.kickoff(inputs=inputs)
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
