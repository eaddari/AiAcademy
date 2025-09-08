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
    Calendar Crew

    Defines a crew that plans, writes, and reviews a study plan according to given requirements.
    The crew is composed of three agents: a calendar definer, a calendar writer, and a calendar reviewer.
    The crew executes three tasks: define the calendar, write the calendar, and review the calendar.

    Attributes
    ----------
    agents : list of BaseAgent
        List of agent instances for the crew.
    tasks : list of Task
        List of task instances for the crew.
    agents_config : str
        Path to the agents configuration YAML file.
    tasks_config : str
        Path to the tasks configuration YAML file.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self): 
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"

    @agent
    def calendar_definer(self) -> Agent:
        """
        Create the calendar definer agent.

        Returns
        -------
        Agent
            The calendar definer agent instance.
        """
        return Agent(
            config=self.agents_config["calendar_definer"],
            llm=self.model,
        )
    @agent
    def calendar_writer(self) -> Agent:
        """
        Create the calendar writer agent.

        Returns
        -------
        Agent
            The calendar writer agent instance.
        """
        return Agent(
            config=self.agents_config["calendar_writer"],
            llm=self.model,
        )

    @task
    def define_calendar(self) -> Task:
        """
        Create the define calendar task.

        Returns
        -------
        Task
            The define calendar task instance.
        """
        return Task(
            config=self.tasks_config["define_calendar"],
        )
    @task
    def write_calendar(self) -> Task:
        """
        Create the write calendar task.

        Returns
        -------
        Task
            The write calendar task instance.
        """
        return Task(
            config=self.tasks_config["write_calendar"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the Planning Crew.

        Returns
        -------
        Crew
            The Planning Crew instance with all agents and tasks.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
