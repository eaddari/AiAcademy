from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class FinalStudyPlanCrew:
    """
    Final Study Plan Crew

    Defines a crew that fills, writes, and reviews the final study plan according to given requirements.
    The crew is composed of three agents: a plan filler, an ASCII writer, and a plan reviewer.
    The crew executes three tasks: fill the plan, write ASCII, and review the plan.

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
    def final_plan_filler(self) -> Agent:
        """
        Create the final plan filler agent.

        Returns
        -------
        Agent
            The plan filler agent instance.
        """
        return Agent(
            config=self.agents_config["plan_filler"],
        )
    @agent
    def ascii_writer(self) -> Agent:
        """
        Create the ASCII writer agent.

        Returns
        -------
        Agent
            The ASCII writer agent instance.
        """
        return Agent(
            config=self.agents_config["ascii_writer"],
        )
    @agent
    def final_plan_reviewer(self) -> Agent:
        """
        Create the final plan reviewer agent.

        Returns
        -------
        Agent
            The plan reviewer agent instance.
        """
        return Agent(
            config=self.agents_config["plan_reviewer"],
        )
    
    @task
    def fill_final_plan(self) -> Task:
        """
        Create the fill final plan task.

        Returns
        -------
        Task
            The fill plan task instance.
        """
        return Task(
            config=self.tasks_config["fill_plan"],
        )
    @task
    def write_ascii(self) -> Task:
        """
        Create the write ASCII task.

        Returns
        -------
        Task
            The write ASCII task instance.
        """
        return Task(
            config=self.tasks_config["write_ascii"],
        )
    @task
    def review_final_plan(self) -> Task:
        """
        Create the review final plan task.

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
        Creates the Final Study Plan Crew.

        Returns
        -------
        Crew
            The Final Study Plan Crew instance with all agents and tasks.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
