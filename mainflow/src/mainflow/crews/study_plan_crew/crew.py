from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class FinalStudyPlanCrew:
    """
    Final Study Plan Crew for Academic Learning Management.

    This crew specializes in creating, formatting, and reviewing final study plans
    for academic purposes. It combines multiple specialized agents to produce
    comprehensive, well-structured, and visually appealing study plans that
    integrate all previously gathered information and resources.

    The final study plan creation process involves:
    - Consolidating information from previous crews (planning, web search, papers)
    - Filling in detailed study plan content with specific activities
    - Creating ASCII art and visual formatting for enhanced presentation
    - Reviewing and validating the final study plan for completeness and quality

    Attributes
    ----------
    agents : List[BaseAgent]
        List of specialized agent instances for the crew
    tasks : List[Task]
        List of task instances to be executed by the crew
    agents_config : str
        Path to the agents configuration YAML file (config/agents.yaml)
    tasks_config : str
        Path to the tasks configuration YAML file (config/tasks.yaml)

    Methods
    -------
    final_plan_filler() -> Agent
        Creates the agent responsible for filling the final study plan with content
    ascii_writer() -> Agent
        Creates the agent responsible for ASCII art and visual formatting
    final_plan_reviewer() -> Agent
        Creates the agent responsible for reviewing and validating the final plan
    fill_final_plan() -> Task
        Creates the task for filling the study plan with detailed content
    write_ascii() -> Task
        Creates the task for adding ASCII art and visual elements
    review_final_plan() -> Task
        Creates the task for final review and validation
    crew() -> Crew
        Creates and returns the complete crew configuration

    Examples
    --------
    >>> final_crew = FinalStudyPlanCrew()
    >>> inputs = {
    ...     "plan": "Machine Learning study plan",
    ...     "resources": "Online courses and tutorials",
    ...     "papers": "Research papers on ML algorithms",
    ...     "calendar": "6-month timeline"
    ... }
    >>> result = final_crew.crew().kickoff(inputs=inputs)
    >>> print(result.raw)

    Notes
    -----
    This crew represents the final stage in the study plan creation pipeline.
    It consolidates all information from previous crews to create a comprehensive
    final study plan. The crew uses sequential processing and outputs the final
    plan to a markdown file for easy sharing and reference.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def final_plan_filler(self) -> Agent:
        """
        Create the final plan filler agent.

        This agent is responsible for consolidating all information from previous
        crews (planning, web resources, academic papers, calendar) and filling
        the final study plan with comprehensive, detailed content.

        Returns
        -------
        Agent
            The plan filler agent instance configured with settings from
            agents_config["final_plan_filler"]

        Notes
        -----
        The final plan filler agent performs the following functions:
        - Integrates information from all previous crew outputs
        - Creates detailed learning activities and milestones
        - Organizes content in a logical, progressive structure
        - Ensures completeness and coherence of the study plan
        - Adds specific timelines and learning objectives
        """
        return Agent(
            config=self.agents_config["final_plan_filler"],
        )

    @agent
    def ascii_writer(self) -> Agent:
        """
        Create the ASCII writer agent.

        This agent specializes in creating ASCII art, visual formatting, and
        enhancing the presentation of the study plan to make it more engaging
        and visually appealing.

        Returns
        -------
        Agent
            The ASCII writer agent instance configured with settings from
            agents_config["ascii_writer"]

        Notes
        -----
        The ASCII writer agent is responsible for:
        - Creating ASCII art headers and dividers
        - Adding visual elements and formatting
        - Enhancing readability with structured layouts
        - Creating progress bars and visual timelines
        - Adding decorative elements to improve engagement
        """
        return Agent(
            config=self.agents_config["ascii_writer"],
        )

    @agent
    def final_plan_reviewer(self) -> Agent:
        """
        Create the final plan reviewer agent.

        This agent performs comprehensive quality assurance on the final study
        plan, ensuring completeness, accuracy, and adherence to best practices
        in educational planning.

        Returns
        -------
        Agent
            The plan reviewer agent instance configured with settings from
            agents_config["final_plan_reviewer"]

        Notes
        -----
        The final plan reviewer agent validates:
        - Completeness of all study plan sections
        - Logical flow and progression of learning activities
        - Accuracy and relevance of included resources
        - Appropriate time allocation and realistic timelines
        - Alignment with original learning objectives
        - Quality of formatting and presentation
        """
        return Agent(
            config=self.agents_config["final_plan_reviewer"],
        )

    @task
    def fill_final_plan(self) -> Task:
        """
        Create the fill final plan task.

        This task handles the consolidation and integration of all information
        from previous crews to create a comprehensive, detailed final study plan.

        Returns
        -------
        Task
            The fill plan task instance using configuration from
            tasks_config["fill_final_plan"]

        Notes
        -----
        This task is the core content creation step that:
        - Combines outputs from planning, web search, papers, and calendar crews
        - Creates detailed learning activities and assignments
        - Establishes clear learning objectives and outcomes
        - Organizes content into logical modules or sections
        - Provides specific timelines and milestones
        """
        return Task(
            config=self.tasks_config["fill_final_plan"],
        )

    @task
    def write_ascii(self) -> Task:
        """
        Create the write ASCII task.

        This task handles the visual formatting and enhancement of the study
        plan with ASCII art, decorative elements, and improved layout structure.

        Returns
        -------
        Task
            The write ASCII task instance using configuration from
            tasks_config["write_ascii"]

        Notes
        -----
        This task enhances the study plan with:
        - ASCII art headers and section dividers
        - Visual progress indicators and timelines
        - Formatted tables and lists
        - Decorative elements for improved engagement
        - Structured layout for better readability
        """
        return Task(
            config=self.tasks_config["write_ascii"],
        )

    @task
    def review_final_plan(self) -> Task:
        """
        Create the review final plan task.

        This task performs the final quality assurance and validation of the
        complete study plan before output. It ensures the plan meets all
        requirements and quality standards.

        Returns
        -------
        Task
            The review plan task instance using configuration from
            tasks_config["review_final_plan"], with output directed to
            "output/final_study_plan.md"

        Notes
        -----
        This is the final task in the pipeline that:
        - Validates completeness and accuracy of the study plan
        - Ensures proper formatting and presentation
        - Checks for consistency and logical flow
        - Verifies alignment with learning objectives
        - Outputs the final plan to a markdown file
        - Provides final recommendations and improvements
        """
        return Task(
            config=self.tasks_config["review_final_plan"],
            output_file="output/final_study_plan.md",
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Final Study Plan Crew.

        Assembles all agents and tasks into a sequential crew for comprehensive
        final study plan creation, formatting, and quality assurance.

        Returns
        -------
        Crew
            The Final Study Plan Crew instance with all agents and tasks
            configured for sequential processing with verbose logging enabled

        Notes
        -----
        The crew uses sequential processing where tasks are executed in order:
        1. Fill final plan - Consolidate all information and create detailed content
        2. Write ASCII - Add visual formatting and ASCII art elements
        3. Review final plan - Quality assurance and final validation

        The final output is written to "output/final_study_plan.md" for easy
        access and sharing. Verbose mode provides detailed logging of the
        creation process.

        This crew represents the culmination of the entire study plan creation
        pipeline, producing a comprehensive, well-formatted, and thoroughly
        reviewed final study plan.

        Examples
        --------
        >>> crew_instance = self.crew()
        >>> inputs = {
        ...     "plan": "Comprehensive ML study plan",
        ...     "resources": "Curated online resources",
        ...     "papers": "Academic research papers",
        ...     "calendar": "Detailed timeline"
        ... }
        >>> result = crew_instance.kickoff(inputs=inputs)
        >>> # Final study plan will be saved to output/final_study_plan.md
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
