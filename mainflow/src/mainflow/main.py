#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from src.mainflow.crews.input_crew.input_validation_crew import InputValidationCrew

# a function that check if the input is not an escape sequence or a null input
def is_valid_input(user_input: str) -> bool:
    # Check for empty input
    if not user_input.strip():
        return False

    escape_sequences = ["\x1b", "\x00", "\n", "\r", "\t", "\x03"]
    for seq in escape_sequences:
        if seq in user_input:
            return False
        
    return True

class PoemState(BaseModel):
    question : str = ""
    poem: str = ""

class PoemFlow(Flow[PoemState]):

    @start()
    def insert_topic(self):
        print("="*20, " Welcome to the EY Junior Accelerator! ", "="*20)
        question = input("Inserting a topic:  ")
        if not is_valid_input(question):
            print("Invalid input detected. Please avoid using escape sequences or empty inputs.")
            return self.insert_topic()
        self.state.question = question

    @listen(insert_topic)
    def generate_poem(self):
        print("Generating poem")
        crew = InputValidationCrew()
        crew_output = crew.crew().kickoff(
            inputs={"question": self.state.question}
        )

        print("Output:", crew_output.raw)
        self.state.poem = crew_output.raw



def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
