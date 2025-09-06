# src/mainflow/crews/web_crew/crew.py
from __future__ import annotations

import json, os
from pathlib import Path
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List
from dotenv import load_dotenv

load_dotenv("C:\\desktopnoonedrive\\gruppo-finale\\AiAcademy\\mainflow\\.env")

@CrewBase
class WebCrew:
    """
    Web Research Crew

    Takes the study plan from Crew 2 (PlanningCrew) and enhances it with
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
        
        # Create model string
        self.model = f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}"
        
        # Initialize Serper tool
        self.serper = SerperDevTool()

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
            tools=[self.serper],
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

    def _parse_json(self, value) -> dict:
        """Accepts CrewOutput or string and returns a JSON dict."""
        # Se è un CrewOutput, prendi il testo, messo perché dava errore crew.kickoff() ritorna CrewOutput non stringa
        text = getattr(value, "raw", None)
        if text is None:
            text = str(value)

        # Prova parsing diretto
        # Gli LLM a volte mettono disclaimer/testo. Questo metodo rende robusto il parsing senza dipendere da feature opzionali.
        try:
            return json.loads(text)
        except Exception:
            # fallback: prendi la prima {...} grande
            start, end = text.find("{"), text.rfind("}")
            if start != -1 and end != -1:
                return json.loads(text[start:end + 1])
            raise


    def _merge_into_payload(self, crew2_payload: dict | list, results: dict) -> dict | list:
        '''Merges the web search results into the original Crew 2 payload.'''
        payload = json.loads(json.dumps(crew2_payload)) # copia sicura
        res_sections = (results or {}).get("sections", {})
        if not res_sections: # niente da unire, non c'è la sezione di web resources
            return payload

        # Se il payload di Crew 2 non ha un campo sections, appende tutto in un unico web_resources top-level così almeno non perdiamo il lavoro.
        sections = payload.get("sections", None)
        if sections is None:
            payload["web_resources"] = res_sections
            return payload

        if isinstance(sections, list): # se section è lista
            # Per ogni sezione trovata dal modello, inserisce l’array web_resources nella sezione corrispondente del payload di Crew 2
            index = {}
            for i, s in enumerate(sections):
                name = str(s.get("name", "")).strip().lower()
                if name:
                    index[name] = i
            for sec_name, items in res_sections.items():
                key = str(sec_name).strip().lower()
                if key in index:
                    payload["sections"][index[key]]["web_resources"] = items
            return payload

        if isinstance(sections, dict): # è dizionario
            for sec_name, items in res_sections.items():
                if sec_name in sections:
                    payload["sections"][sec_name]["web_resources"] = items
                else:
                    for k in list(sections.keys()):
                        if str(k).lower().strip() == str(sec_name).lower().strip():
                            payload["sections"][k]["web_resources"] = items
                            break
            return payload

        # se sections non è né lista né dizionario, appende tutto in un unico web_resources top-level così almeno non perdiamo il lavoro.
        payload["web_resources"] = res_sections
        return payload

    def kickoff(self, crew2_payload: dict | list) -> dict | list:
        """Starts the Crew 3 process."""
        # Prepara il task con il payload di Crew 2
        description = self.task_tpl["description"].format(
            crew2_payload=json.dumps(crew2_payload, ensure_ascii=False, indent=2)
        )
        task = Task(
            description=description,
            expected_output=self.task_tpl["expected_output"],
            agent=self.agent,
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
        crew_output = crew.kickoff()  # CrewOutput
        results = self._parse_json(crew_output)  # la nuova _parse_json gestisce CrewOutput
        updated = self._merge_into_payload(crew2_payload, results)
        return updated
