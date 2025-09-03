from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from tools.custom_tool import LocalRag
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

@CrewBase
class ExplanationCrew():
    """Explanation crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def agent_manager(self) -> Agent:
        """
        Manages the agent's tasks and responsibilities by deciding how to write the explanation of the topic.
        """
        return Agent(
            config=self.agents_config['agent_manager'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )
        
    @agent
    def expert_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_writer'], # type: ignore[index]
            verbose=True
        )

    @task
    def agent_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['agent_manager_task'] # type: ignore[index]
        )
        
    @task
    def web_researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_research_task'] # type: ignore[index]
        )
        
    @task
    def expert_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['expert_writer_task'] # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Explanation crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
