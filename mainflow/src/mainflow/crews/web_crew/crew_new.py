# src/mainflow/crews/web_crew/crew.py
from __future__ import annotations

import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from src.mainflow.tools.custom_tool import SerperSearchTool
from typing import List
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv("C:\\desktopnoonedrive\\gruppo-finale\\AiAcademy\\mainflow\\.env")
search_tool = SerperSearchTool()
@CrewBase
class WebCrew:
    """
    Web Research Crew

    Takes the study plan from the planning crew and enhances it with
    relevant web resources using Serper search tool. Focuses on finding
    trustworthy educational resources and official documentation.

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

    def __init__(self) -> None:
        # Set up Azure OpenAI environment variables
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string for Azure OpenAI
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"

    @agent
    def web_researcher(self) -> Agent:
        """
        Create the web researcher agent.

        Returns
        -------
        Agent
            The web researcher agent instance with Serper tool.
        """
        return Agent(
            config=self.agents_config["web_researcher"],
            tools=[search_tool],
            llm=self.model,
        )

    @task
    def web_search_task(self) -> Task:
        """
        Create the web search task.

        Returns
        -------
        Task
            The web search task instance.
        """
        return Task(
            config=self.tasks_config["web_search_task"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the Web Research Crew.

        Returns
        -------
        Crew
            The Web Research Crew instance with all agents and tasks.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
