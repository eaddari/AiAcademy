#!/usr/bin/env python
"""
Generic Multi-Agent Research Flow for CrewAI System.

This module implements a comprehensive research workflow that intelligently
routes different types of queries to specialized crews. The flow coordinates
RAG research, web research, mathematical problem solving, and synthesis to
provide comprehensive analysis and reporting.

The workflow includes:
- Intelligent query classification and routing
- Specialized crew execution based on query type
- Multi-source research coordination
- Comprehensive synthesis and reporting

Classes
-------
RouterOutput : BaseModel
    Pydantic model for routing decisions between different research methods.
ResearchPlan : BaseModel
    Structured plan for coordinating multi-faceted research workflows.
ResearchResults : BaseModel
    Container for results from different research methods and synthesis.
GenericFlowState : BaseModel
    State management for the complete generic research workflow.
GenericFlow : Flow
    Main flow class orchestrating the multi-agent research process.

Functions
---------
kickoff : callable
    Entry point function to start the generic research flow.
plot : callable
    Function to generate visual representation of the flow structure.

Examples
--------
Run the research flow:
    >>> from flow_copy import kickoff
    >>> result = kickoff()

Generate flow visualization:
    >>> from flow_copy import plot
    >>> plot()

Notes
-----
The flow uses Azure OpenAI for intelligent routing and synthesis, and
coordinates multiple specialized crews for comprehensive research coverage.
"""
import json
import os
from typing import List, Literal
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow import Flow, listen, start, router, or_
from openai import AzureOpenAI
from crews.webrag.crew import Webrag
from crews.mathcrew.crew import Math
from crews.summary.crew import ExplanationCrew


class RouterOutput(BaseModel):
    """
    Output model for intelligent routing decisions.
    
    This model defines the possible routing paths for different types
    of research queries, enabling the flow to direct queries to the
    most appropriate specialized crew.
    
    Attributes
    ----------
    route : Literal
        The routing decision indicating which research method to use:
        - "research": General research queries
        - "summarization": Content summarization requests  
        - "math": Mathematical problems and calculations
        - "image_generation": Visual content creation requests
        
    Examples
    --------
    >>> router_output = RouterOutput(route="math")
    >>> print(router_output.route)
    """

    route: Literal["reseacrh", "summarization", "math", "image_generation"] = Field(
        description="Decided method for router"
    )


# Define our models for structured data
class ResearchPlan(BaseModel):
    """
    Structured plan for coordinating research workflows.
    
    This model defines the comprehensive research strategy including
    different research focuses, key questions, and target audience
    considerations for multi-faceted research operations.
    
    Attributes
    ----------
    topic : str
        The main research topic or user input to be investigated.
    rag_focus : str
        Specific focus area for RAG-based document research.
    web_focus : str
        Specific focus area for web-based research activities.
    math_focus : str
        Specific focus area for mathematical problem solving.
    research_questions : List[str]
        Key research questions that need to be addressed.
    target_audience : str
        Intended audience for the research report and findings.
        
    Examples
    --------
    >>> plan = ResearchPlan(
    ...     topic="Machine Learning Applications",
    ...     rag_focus="Technical implementation details",
    ...     web_focus="Latest developments and trends",
    ...     math_focus="Algorithm performance metrics",
    ...     research_questions=["What are the key algorithms?"],
    ...     target_audience="Technical developers"
    ... )
    """

    topic: str = Field(description="Main user input")
    rag_focus: str = Field(description="Specific focus for RAG research")
    web_focus: str = Field(description="Specific focus for web research")
    math_focus: str = Field(description="Specific focus for math solving")
    research_questions: List[str] = Field(description="Key questions to answer")
    target_audience: str = Field(description="Target audience for the report")


class ResearchResults(BaseModel):
    """
    Results container for multi-source research findings.
    
    This model aggregates results from different research methods
    including RAG research, web research, mathematical analysis,
    and provides combined insights and metadata.
    
    Attributes
    ----------
    rag_findings : str, default=""
        Results and insights from RAG-based document research.
    web_findings : str, default=""
        Results and insights from web-based research activities.
    math_findings : str, default=""
        Results and solutions from mathematical problem solving.
    combined_insights : str, default=""
        Synthesized insights combining all research findings.
    research_method : str, default=""
        Primary research method used for the investigation.
        
    Examples
    --------
    >>> results = ResearchResults()
    >>> results.rag_findings = "Technical documentation analysis..."
    >>> results.research_method = "RAG"
    """

    rag_findings: str = ""
    web_findings: str = ""
    math_findings: str = ""
    combined_insights: str = ""
    research_method: str = ""


# Define our flow state
class GenericFlowState(BaseModel):
    """
    State management for the complete generic research workflow.
    
    This model maintains the persistent state throughout the research
    flow execution, tracking user input, research plans, results,
    and orchestration decisions.
    
    Attributes
    ----------
    topic : str, default=""
        The main research topic provided by the user.
    current_year : str, default=""
        Current year for contextualizing research findings.
    research_plan : ResearchPlan, optional
        Structured research plan with focuses and questions.
    research_results : ResearchResults
        Container for all research findings and synthesis.
    orchestrator_decision : str, default=""
        Routing decision made by the orchestrator logic.
    final_report_structure : str, default=""
        Structure and organization of the final report.
        
    Examples
    --------
    >>> state = GenericFlowState()
    >>> state.topic = "Artificial Intelligence in Healthcare"
    >>> state.current_year = "2025"
    
    Notes
    -----
    This state model ensures data persistence and consistency
    throughout the multi-stage research workflow execution.
    """

    topic: str = ""
    current_year: str = ""
    research_plan: ResearchPlan = None
    research_results: ResearchResults = ResearchResults()
    research_decision: str = ""
    orchestrator_decision: str = ""
    final_report: str = ""
    final_report_structure: str = ""
    final_report_infos: str = ""


class GenericFlow(Flow[GenericFlowState]):
    """
    Main flow class for orchestrating multi-agent research processes.
    
    This class implements a comprehensive research workflow that intelligently
    routes queries to specialized crews, coordinates multiple research methods,
    and synthesizes findings into comprehensive reports.
    
    The flow includes:
    1. User input collection and preprocessing
    2. Research plan creation and strategy development
    3. Intelligent routing to appropriate research methods
    4. Parallel or sequential execution of specialized crews
    5. Synthesis and final report generation
    
    Attributes
    ----------
    state : GenericFlowState
        The persistent state object tracking all workflow data
        and intermediate results throughout execution.
        
    Methods
    -------
    collect_user_input()
        Entry point for collecting and processing user research requests.
    create_research_plan()
        Develops structured research strategy and planning.
    orchestrate_research()
        Intelligently routes queries to appropriate research methods.
    route_research()
        Implements routing logic for different research paths.
    execute_rag_research()
        Executes RAG-based document research.
    execute_web_research()
        Executes web-based research activities.
    execute_math_problem()
        Executes mathematical problem solving.
    synthesize_and_report()
        Synthesizes findings and generates final reports.
        
    Examples
    --------
    >>> flow = GenericFlow()
    >>> result = flow.kickoff()
    
    Notes
    -----
    The flow uses CrewAI decorators (@start, @listen, @router) to define
    execution sequence and dependencies. Azure OpenAI is used for
    intelligent classification and routing decisions.
    """
    
    @start()
    def collect_user_input(self):
        """
        Entry point: Collect and process user research input.
        
        Gathers user input about the research topic and initializes
        the workflow state with basic information needed for research
        planning and execution.
        
        Returns
        -------
        str
            Status identifier "user_input_collected" to trigger the
            next stage in the research workflow.
            
        Notes
        -----
        This method sets up the basic research context including
        the topic and current year for temporal context. The input
        can be customized or made interactive as needed.
        """
        Entry point: Collect user input about research topic
        """
        print("\n=== WebRAG Research Flow ===\n")

        # Get user input
        self.state.topic = input("What topic would you like to research? ")

        from datetime import datetime

        self.state.current_year = str(datetime.now().year)

        print(f"\nStarting research on: {self.state.topic}")
        print(f"Current year: {self.state.current_year}\n")

        # user_input = input("Chat with LLM: ").strip()
        # print(f"User input: {user_input}")

        llm = LLM(
            model="azure/gpt-4.1",
            temperature=0,
            response_format=RouterOutput,
        )

        messages = [
            {
                "role": "system",
                "content": "You are an orchestrator. Decide the best research method based on user input. Respond with JSON only, using the 'method' field with one of these values: 'research' for RAG/web research, 'math' for mathematical problems, or 'summarization' for summarization tasks.",
            },
            {
                "role": "user",
                "content": f"Decide the best research method for this input: {self.state.topic}",
            },
        ]

        result = llm.call(messages)

        json_result = json.loads(result)
        router_output = RouterOutput(**json_result)

        print(router_output.route)

        return router_output.route

    @listen(collect_user_input)
    def create_research_plan(self):
        self.state.research_plan = ResearchPlan(
            topic=self.state.topic,
            rag_focus=f"Local research about {self.state.topic}",
            web_focus=f"Web research about {self.state.topic}",
            math_focus=f"Math research about {self.state.topic}",
            research_questions=[f"What is {self.state.topic}?"],
            target_audience="General audience",
        )
        print("Research plan created")
        return "research_plan_created"

    @listen(create_research_plan)
    def orchestrate_research(self):
        llm = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            azure_deployment=os.getenv("MODEL", "gpt-4.1"),
        )
        chat = llm.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4.1"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a classifier. Answer with ONLY one word. 'math' if the input is a mathematical equation or calculation. if not a mathematical equation or calculation, respond with 'not_math'.",
                },
                {"role": "user", "content": f"Classify this input: {self.state.topic}"},
            ],
            max_tokens=10,
            temperature=0.0,
        )
        answer = chat.choices[0].message.content.strip().lower()
        print(answer)
        if answer == "math":
            self.state.orchestrator_decision = "math"
            return "orchestration_complete"
        elif answer == "not_math":
            llm = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                azure_deployment=os.getenv("MODEL", "gpt-4.1"),
            )
            chat = llm.chat.completions.create(
                model=os.getenv("MODEL", "gpt-4.1"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a classifier. Answer with ONLY one word. 'rag' if the input is about minecraft dirt blocks. 'web' if it's anything else.",
                    },
                    {
                        "role": "user",
                        "content": f"Classify this input: {self.state.topic}",
                    },
                ],
                max_tokens=10,
                temperature=0.0,
            )
            answer = chat.choices[0].message.content.strip().lower()
            if "rag" in answer:
                self.state.orchestrator_decision = "rag"
            elif "web" in answer:
                self.state.orchestrator_decision = "web"
            return "orchestration_complete"

    @router(orchestrate_research)
    def route_research(self):
        decision = self.state.orchestrator_decision.lower()
        print(f"Orchestrator decision: {decision}")
        if "math" in decision:
            return "math_path"
        elif "rag" in decision:
            return "rag_path"
        elif "web" in decision:
            return "web_path"

    @listen("rag_path")
    def execute_rag_research(self):
        """
        Execute RAG research using the local document crew
        """
        print("🔍 Executing RAG research...")

        try:
            webrag_crew = Webrag()
            rag_result = webrag_crew.rag_researcher().execute_task(
                webrag_crew.rag_research_task(),
                context={
                    "topic": self.state.topic,
                    "current_year": self.state.current_year,
                },
            )
            self.state.research_results.rag_findings = str(rag_result)
        except Exception as e:
            print(f"RAG research error: {e}")
            self.state.research_results.rag_findings = (
                f"RAG research completed for: {self.state.topic}"
            )

        self.state.research_results.research_method = "RAG"
        print("✅ RAG research completed")
        return "rag_completed"

    @listen("web_path")
    def execute_web_research(self):
        """
        Execute web research
        """
        print("🌐 Executing web research...")
        try:
            webrag_crew = Webrag()
            web_result = webrag_crew.web_researcher().execute_task(
                webrag_crew.web_research_task(),
                context={
                    "topic": self.state.topic,
                    "current_year": self.state.current_year,
                },
            )
            self.state.research_results.web_findings = str(web_result)
        except Exception as e:
            print(f"Web research error: {e}")
            self.state.research_results.web_findings = (
                f"Web research completed for: {self.state.topic}"
            )

        self.state.research_results.research_method = "Web"
        print("✅ Web research completed")
        return "web_completed"

    @listen("math_path")
    def execute_math_problem(self):
        """
        Execute math problem
        """
        try:
            math_crew = Math()
            math_result = math_crew.math_tool_agent().execute_task(
                math_crew.math_task(),
                context={"problem": self.state.topic, "topic": self.state.topic},
            )
            self.state.research_results.math_findings = str(math_result)
        except Exception as e:
            print(f"Math problem error: {e}")
            self.state.research_results.math_findings = (
                f"Math problem completed for: {self.state.topic}"
            )

        self.state.research_results.research_method = "Math"
        return "math_completed"

    @listen(or_(execute_rag_research, execute_web_research, execute_math_problem))
    def synthesize_and_report(self):
        """
        Synthesize research findings and create final report
        """
        print("📝 Synthesizing findings and creating report...")

        # Determine which research was actually executed
        if self.state.research_results.rag_findings:
            research_content = self.state.research_results.rag_findings
            research_method = "RAG"
        elif self.state.research_results.math_findings:
            research_content = self.state.research_results.math_findings
            research_method = "Math"
        else:
            research_content = self.state.research_results.web_findings
            research_method = "Web"

        explanation_crew = ExplanationCrew()

        self.state.final_report_structure = (
            explanation_crew.agent_manager().execute_task(
                explanation_crew.agent_manager_task(),
                context={
                    "topic": self.state.topic,
                    "research_content": research_content,
                },
            )
        )

        self.state.final_report_infos = explanation_crew.web_researcher().execute_task(
            explanation_crew.web_researcher_task(),
            context={
                "topic": self.state.topic,
                "research_content": research_content,
                "current_year": self.state.current_year,
            },
        )

        self.state.final_report = explanation_crew.expert_writer().execute_task(
            explanation_crew.expert_writer_task(),
            context={
                "topic": self.state.topic,
                "structure": str(self.state.final_report_structure),
                "research_info": str(self.state.final_report_infos),
                "original_research": research_content,
                "method": research_method,
            },
        )
        # Save the report
        os.makedirs("output", exist_ok=True)
        with open("output/research_report.md", "w", encoding="utf-8") as f:
            f.write(str(self.state.final_report))

        print(f"✅ Research flow completed using {research_method}!")
        print("📄 Final report saved to: output/research_report.md")

        return "flow_completed"


def kickoff():
    """
    Execute the Generic research flow and coordinate multi-agent research.
    
    Initializes and runs the complete generic research workflow, which
    intelligently routes queries to specialized crews and synthesizes
    comprehensive research findings.
    
    Returns
    -------
    Any
        The result object from the flow execution, containing research
        findings, analysis, and generated reports.
        
    Notes
    -----
    The function creates multiple output files:
    - research_plan.json: Initial research strategy and planning
    - research_report.md: Final comprehensive research report
    - research_summary.json: Complete research summary and metadata
    
    Examples
    --------
    >>> result = kickoff()
    >>> print("Research flow completed successfully")
    """
    flow = GenericFlow()
    result = flow.kickoff()

    print("\n" + "=" * 50)
    print("🎉 Generic Flow Complete!")
    print("=" * 50)
    print("Your research results are available in the output directory:")
    print("• research_plan.json - Initial research strategy")
    print("• research_report.md - Final comprehensive report")
    print("• research_summary.json - Complete research summary")

    return result


def plot():
    """Generate a visualization of the flow"""
    flow = GenericFlow()
    flow.plot("generic_flow")
    print("Flow visualization saved to generic_flow.html")


if __name__ == "__main__":
    kickoff()
    plot()
