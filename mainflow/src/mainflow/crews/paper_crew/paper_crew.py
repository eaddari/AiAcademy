from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from mainflow.tools.arxiv_searcher_tool import arxiv_searcher_tool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class PaperCrew():
    """PaperCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def scientific_topic_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config['scientific_topic_identifier'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def keyword_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['keyword_extractor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def query_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['query_validator'], # type: ignore[index]
            verbose=True
        )

    @agent
    def arxiv_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['arxiv_searcher'], # type: ignore[index]
            verbose=True,
            tools=[arxiv_searcher_tool], # type: ignore[index]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def scientific_topic_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['scientific_topic_extraction_task'], # type: ignore[index]
        )
    
    @task
    def keyword_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['keyword_extraction_task'], # type: ignore[index]
        )

    @task
    def validate_query_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_query_task'], # type: ignore[index]
        )

    @task
    def perform_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['perform_search_task'], # type: ignore[index]
            output_file='paper_crew_result.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PaperCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
