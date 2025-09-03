#!/usr/bin/env python
"""
Documentation Generation Flow for CrewAI Multi-Agent System.

This module implements a comprehensive documentation generation workflow that
uses Retrieval-Augmented Generation (RAG) and specialized AI crews to create
structured technical documentation. The flow coordinates multiple agents to
research, analyze, and synthesize information into professional documentation.

The workflow includes:
- Automated RAG research to gather system information
- Template-based section identification and content generation
- Multi-agent collaboration for comprehensive documentation
- Quality assurance and final report compilation

Classes
-------
DocumentationFlowState : BaseModel
    Pydantic model for managing flow state and data persistence.
DocumentationFlow : Flow
    Main flow class that orchestrates the documentation generation process.

Functions
---------
kickoff : callable
    Entry point function to start the documentation generation flow.
plot : callable
    Function to generate visual representation of the flow structure.

Examples
--------
Run the documentation flow:
    >>> from flow_documentation import kickoff
    >>> result = kickoff()

Generate flow visualization:
    >>> from flow_documentation import plot
    >>> plot()

Notes
-----
The flow uses Azure OpenAI models and requires proper configuration of
environment variables for API access. The RAG system depends on a
pre-indexed knowledge base with relevant system documentation.
"""
import os
from datetime import datetime
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from src.esercizio_esteso.crews.webrag.crew import Webrag
from src.esercizio_esteso.crews.docgen.crew import Docgen


class DocumentationFlowState(BaseModel):
    """
    State management for the Documentation flow.
    
    This Pydantic model manages the persistent state throughout the
    documentation generation workflow, tracking research findings,
    template sections, and intermediate results.
    
    Attributes
    ----------
    topic : str, default=""
        The main topic or focus area for documentation generation.
    rag_findings : str, default=""
        Raw findings and information extracted from the RAG research phase.
    template_sections : list, default=[]
        List of documentation template sections to be populated.
    section_responses : dict, default={}
        Dictionary mapping section identifiers to generated content.
    final_report : str, default=""
        The complete generated documentation as a formatted string.
        
    Examples
    --------
    >>> state = DocumentationFlowState()
    >>> state.topic = "API Documentation"
    >>> state.rag_findings = "Comprehensive API details..."
    
    Notes
    -----
    This model ensures type safety and data validation throughout the
    flow execution process, providing a structured way to manage the
    evolving documentation content.
    """
    
    topic: str = ""
    rag_findings: str = ""
    template_sections: list = []
    section_responses: dict = {}
    final_report: str = ""


class DocumentationFlow(Flow[DocumentationFlowState]):
    """
    Main flow class for orchestrating documentation generation.
    
    This class implements a CrewAI Flow that coordinates multiple AI agents
    and crews to generate comprehensive technical documentation. The flow
    follows a structured pipeline from research through synthesis to final
    report generation.
    
    The workflow includes the following stages:
    1. User input collection and topic definition
    2. RAG-based research to gather relevant information
    3. Template section identification and structure planning
    4. Content generation for each documentation section
    5. Final report compilation and formatting
    
    Attributes
    ----------
    state : DocumentationFlowState
        The persistent state object that tracks progress and data
        throughout the documentation generation process.
        
    Methods
    -------
    collect_user_input()
        Entry point for the flow that sets up automatic documentation generation.
    execute_rag_research()
        Performs comprehensive RAG research to gather system information.
    identify_template_sections()
        Parses templates to identify sections requiring content generation.
    generate_section_content()
        Creates content for each identified documentation section.
    compile_final_report()
        Assembles all sections into a cohesive final document.
        
    Examples
    --------
    >>> flow = DocumentationFlow()
    >>> result = flow.kickoff()
    
    Notes
    -----
    The flow uses the @start and @listen decorators to define the execution
    sequence and dependencies between different stages. Each method returns
    a string identifier that triggers the next stage in the pipeline.
    """
    
    @start()
    def collect_user_input(self):
        """
        Entry point: Set up automatic documentation generation from RAG.
        
        Initializes the documentation generation process by setting a
        comprehensive topic that will guide the RAG research phase.
        This method establishes the scope and focus for the entire
        documentation workflow.
        
        Returns
        -------
        str
            Status identifier "user_input_collected" to trigger the next
            stage in the flow pipeline.
            
        Notes
        -----
        The topic is set to capture comprehensive system information
        including architecture, implementation details, and usage
        instructions. This broad scope ensures thorough documentation
        coverage.
        """
        print("\n=== RAG Documentation Flow ===\n")
        
        # Set a general topic to extract comprehensive information from RAG
        self.state.topic = "comprehensive system documentation and technical implementation details"
        
        print(f"Starting automated documentation generation using RAG knowledge base\n")
        
        return "user_input_collected"

    @listen(collect_user_input)
    def execute_rag_research(self):
        """
        Execute comprehensive RAG research to gather all available information.
        
        Performs Retrieval-Augmented Generation research using the webrag crew
        to extract comprehensive information from the local knowledge base.
        The research covers system architecture, technical implementation,
        available components, and usage instructions.
        
        Returns
        -------
        str
            Status identifier "rag_completed" to trigger the next stage
            in the flow pipeline.
            
        Raises
        ------
        Exception
            If RAG research fails, the error is logged and a default
            message is used to continue the flow execution.
            
        Notes
        -----
        The method uses a comprehensive query designed to extract all
        relevant system information from the RAG knowledge base. Error
        handling ensures the flow continues even if RAG research fails.
        """
        print("🔍 Executing comprehensive RAG research to gather all system information...")
        
        # Ensure FAISS index exists
        try:
            from src.esercizio_esteso.crews.webrag.crew import SETTINGS, get_embeddings, corpus, load_or_build_vectorstore
            from pathlib import Path
            if not (Path(SETTINGS.persist_dir) / "index.faiss").exists():
                print("📚 Building FAISS index...")
                load_or_build_vectorstore(SETTINGS, get_embeddings(SETTINGS), corpus())
        except Exception as e:
            print(f"⚠️ FAISS setup failed: {e}")
        
        try:
            webrag_crew = Webrag()
            # Use a broad query to extract comprehensive information from the RAG system
            comprehensive_query = """
            Please provide comprehensive information about this system including:
            - System architecture and components
            - Technical implementation details
            - Available crews, agents, and tools
            - Configuration and setup
            - Features and capabilities
            - Usage instructions
            - Any other relevant technical information
            """
            
            rag_result = webrag_crew.rag_researcher().execute_task(
                webrag_crew.rag_research_task(),
                context={
                    "topic": comprehensive_query,
                    "current_year": str(datetime.now().year),
                }, # type: ignore
            )
            self.state.rag_findings = str(rag_result)
        except Exception as e:
            print(f"RAG research error: {e}")
            self.state.rag_findings = "Comprehensive system information gathered from RAG knowledge base"
        
        print("✅ RAG research completed")
        return "rag_completed"

    @listen(execute_rag_research)
    def identify_template_sections(self):
        """
        Parse the template to identify all sections that need information.
        
        Analyzes the documentation template structure to identify all
        sections that require content generation. Creates a structured
        list of sections with descriptions and specific questions to
        guide the content generation process.
        
        Returns
        -------
        str
            Status identifier "template_parsed" to trigger the next stage
            in the flow pipeline.
            
        Notes
        -----
        The template sections include standard documentation components
        such as application information, key links, architecture details,
        security considerations, and operational procedures. Each section
        includes specific questions to guide content generation.
        """
        print("📋 Identifying template sections...")
        
        # Define the main sections from the template
        self.state.template_sections = [
            {
                "title": "Application Owner & Basic Info",
                "description": "Application owner name, contact information, document version, reviewers",
                "questions": [
                    "Application Owner (name and contact):",
                    "Document Version:",
                    "Reviewers:"
                ]
            },
            {
                "title": "Key Links", 
                "description": "Repository, deployment pipeline, API, cloud account, project management links",
                "questions": [
                    "Code Repository URL:",
                    "Deployment Pipeline URL:",
                    "API Documentation URL:",
                    "Cloud Account details:",
                    "Project Management Board URL:"
                ]
            },
            {
                "title": "General Information & Purpose",
                "description": "AI system's intended purpose, target users, goals, ethical implications",
                "questions": [
                    "What is the AI system's intended purpose and sector of deployment?",
                    "What problem does this AI application solve?",
                    "Who are the target users and stakeholders?",
                    "What are the measurable goals and KPIs?",
                    "What are the prohibited uses or potential misuse scenarios?"
                ]
            },
            {
                "title": "Risk Classification",
                "description": "EU AI Act risk level classification and reasoning",
                "questions": [
                    "Risk Level (High/Limited/Minimal):",
                    "Reasoning for this risk classification:"
                ]
            },
            {
                "title": "Application Functionality",
                "description": "Instructions for use, capabilities, limitations, input/output requirements",
                "questions": [
                    "Instructions for deployers:",
                    "What can the application do (capabilities)?",
                    "What are the limitations?",
                    "Input data format and quality requirements:",
                    "How should outputs be interpreted?"
                ]
            },
            {
                "title": "Models and Datasets",
                "description": "Information about models and datasets used",
                "questions": [
                    "List the models used and their documentation links:",
                    "List the datasets used and their documentation:"
                ]
            },
            {
                "title": "Deployment Information",
                "description": "Deployment environment, infrastructure, and configuration",
                "questions": [
                    "Deployment environment details:",
                    "Infrastructure requirements:",
                    "Configuration settings:"
                ]
            },
            {
                "title": "Human Oversight",
                "description": "Human oversight mechanisms and procedures",
                "questions": [
                    "What human oversight mechanisms are in place?",
                    "How can humans intervene or override the system?",
                    "What are the escalation procedures?"
                ]
            }
        ]
        
        self.state.section_responses = {}
        
        print(f"✅ Found {len(self.state.template_sections)} sections to complete")
        return "sections_identified"

    @listen(identify_template_sections)
    def collect_all_sections(self):
        """
        Collect information for all sections with proper looping
        """
        print(f"📋 Starting collection for {len(self.state.template_sections)} sections...\n")
        
        for section_index, section in enumerate(self.state.template_sections):
            section_title = section["title"]
            
            print(f"{'='*80}")
            print(f"📝 SECTION {section_index + 1}/{len(self.state.template_sections)}: {section_title}")
            print(f"{'='*80}")
            print(f"Description: {section['description']}")
            
            # Check if RAG has information for this section
            try:
                from openai import AzureOpenAI
                
                llm = AzureOpenAI(
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), # type: ignore
                    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                    azure_deployment=os.getenv("MODEL", "gpt-4.1"),
                )
                
                rag_check_prompt = f"""
                Based on the following RAG findings, extract any information relevant to the section "{section_title}":
                
                RAG FINDINGS:
                {self.state.rag_findings}
                
                Section description: {section['description']}
                
                Return only the relevant information found, or "No relevant information found" if nothing matches.
                """
                
                response = llm.chat.completions.create(
                    model=os.getenv("MODEL", "gpt-4.1"),
                    messages=[
                        {"role": "system", "content": "Extract relevant information for the specified section."},
                        {"role": "user", "content": rag_check_prompt}
                    ],
                    max_tokens=300,
                    temperature=0.1,
                )
                
                rag_info = response.choices[0].message.content.strip()
                
                if "No relevant information found" not in rag_info:
                    print(f"\n🔍 Found in RAG: {rag_info}")
                else:
                    print(f"\n🔍 No relevant information found in RAG for this section")
                    
            except Exception as e:
                print(f"⚠️ Could not check RAG for section info: {e}")
                rag_info = "RAG check failed"
            
            # Ask questions for this section
            section_responses = {}
            print(f"\nPlease provide information for the following:")
            
            for question in section["questions"]:
                print(f"\n❓ {question}")
                answer = input("   Answer (or press Enter to skip): ").strip()
                if answer:
                    section_responses[question] = answer
                else:
                    section_responses[question] = "[Not provided]"
            
            # Store the responses for this section
            self.state.section_responses[section_title] = {
                "rag_info": rag_info,
                "user_responses": section_responses
            }
            
            print(f"\n✅ Section '{section_title}' completed!")
            print(f"{'='*80}\n")
        
        print(f"🎉 All {len(self.state.template_sections)} sections completed!")
        return "all_sections_completed"

    @listen(collect_all_sections)
    def generate_documentation(self):
        """
        Generate documentation using RAG findings + section-by-section user input to fill out the EU AI Act template
        """
        print("📝 Generating documentation by filling out EU AI Act template...")
        
        # Load template structure from template.md
        template_path = "template.md"
        template_structure = ""
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_structure = f.read()
            print(f"📋 Using EU AI Act compliance template from: {template_path}")
        else:
            print("⚠️ Template not found, using fallback structure")
            template_structure = """# System Documentation

## Overview
{research_content}

## Technical Details
[To be filled from RAG findings]
"""
        
        # Combine RAG findings with all section responses
        combined_content = f"""
        RAG FINDINGS:
        {self.state.rag_findings}

        SECTION-BY-SECTION USER RESPONSES:
        """
        
        for section_title, section_data in self.state.section_responses.items():
            combined_content += f"\n\n### {section_title}:\n"
            combined_content += f"RAG Info: {section_data['rag_info']}\n"
            combined_content += "User Responses:\n"
            for question, answer in section_data['user_responses'].items():
                combined_content += f"- {question} {answer}\n"
        
        # Use docgen crew to fill out the template with all collected information
        document_crew = Docgen()
        
        # Generate documentation by filling the template with combined information
        self.state.final_report = str(
            document_crew.generation_agent().execute_task(
                document_crew.document_generation_task(),
                context={
                    "topic": "Multi-Agent AI Research System",
                    "research_content": combined_content,
                    "research_method": "RAG + Section-by-Section User Input",
                    "current_year": str(datetime.now().year),
                    "template_structure": template_structure,
                    "instruction": """Fill out the provided template structure using both the RAG findings and detailed section-by-section user responses. 
                    For each section in the template:
                    1. First use any relevant RAG information found
                    2. Then incorporate the specific user responses for that section
                    3. Prioritize user-provided information when it conflicts with RAG findings
                    4. Maintain the exact template structure and formatting
                    5. Replace placeholders with concrete information
                    6. If information is still missing after combining both sources, clearly mark those sections as '[Information not available]'
                    7. Ensure EU AI Act compliance requirements are properly addressed""",
                }, # type: ignore
            )
        )
        
        # Save the generated documentation
        os.makedirs("output", exist_ok=True)
        with open("output/research_report.md", "w", encoding="utf-8") as f:
            f.write(self.state.final_report)
        
        print("✅ Documentation generation completed!")
        print("📄 EU AI Act compliant documentation saved to: output/research_report.md")
        print(f"📊 Completed {len(self.state.section_responses)} sections with user input")
        
        return "flow_completed"


def kickoff():
    """
    Execute the Documentation flow and generate comprehensive documentation.
    
    Initializes and runs the complete documentation generation workflow,
    coordinating multiple AI agents to create structured technical
    documentation based on RAG research and template-driven content
    generation.
    
    Returns
    -------
    Any
        The result object from the flow execution, containing the
        generated documentation and metadata about the process.
        
    Notes
    -----
    The function creates a new DocumentationFlow instance and executes
    the complete workflow pipeline. The final documentation is saved
    to 'output/research_report.md' and status information is printed
    to the console.
    
    Examples
    --------
    >>> result = kickoff()
    >>> print("Documentation generated successfully")
    """
    flow = DocumentationFlow()
    result = flow.kickoff()
    
    print("\n" + "=" * 50)
    print("🎉 Documentation Flow Complete!")
    print("=" * 50)
    print("📄 Final documentation saved to: output/research_report.md")
    
    return result


def plot():
    """
    Generate a visualization of the documentation flow structure.
    
    Creates a visual representation of the DocumentationFlow showing
    the relationships between different stages, agents, and tasks in
    the documentation generation workflow.
    
    Notes
    -----
    The visualization is saved as an HTML file named
    'documentation_flow.html' in the current directory. This helps
    in understanding the flow structure and debugging the workflow.
    
    Examples
    --------
    >>> plot()
    >>> print("Flow visualization created")
    """
    flow = DocumentationFlow()
    flow.plot("documentation_flow")
    print("Flow visualization saved to documentation_flow.html")


if __name__ == "__main__":
    kickoff()
