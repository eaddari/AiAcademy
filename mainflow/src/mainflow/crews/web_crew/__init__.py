# src/mainflow/crews/web_crew/__init__.py
from __future__ import annotations

import json, os
from pathlib import Path
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

class WebCrew:
    """
    Crew 3:
    - takes ONLY Crew 2's JSON payload
    - searches with Serper
    - writes results back into the correct sections of that payload
      under a 'web_resources' key
    """
    def __init__(self) -> None:
        base = Path(__file__).parent #carica file yaml nella stessa cartella

        with open(base / "agents.yaml", "r", encoding="utf-8") as f:
            agents_cfg = yaml.safe_load(f)
        with open(base / "tasks.yaml", "r", encoding="utf-8") as f:
            tasks_cfg = yaml.safe_load(f)

        # --- Azure OpenAI LLM 
        self.llm = LLM(
            model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT')}",
            api_key=os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION") or os.getenv("AZURE_API_VERSION"),
            temperature=0.2,
        )

        # Tool Serper
        self.serper = SerperDevTool()

        # Agente con LLM Azure
        self.agent = Agent(
            **agents_cfg["web_researcher"],
            tools=[self.serper],
            llm=self.llm,          
        )

        self.task_tpl = tasks_cfg["web_search_task"]

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
