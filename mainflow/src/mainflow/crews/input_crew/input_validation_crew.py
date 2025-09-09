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
    """
    Input Validation Crew for Academic Research.
    
    This crew handles the validation, sanitization, and analysis of user input
    for academic research purposes. It includes multiple agents that work together
    to ensure input quality, ethics compliance, and security validation.
    
    Attributes
    ----------
    agents : List[BaseAgent]
        List of agents in the crew
    tasks : List[Task]
        List of tasks to be executed by the crew
    model : str
        Azure OpenAI model configuration string
    
    Methods
    -------
    input_sanitizer()
        Creates an agent for input sanitization
    ethics_checker()
        Creates an agent for academic ethics validation
    role_identifier()
        Creates an agent for identifying user roles
    knowledge_identifier()
        Creates an agent for identifying knowledge domains
    goals_identifier()
        Creates an agent for identifying user goals
    security_validator()
        Creates an agent for security validation
    final_validator()
        Creates an agent for final validation
    crew()
        Creates and returns the complete crew configuration
    """
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self): 
        """
        Initialize the InputValidationCrew.
        
        Sets up Azure OpenAI configuration and model string from environment variables.
        
        Notes
        -----
        Requires the following environment variables:
        - AZURE_OPENAI_API_KEY
        - AZURE_OPENAI_ENDPOINT
        - AZURE_DEPLOYMENT_NAME
        """
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_API_VERSION"] = "2024-12-01-preview"
        
        # Create model string
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"
        
    @agent
    def input_sanitizer(self) -> Agent:
        """
        Create an input sanitization agent.
        
        Returns
        -------
        Agent
            An agent configured to sanitize and clean user input
        """
        return Agent(
            config=self.agents_config["input_sanitizer"],
            llm=self.model,
        )
    
    @agent
    def ethics_checker(self) -> Agent:
        """
        Create an ethics checking agent.
        
        The ethics checker agent validates that the cleaned input is appropriate
        and complies with academic ethics standards.
        
        Returns
        -------
        Agent
            An agent configured to check academic ethics compliance
        """
        return Agent(
            config=self.agents_config["ethics_checker"],
            llm=self.model,
        )

    @agent
    def role_identifier(self) -> Agent:
        """
        Create a role identification agent.
        
        Returns
        -------
        Agent
            An agent configured to identify user roles and responsibilities
        """
        return Agent(
            config=self.agents_config["role_identifier"],
            llm=self.model,
        )
    
    @agent
    def knowledge_identifier(self) -> Agent:
        """
        Create a knowledge domain identification agent.
        
        Returns
        -------
        Agent
            An agent configured to identify relevant knowledge domains
        """
        return Agent(
            config=self.agents_config["knowledge_identifier"],
            llm=self.model,
        )
    
    @agent
    def goals_identifier(self) -> Agent:
        """
        Create a goals identification agent.
        
        Returns
        -------
        Agent
            An agent configured to identify and analyze user goals
        """
        return Agent(
            config=self.agents_config["goals_identifier"],
            llm=self.model,
        )
    
    @agent
    def security_validator(self) -> Agent:
        """
        Create a security validation agent.
        
        Returns
        -------
        Agent
            An agent configured to validate security aspects of user input
        """
        return Agent(
            config=self.agents_config["security_validator"],
            llm=self.model,
        )
    
    @agent
    def final_validator(self) -> Agent:
        """
        Create a final validation agent.
        
        Returns
        -------
        Agent
            An agent configured to perform final validation of processed input
        """
        return Agent(
            config=self.agents_config["final_validator"],
            llm=self.model,
        )
    
    @task
    def sanitize_input(self) -> Task:
        """
        Create an input sanitization task.
        
        Returns
        -------
        Task
            A task configured to sanitize user input
        """
        return Task(
            config=self.tasks_config["sanitize_input"],
        )

    @task
    def check_academic_ethics(self) -> Task:
        """
        Create an academic ethics checking task.
        
        Returns
        -------
        Task
            A task configured to validate academic ethics compliance
        """
        return Task(
            config=self.tasks_config["check_academic_ethics"],
        )

    @task
    def validate_security(self) -> Task:
        """
        Create a security validation task.
        
        Returns
        -------
        Task
            A task configured to validate security aspects
        """
        return Task(
            config=self.tasks_config["validate_security"],
        )
    
    @task
    def individuate_role(self) -> Task:
        """
        Create a role identification task.
        
        Returns
        -------
        Task
            A task configured to identify user roles
        """
        return Task(
            config=self.tasks_config["individuate_role"],
        )
    
    @task
    def individuate_knowledge(self) -> Task:
        """
        Create a knowledge domain identification task.
        
        Returns
        -------
        Task
            A task configured to identify knowledge domains
        """
        return Task(
            config=self.tasks_config["individuate_knowledge"],
        )
    
    @task
    def individuate_goals(self) -> Task:
        """
        Create a goals identification task.

        Returns
        -------
        Task
            A task configured to identify user goals
        """
        return Task(
            config=self.tasks_config["individuate_goals"],
        )
    
    @task
    def final_validation(self) -> Task:
        """
        Create a final validation task.
        
        Returns
        -------
        Task
            A task configured to perform final validation
        """
        return Task(
            config=self.tasks_config["final_validation"],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Input Validation Crew.
        
        Assembles all agents and tasks into a sequential crew for input validation.
        
        Returns
        -------
        Crew
            A configured crew with all agents and tasks for input validation
            
        Notes
        -----
        The crew uses sequential processing where tasks are executed one after another.
        Verbose mode is enabled for detailed logging.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
