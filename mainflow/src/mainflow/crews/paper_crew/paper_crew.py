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
    """
    Academic Paper Research Crew for ArXiv Paper Discovery.
    
    This crew specializes in scientific literature research, focusing on identifying,
    extracting, and searching for relevant academic papers from ArXiv. It combines
    multiple agents to provide comprehensive paper discovery capabilities.
    
    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agents for paper research tasks
    tasks : List[Task]
        List of tasks to be executed by the crew
    
    Methods
    -------
    scientific_topic_identifier()
        Creates an agent for identifying scientific topics from user input
    keyword_extractor()
        Creates an agent for extracting relevant keywords
    query_validator()
        Creates an agent for validating search queries
    arxiv_searcher()
        Creates an agent for searching ArXiv papers
    scientific_topic_extraction_task()
        Creates a task for extracting scientific topics
    keyword_extraction_task()
        Creates a task for extracting search keywords
    validate_query_task()
        Creates a task for validating search queries
    perform_search_task()
        Creates a task for performing ArXiv searches
    crew()
        Creates and returns the complete crew configuration
    
    Notes
    -----
    This crew uses sequential processing where each agent builds upon the work
    of the previous one to create an effective paper discovery pipeline.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def scientific_topic_identifier(self) -> Agent:
        """
        Create a scientific topic identification agent.
        
        This agent analyzes user input to identify the core scientific topics
        and research areas that should be explored.
        
        Returns
        -------
        Agent
            An agent configured to identify scientific topics from text input
            
        Notes
        -----
        The agent uses configuration from the YAML file to define its behavior
        and capabilities for topic identification.
        """
        return Agent(
            config=self.agents_config['scientific_topic_identifier'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def keyword_extractor(self) -> Agent:
        """
        Create a keyword extraction agent.
        
        This agent extracts relevant keywords and search terms from identified
        scientific topics to optimize ArXiv search queries.
        
        Returns
        -------
        Agent
            An agent configured to extract keywords for academic search
            
        Notes
        -----
        The agent focuses on extracting domain-specific terminology and
        research-relevant keywords that will improve search effectiveness.
        """
        return Agent(
            config=self.agents_config['keyword_extractor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def query_validator(self) -> Agent:
        """
        Create a search query validation agent.
        
        This agent validates and optimizes search queries to ensure they are
        well-formed and likely to return relevant results from ArXiv.
        
        Returns
        -------
        Agent
            An agent configured to validate and optimize search queries
            
        Notes
        -----
        The agent checks query syntax, relevance, and potential effectiveness
        before the actual search is performed.
        """
        return Agent(
            config=self.agents_config['query_validator'], # type: ignore[index]
            verbose=True
        )

    @agent
    def arxiv_searcher(self) -> Agent:
        """
        Create an ArXiv search agent.
        
        This agent performs the actual search on ArXiv using validated queries
        and returns relevant academic papers.
        
        Returns
        -------
        Agent
            An agent configured to search ArXiv with arxiv_searcher_tool
            
        Notes
        -----
        The agent is equipped with the arxiv_searcher_tool to interact with
        the ArXiv API and retrieve academic papers.
        """
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
        """
        Create a scientific topic extraction task.
        
        This task processes user input to identify and extract the main
        scientific topics and research areas of interest.
        
        Returns
        -------
        Task
            A task configured to extract scientific topics from user input
            
        Notes
        -----
        This is typically the first task in the pipeline, providing the
        foundation for subsequent keyword extraction and search operations.
        """
        return Task(
            config=self.tasks_config['scientific_topic_extraction_task'], # type: ignore[index]
        )
    
    @task
    def keyword_extraction_task(self) -> Task:
        """
        Create a keyword extraction task.
        
        This task takes identified scientific topics and extracts relevant
        keywords and search terms for ArXiv queries.
        
        Returns
        -------
        Task
            A task configured to extract keywords from scientific topics
            
        Notes
        -----
        The task builds upon the output of the topic extraction task to
        create search-optimized keywords.
        """
        return Task(
            config=self.tasks_config['keyword_extraction_task'], # type: ignore[index]
        )

    @task
    def validate_query_task(self) -> Task:
        """
        Create a query validation task.
        
        This task validates and optimizes the extracted keywords into
        well-formed search queries suitable for ArXiv.
        
        Returns
        -------
        Task
            A task configured to validate and optimize search queries
            
        Notes
        -----
        The task ensures that search queries are syntactically correct
        and likely to return relevant academic papers.
        """
        return Task(
            config=self.tasks_config['validate_query_task'], # type: ignore[index]
        )

    @task
    def perform_search_task(self) -> Task:
        """
        Create an ArXiv search task.
        
        This task executes the validated search queries against ArXiv
        and retrieves relevant academic papers.
        
        Returns
        -------
        Task
            A task configured to perform ArXiv searches and retrieve papers
            
        Notes
        -----
        This is the final task in the pipeline that produces the actual
        search results from ArXiv.
        """
        return Task(
            config=self.tasks_config['perform_search_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Paper Research Crew.
        
        Assembles all agents and tasks into a sequential crew for academic
        paper discovery and research.
        
        Returns
        -------
        Crew
            A configured crew with all agents and tasks for paper research
            
        Notes
        -----
        The crew uses sequential processing where each task depends on the
        output of the previous task. Verbose mode is enabled for detailed
        logging of the research process.
        
        The pipeline flow is:
        1. Extract scientific topics from user input
        2. Extract relevant keywords from topics
        3. Validate and optimize search queries
        4. Perform ArXiv search and retrieve papers
        """
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
