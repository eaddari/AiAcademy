from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM

from src.evaluation.tools.rag_tool import QdrantRAGTool

import os
from dotenv import load_dotenv
load_dotenv(".env")

@CrewBase
class RagCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.qdrant_rag_tool = QdrantRAGTool()
        # Configure LLM for Azure OpenAI
        self.llm = LLM(
            model=os.getenv("MODEL"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-12-01-preview"
        )
        
        # Create agents
        self._medical_researcher = Agent(
            role="Medical Information Researcher",
            goal="Search and retrieve relevant medical information from the knowledge base to answer specific medical queries and provide accurate, evidence-based responses",
            backstory="You're a skilled medical researcher with expertise in accessing and analyzing medical literature and documentation. You specialize in finding relevant medical information quickly and accurately, using advanced search techniques to retrieve the most pertinent information for any medical query.",
            tools=[self.qdrant_rag_tool],
            llm=self.llm,
            verbose=True
        )
        
        self._medical_analyst = Agent(
            role="Medical Information Analyst",
            goal="Analyze and synthesize medical information retrieved by the researcher to provide comprehensive, well-structured answers with proper medical context",
            backstory="You're an experienced medical analyst with deep knowledge of medical terminology, procedures, and healthcare practices. You excel at interpreting medical information, identifying key insights, and presenting complex medical concepts in a clear, understandable manner while maintaining clinical accuracy.",
            tools=[self.qdrant_rag_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def medical_researcher(self) -> Agent:
        return self._medical_researcher

    @agent 
    def medical_analyst(self) -> Agent:
        return self._medical_analyst

    @task
    def research_medical_query(self) -> Task:
        return Task(
            description="Research the medical query: \"{medical_query}\" using the available knowledge base. Use the qdrant_rag_search tool to find relevant medical information that can help answer the query. Focus on finding accurate, evidence-based information from reliable medical sources.",
            expected_output="A comprehensive collection of relevant medical information related to the query, including source citations and key medical facts that will help answer the question.",
            agent=self._medical_researcher
        )

    @task
    def analyze_medical_information(self) -> Task:
        return Task(
            description="Analyze the medical information retrieved for the query: \"{medical_query}\". Synthesize the information to provide a comprehensive, well-structured answer. Ensure the response is medically accurate, properly contextualized, and includes appropriate citations to the source materials.",
            expected_output="A well-structured, comprehensive answer to the medical query that includes: Clear explanation of the medical topic, key facts and important details, proper source citations, and medical context and implications where relevant.",
            agent=self._medical_analyst
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
