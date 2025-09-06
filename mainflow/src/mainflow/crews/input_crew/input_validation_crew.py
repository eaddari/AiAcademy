from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
#load_dotenv("C:\\Users\\ZR184CB\\OneDrive - EY\\Documents\\GitHub\\AiAcademy\\mainflow\\src\\mainflow\\crews\\input_crew\\.env")
load_dotenv("mainflow\\.env")

@CrewBase
class InputValidationCrew:
    """Input Validation Crew for Academic Research"""
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self): 
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"
        
    @agent
    def input_sanitizer(self) -> Agent:
        return Agent(
            config=self.agents_config["input_sanitizer"],
            llm=self.model,
        )
    
    #the ethics checker agent should check that the cleaned input is appropriate
    @agent
    def ethics_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["ethics_checker"],
            llm=self.model,
        )

    @agent
    def role_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config["role_identifier"],
            llm=self.model,
        )
    @agent
    def knowledge_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config["knowledge_identifier"],
            llm=self.model,
        )
    
    @agent
    def security_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["security_validator"],
            llm=self.model,
        )
    @agent
    def final_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["final_validator"],
            llm=self.model,
        )
    
    @task
    def sanitize_input(self) -> Task:
        return Task(
            config=self.tasks_config["sanitize_input"],
        )

    @task
    def check_academic_ethics(self) -> Task:
        return Task(
            config=self.tasks_config["check_academic_ethics"],
        )

    @task
    def validate_security(self) -> Task:
        return Task(
            config=self.tasks_config["validate_security"],
        )
    @task
    def individuate_role(self) -> Task:
        return Task(
            config=self.tasks_config["individuate_role"],
        )
    @task
    def individuate_knowledge(self) -> Task:
        return Task(
            config=self.tasks_config["individuate_knowledge"],
        )
    @task
    def final_validation(self) -> Task:
        return Task(
            config=self.tasks_config["final_validation"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Input Validation Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
