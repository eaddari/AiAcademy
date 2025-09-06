from typing import Type
import os
import json
import requests
import mlflow
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv  
load_dotenv("mainflow\\.env") 


class SerperSearchTool(BaseTool):
    name: str = "serper_search"
    description: str = "Search the web for information using Google Search via Serper API"
    api_key: str = Field(default=None, description="Serper API key. If not provided, will use SERPER_API_KEY env variable.")

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("Serper API key required. Get it from https://serper.dev/")
        
    @mlflow.trace(span_type="RETRIEVER")
    def _run(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 10})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            print(f"Serper response: {response}")
        except Exception as e:
            return f"Search failed: {str(e)}"
        
        return response.json()