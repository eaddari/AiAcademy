# da mainflow python -m tests.monitoring
# mlflow ui --backend-store-uri "file:///$((Resolve-Path .\mlruns).Path.Replace('\','/'))"
# --- make project root AND src/ importable ---
import sys, os
# HERE = os.path.dirname(__file__)                         # .../mainflow/tests
# PROJECT_ROOT = os.path.abspath(os.path.join(HERE, "..")) # .../mainflow
# SRC_DIR = os.path.join(PROJECT_ROOT, "src")              # .../mainflow/src

# for p in (PROJECT_ROOT, SRC_DIR):
#     if p not in sys.path:
#         sys.path.insert(0, p)
# # ------------------------------------------------------
from pydantic import BaseModel
import mlflow
from crewai.flow import Flow, listen, start, and_
import time
from src.mainflow.utils.input_validation import is_valid_input
from mlflow.genai.scorers import RetrievalRelevance, RelevanceToQuery
import pandas as pd
from src.mainflow.crews.input_crew.input_validation_crew import InputValidationCrew
from src.mainflow.crews.planner_crew.crew import PlanningCrew
from src.mainflow.crews.web_crew.crew_new import WebCrew
from src.mainflow.crews.paper_crew.paper_crew import PaperCrew
from src.mainflow.crews.study_plan_crew.crew import FinalStudyPlanCrew

# usa sempre lo store del root del progetto
# TRACKING_DIR = os.path.join(PROJECT_ROOT, "mlruns")
# mlflow.set_tracking_uri("file:///" + TRACKING_DIR.replace("\\", "/"))

mlflow.crewai.autolog()
mlflow.set_experiment("EY Junior Accelerator") #imposta l'esperimento

print("Tracking URI ->", mlflow.get_tracking_uri())
# per accedere a ui mlflow runnare in secondo terminale
# server --host localhost --port 5001 --backend-store-uri file:///C:/desktopnoonedrive/gruppo-finale/AiAcademy/mainflow/mlruns


class State(BaseModel):
    question : str = ""
    user_info : str = ""
    plan : str = ""
    resources : str = ""
    papers : str = ""
    study_plan : str = ""

class MonitoringConfig():

    #salva l'ora di inizio per calcolare il tempo di esecuzione
    def __init__(self):
        self.start_time = time.time()

    def monitoring_crew(self,state: State, crew_output, crew: InputValidationCrew, crew_name, create: bool = False):
        """
        Enhanced monitoring that works alongside CrewAI autolog.
        Autolog will handle detailed agent/task tracing, while this provides workflow-level metrics.
        """
        with mlflow.start_run(run_name=f"{crew_name} Monitoring", nested=True):              
                mlflow.log_param("crew", crew_name)
                mlflow.log_param("input_question", state.question)
                mlflow.log_param("sanitized_input", crew_output.raw)
                mlflow.log_param("num_agents", len(crew.agents))
                execution_time = time.time() - self.start_time
                mlflow.log_metric("execution_time_seconds", execution_time)
                mlflow.log_param("output_type", type(crew_output).__name__)
                mlflow.log_metric("output_length", len(str(crew_output.raw)))
                mlflow.log_metric("tokens_total", float(crew_output.token_usage.total_tokens))
                mlflow.log_metric("tokens_prompt", float(len(state.question)))
                mlflow.log_metric("tokens_completion", float(crew_output.token_usage.completion_tokens))
                mlflow.log_param("token_usage_details", str(crew_output.token_usage))


class Flow(Flow[State]):

    @start()
    def insert_topic(self):
        print("="*20, " Welcome to the EY Junior Accelerator! ", "="*20)
        
        question = input("Describe your role, past experience, learning goals: ")
        
        if not is_valid_input(question):
            print("Invalid input detected. Please avoid using escape sequences or empty inputs.")
            return self.insert_topic()
        self.state.question = question

    @listen(insert_topic)
    def sanitize_input(self):
        print("Sanitizing input")
        validation_crew = InputValidationCrew()
        monitor = MonitoringConfig()
        crew_output = validation_crew.crew().kickoff(
            inputs={"question": self.state.question}
        )
        monitor.monitoring_crew(self.state, crew_output, validation_crew, "InputValidationCrew")
        
        self.state.user_info = crew_output.raw
        print(self.state.user_info)
        

    @listen(sanitize_input)
    def generate_plan(self):
        print("Generating plan")
        planning_crew = PlanningCrew()
        monitor = MonitoringConfig()
        crew_output = planning_crew.crew().kickoff(

            inputs={"user_info": self.state.user_info}
        )
        monitor.monitoring_crew(self.state, crew_output, planning_crew, "PlanningCrew")
        self.state.plan = crew_output.raw

        print("Output:", crew_output.raw)
        

    @listen(generate_plan)
    def web_search(self):
        print("Searching the web for resources")
        web_crew = WebCrew()
        monitor = MonitoringConfig()
        crew_output = web_crew.crew().kickoff(

            inputs={"plan": self.state.plan}
        )
        monitor.monitoring_crew(self.state, crew_output, web_crew, "WebCrew")
        self.state.resources = crew_output.raw

    @listen(web_search)
    def paper_research(self):
        print("Searching for academic papers")
        paper_crew = PaperCrew()
        monitor = MonitoringConfig()
        crew_output = paper_crew.crew().kickoff(

            inputs={"plan": self.state.plan}
        )
        monitor.monitoring_crew(self.state, crew_output, paper_crew, "PaperCrew")

        print("Papers crew output:", crew_output.raw)
        self.state.papers = crew_output.raw

    @listen(and_(web_search, paper_research))
    def create_study_plan(self):
        print("Creating study plan")
        study_plan_crew = FinalStudyPlanCrew()
        monitor = MonitoringConfig()
        crew_output = study_plan_crew.crew().kickoff(

            inputs={
                "resources": self.state.resources,
                "papers": self.state.papers,
                "plan": self.state.plan
            }
        )
        monitor.monitoring_crew(self.state, crew_output, study_plan_crew, "FinalStudyPlanCrew")
        
        evaluation_ethics_data = pd.DataFrame([{"inputs": {"question": self.state.question},
                                                "outputs": crew_output.raw}])
        mlflow.genai.evaluate(data=evaluation_ethics_data,scorers=[RelevanceToQuery(model = "azure:/gpt-4.1")])
        print(crew_output.raw)
        self.state.study_plan = crew_output.raw


def kickoff():
    """
    Main workflow execution with enhanced MLflow tracking.
    CrewAI autolog will automatically capture detailed traces for all crew operations.
    """
    with mlflow.start_run(run_name="EYFlow_with_Autolog") as run:
        mlflow.log_param("workflow_type", "EY_Junior_Accelerator")
        mlflow.log_param("autolog_enabled", True)
        mlflow.log_param("python_version", sys.version)
        try:
            start_time = time.time()
            flow = Flow()
            result = flow.kickoff()
            total_time = time.time() - start_time
            mlflow.log_metric("total_workflow_time", total_time)
            mlflow.log_param("workflow_status", "completed")
            print(f"🎉 Workflow completed successfully in {total_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            mlflow.log_param("workflow_status", "failed")
            mlflow.log_param("error_message", str(e))
            print(f"❌ Workflow failed: {e}")
            raise
    
def plot():
    flow = Flow()
    flow.plot()

if __name__ == "__main__":
    kickoff()
