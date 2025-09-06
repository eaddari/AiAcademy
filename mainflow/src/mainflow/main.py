from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_

from mainflow.utils.input_validation import is_valid_input

from mainflow.crews.input_crew.input_validation_crew import InputValidationCrew
from mainflow.crews.planner_crew.crew import PlanningCrew
from mainflow.crews.web_crew.crew_new import WebCrew
from mainflow.crews.paper_crew.paper_crew import PaperCrew
from mainflow.crews.study_plan_crew.crew import FinalStudyPlanCrew

class State(BaseModel):
    question : str = ""
    user_info : str = ""
    plan : str = ""
    resources : str = ""
    papers : str = ""
    study_plan : str = ""

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
        crew_output = validation_crew.crew().kickoff(
            inputs={"question": self.state.question}
        )

        print(crew_output.raw)
        
        self.state.user_info = crew_output.raw

        # Output ipotetico
        # {"role": "AI Engineer", "past_experience": "bachelor's degree in economy and finance", "learning_goals": "become proficient in AI and machine learning"}

    @listen(sanitize_input)
    def generate_plan(self):
        print("Generating plan")
        planning_crew = PlanningCrew()
        crew_output = planning_crew.crew().kickoff(

            inputs={"user_info": self.state.user_info}
        )

        print("Output:", crew_output.raw)
        self.state.plan = crew_output.raw

    @listen(generate_plan)
    def web_search(self):
        print("Searching the web for resources")
        web_crew = WebCrew()
        crew_output = web_crew.crew().kickoff(

            inputs={"plan": self.state.plan}
        )

        print("Web crew output:", crew_output.raw)
        self.state.resources = crew_output.raw

    @listen(web_search)
    def paper_research(self):
        print("Searching for academic papers")
        paper_crew = PaperCrew()
        crew_output = paper_crew.crew().kickoff(

            inputs={"plan": self.state.plan}
        )

        print("Papers crew output:", crew_output.raw)
        self.state.papers = crew_output.raw

    @listen(and_(web_search, paper_research))
    def create_study_plan(self):
        print("Creating study plan")
        study_plan_crew = FinalStudyPlanCrew()
        crew_output = study_plan_crew.crew().kickoff(

            inputs={
                "resources": self.state.resources,
                "papers": self.state.papers,
                "plan": self.state.plan
            }
        )

        print(crew_output.raw)
        self.state.study_plan = crew_output.raw


def kickoff():
    flow = Flow()
    flow.kickoff()


def plot():
    flow = Flow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
