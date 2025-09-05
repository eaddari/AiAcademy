from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class PlanningCrew:
    """
    Study Planning Crew

    Defines a crew that plans, writes, and reviews a study plan according to given requirements.
    The crew is composed of three agents: a plan definer, a plan writer, and a plan reviewer.
    The crew executes three tasks: define the plan, write the plan, and review the plan.

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

    @agent
    def plan_definer(self) -> Agent:
        """
        Create the plan definer agent.

        Returns
        -------
        Agent
            The plan definer agent instance.
        """
        return Agent(
            config=self.agents_config["plan_definer"],
        )
    @agent
    def plan_writer(self) -> Agent:
        """
        Create the plan writer agent.

        Returns
        -------
        Agent
            The plan writer agent instance.
        """
        return Agent(
            config=self.agents_config["plan_writer"],
        )
    @agent
    def plan_reviewer(self) -> Agent:
        """
        Create the plan reviewer agent.

        Returns
        -------
        Agent
            The plan reviewer agent instance.
        """
        return Agent(
            config=self.agents_config["plan_reviewer"],
        )
    
    @task
    def define_plan(self) -> Task:
        """
        Create the define plan task.

        Returns
        -------
        Task
            The define plan task instance.
        """
        return Task(
            config=self.tasks_config["define_plan"],
        )
    @task
    def write_plan(self) -> Task:
        """
        Create the write plan task.

        Returns
        -------
        Task
            The write plan task instance.
        """
        return Task(
            config=self.tasks_config["write_plan"],
        )
    @task
    def review_plan(self) -> Task:
        """
        Create the review plan task.

        Returns
        -------
        Task
            The review plan task instance.
        """
        return Task(
            config=self.tasks_config["review_plan"],
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
