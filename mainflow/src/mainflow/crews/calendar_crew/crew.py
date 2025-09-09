from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from dotenv import load_dotenv

load_dotenv("C:\\desktopnoonedrive\\gruppo-finale\\AiAcademy\\mainflow\\.env")

@CrewBase
class CalendarCrew:
    """
    Calendar Crew for Study Schedule Management.

    This crew specializes in creating detailed study calendars and schedules
    based on study plans and learning objectives. It transforms abstract study
    plans into concrete, time-bound schedules with specific milestones, deadlines,
    and learning activities organized across time periods.

    The calendar creation process involves:
    - Analyzing study plans to identify key topics and time requirements
    - Defining calendar structure with appropriate time blocks and milestones
    - Writing detailed calendar entries with specific learning activities
    - Organizing schedule to optimize learning progression and retention

    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agent instances for calendar management
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
    calendar_definer() -> Agent
        Creates the calendar definer agent for schedule structure planning
    calendar_writer() -> Agent
        Creates the calendar writer agent for detailed schedule creation
    define_calendar() -> Task
        Creates the task for defining calendar structure and framework
    write_calendar() -> Task
        Creates the task for writing detailed calendar content
    crew() -> Crew
        Creates and returns the complete crew configuration

    Examples
    --------
    >>> calendar_crew = CalendarCrew()
    >>> inputs = {
    ...     "plan": "Machine Learning study plan",
    ...     "duration": "6 months",
    ...     "hours_per_week": 10
    ... }
    >>> result = calendar_crew.crew().kickoff(inputs=inputs)
    >>> print(result.raw)  # Contains detailed study calendar

    Notes
    -----
    This crew focuses on temporal organization of study activities and creates
    realistic, achievable schedules. It considers learning progression, spaced
    repetition, and optimal time allocation for different types of learning
    activities. The crew uses sequential processing to ensure proper calendar
    structure before detailed content creation.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self): 
        """
        Initialize the CalendarCrew.

        Sets up Azure OpenAI configuration and model string from environment
        variables. Configures the necessary API credentials and version for
        Azure OpenAI integration used by calendar planning agents.

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
    def calendar_definer(self) -> Agent:
        """
        Create the calendar definer agent.

        This agent analyzes study plans and defines the overall structure and
        framework for study calendars. It determines appropriate time blocks,
        learning phases, milestones, and scheduling constraints based on the
        study plan requirements and user preferences.

        Returns
        -------
        Agent
            The calendar definer agent instance configured with Azure OpenAI model
            and settings from agents_config["calendar_definer"]

        Notes
        -----
        The calendar definer agent is responsible for:
        - Analyzing study plan content and time requirements
        - Defining calendar structure and time allocation strategies
        - Identifying key milestones and checkpoint dates
        - Establishing learning phases and progression stages
        - Considering optimal spacing for different types of learning activities
        - Setting realistic timeframes based on content complexity
        """
        return Agent(
            config=self.agents_config["calendar_definer"],
            llm=self.model,
        )
    @agent
    def calendar_writer(self) -> Agent:
        """
        Create the calendar writer agent.

        This agent takes the defined calendar structure and creates detailed,
        specific calendar entries with learning activities, assignments, and
        milestones. It transforms the abstract calendar framework into concrete,
        actionable daily and weekly schedules.

        Returns
        -------
        Agent
            The calendar writer agent instance configured with Azure OpenAI model
            and settings from agents_config["calendar_writer"]

        Notes
        -----
        The calendar writer agent is responsible for:
        - Creating detailed daily and weekly schedule entries
        - Specifying concrete learning activities and tasks
        - Adding specific deadlines and milestone dates
        - Organizing activities for optimal learning progression
        - Including review sessions and spaced repetition schedules
        - Balancing study load across different time periods
        - Adding buffer time for review and consolidation
        """
        return Agent(
            config=self.agents_config["calendar_writer"],
            llm=self.model,
        )

    @task
    def define_calendar(self) -> Task:
        """
        Create the define calendar task.

        This task handles the analysis of study plan requirements and the
        definition of the calendar structure, time allocation framework,
        and scheduling constraints for the study calendar.

        Returns
        -------
        Task
            The define calendar task instance using configuration from
            tasks_config["define_calendar"]

        Notes
        -----
        This task is typically the first in the calendar creation pipeline.
        It establishes the foundation for detailed calendar content creation
        by defining:
        - Overall time structure and learning phases
        - Milestone dates and checkpoint schedules
        - Time allocation strategies for different topics
        - Scheduling constraints and preferences
        """
        return Task(
            config=self.tasks_config["define_calendar"],
        )
    @task
    def write_calendar(self) -> Task:
        """
        Create the write calendar task.

        This task handles the creation of detailed calendar content based on
        the defined structure. It transforms the calendar framework into
        specific, actionable daily and weekly schedules with concrete activities.

        Returns
        -------
        Task
            The write calendar task instance using configuration from
            tasks_config["write_calendar"]

        Notes
        -----
        This task builds upon the output of the define_calendar task to create
        comprehensive calendar content including:
        - Detailed daily and weekly schedules
        - Specific learning activities and assignments
        - Milestone dates and deadline reminders
        - Review sessions and spaced repetition schedules
        - Progress tracking checkpoints
        """
        return Task(
            config=self.tasks_config["write_calendar"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Calendar Crew.

        Assembles all agents and tasks into a sequential crew for comprehensive
        study calendar creation and scheduling. The crew transforms study plans
        into concrete, time-bound schedules with specific learning activities.

        Returns
        -------
        Crew
            The Calendar Crew instance with all agents and tasks configured
            for sequential processing with verbose logging enabled

        Notes
        -----
        The crew uses sequential processing where tasks are executed in order:
        1. Define calendar - Analyze requirements and create calendar structure
        2. Write calendar - Create detailed schedule content and activities

        Verbose mode is enabled for detailed logging of the calendar creation
        process. The crew ensures optimal time allocation and realistic
        scheduling that supports effective learning progression.

        The calendar creation workflow:
        - Receives study plan input with learning objectives
        - Analyzes time requirements and complexity of topics
        - Defines appropriate calendar structure and milestones
        - Creates detailed daily/weekly schedules with specific activities
        - Optimizes schedule for learning effectiveness and retention

        Examples
        --------
        >>> crew_instance = self.crew()
        >>> inputs = {
        ...     "plan": "Data Science study plan",
        ...     "duration": "3 months",
        ...     "availability": "15 hours per week"
        ... }
        >>> result = crew_instance.kickoff(inputs=inputs)
        >>> # Result contains detailed study calendar with daily/weekly activities
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
