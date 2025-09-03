#!/usr/bin/env python

from pydantic import BaseModel
from crewai.flow import Flow, listen, start

from src.evaluation.crews.rag_crew.crew import RagCrew


class Query(BaseModel):
    medical_query: str = ""
    analysis_result: str = ""


class MedicalRAGFlow(Flow[Query]):

    @start()
    def set_medical_query(self):
        self.state.medical_query = "What are the symptoms and treatment options for hypertension?"

    @listen(set_medical_query)
    def process_medical_query(self):
        result = RagCrew().crew().kickoff(inputs={"medical_query": self.state.medical_query})
        self.state.analysis_result = result.raw

    @listen(process_medical_query)
    def save_results(self):
        with open("medical_analysis.txt", "w", encoding="utf-8") as f:
            f.write(f"Query: {self.state.medical_query}\n\n")
            f.write("Analysis Result:\n")
            f.write(self.state.analysis_result)


def kickoff():
    MedicalRAGFlow().kickoff()


def kickoff_with_custom_query(query: str):
    flow = MedicalRAGFlow()
    flow.state.medical_query = query
    flow.process_medical_query()
    flow.save_results()


if __name__ == "__main__":

        kickoff()
