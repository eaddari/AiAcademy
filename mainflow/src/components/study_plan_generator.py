"""
Study Plan Generator component that integrates with the CrewAI flow
"""

import os
import sys
from pathlib import Path
import streamlit as st
from typing import Optional, Dict, Any, Callable

# Add the mainflow module to the path - go up to project root then to src/mainflow
project_root = Path(__file__).parent.parent.parent
mainflow_path = project_root / "src"
sys.path.insert(0, str(mainflow_path))

class StudyPlanGenerator:
    """Handles the study plan generation process using CrewAI"""
    
    def __init__(self):
        self.result_data = {}
        
    def generate_study_plan(
        self, 
        user_input: str,
        progress_callback: Optional[Callable] = None,
        output_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Generate a study plan based on user input
        
        Args:
            user_input: User's description of their background and goals
            progress_callback: Callback for progress updates
            output_callback: Callback for step outputs
            
        Returns:
            Dictionary containing the generated study plan and resources
        """
        
        try:
            # Create a custom Flow that we can control
            flow = CustomStreamlitFlow(
                user_input=user_input,
                progress_callback=progress_callback,
                output_callback=output_callback
            )
            
            # Execute the flow
            result = flow.run()
            
            return result
            
        except Exception as e:
            st.error(f"Error in study plan generation: {str(e)}")
            raise e


class CustomStreamlitFlow:
    """Custom flow handler that works with Streamlit without modifying Flow.state directly"""
    
    def __init__(self, user_input: str, progress_callback: Optional[Callable] = None, output_callback: Optional[Callable] = None):
        self.user_input = user_input
        self.progress_callback = progress_callback
        self.output_callback = output_callback
        self.results = {}
        
    def run(self) -> Dict[str, Any]:
        """Execute the study plan generation flow"""
        
        try:
            # Step 1: Input Validation
            if self.progress_callback:
                self.progress_callback("Input Validation", 0.1)
            
            user_info = self._run_input_validation()
            self.results["user_info"] = user_info
            
            if self.output_callback:
                self.output_callback("Input Validation", user_info)
            
            # Step 2: Plan Generation  
            if self.progress_callback:
                self.progress_callback("Plan Generation", 0.3)
                
            plan = self._run_plan_generation(user_info)
            self.results["plan"] = plan
            
            if self.output_callback:
                self.output_callback("Plan Generation", plan)
            
            # Step 3: Web Research
            if self.progress_callback:
                self.progress_callback("Web Research", 0.5)
                
            resources = self._run_web_search(plan)
            self.results["resources"] = resources
            
            if self.output_callback:
                self.output_callback("Web Research", resources)
            
            # Step 4: Paper Research
            if self.progress_callback:
                self.progress_callback("Paper Research", 0.7)
                
            papers = self._run_paper_research(plan)
            self.results["papers"] = papers
            
            if self.output_callback:
                self.output_callback("Paper Research", papers)
            
            # Step 5: Final Study Plan Creation
            if self.progress_callback:
                self.progress_callback("Creating Final Study Plan", 0.9)
                
            study_plan = self._run_study_plan_creation(resources, papers, plan)
            self.results["study_plan"] = study_plan
            
            if self.progress_callback:
                self.progress_callback("Complete", 1.0)
            
            return self.results
            
        except Exception as e:
            st.error(f"Error in custom flow execution: {str(e)}")
            raise e
    
    def _run_input_validation(self) -> str:
        """Run the input validation crew"""
        try:
            from mainflow.crews.input_crew.input_validation_crew import InputValidationCrew
            
            validation_crew = InputValidationCrew()
            crew_output = validation_crew.crew().kickoff(
                inputs={"question": self.user_input}
            )
            
            return crew_output.raw
            
        except Exception as e:
            st.warning(f"Input validation step failed: {str(e)}")
            # Fallback - use original input
            return self.user_input
    
    def _run_plan_generation(self, user_info: str) -> str:
        """Run the planning crew"""
        try:
            from mainflow.crews.planner_crew.crew import PlanningCrew
            
            planning_crew = PlanningCrew()
            crew_output = planning_crew.crew().kickoff(
                inputs={"user_info": user_info}
            )
            
            return crew_output.raw
            
        except Exception as e:
            st.error(f"Plan generation failed: {str(e)}")
            raise e
    
    def _run_web_search(self, plan: str) -> str:
        """Run the web search crew"""
        try:
            from mainflow.crews.web_crew.crew_new import WebCrew
            
            web_crew = WebCrew()
            crew_output = web_crew.crew().kickoff(
                inputs={"plan": plan}
            )
            
            return crew_output.raw
            
        except Exception as e:
            st.warning(f"Web search step failed: {str(e)}")
            # Provide fallback
            return "Web resources could not be retrieved at this time."
    
    def _run_paper_research(self, plan: str) -> str:
        """Run the paper research crew"""
        try:
            from mainflow.crews.paper_crew.paper_crew import PaperCrew
            
            paper_crew = PaperCrew()
            crew_output = paper_crew.crew().kickoff(
                inputs={"plan": plan}
            )
            
            return crew_output.raw
            
        except Exception as e:
            st.warning(f"Paper research step failed: {str(e)}")
            # Provide fallback
            return "Academic papers could not be retrieved at this time."
    
    def _run_study_plan_creation(self, resources: str, papers: str, plan: str) -> str:
        """Run the final study plan creation crew"""
        try:
            from mainflow.crews.study_plan_crew.crew import FinalStudyPlanCrew
            
            study_plan_crew = FinalStudyPlanCrew()
            crew_output = study_plan_crew.crew().kickoff(
                inputs={
                    "resources": resources,
                    "papers": papers,
                    "plan": plan
                }
            )
            
            return crew_output.raw
            
        except Exception as e:
            st.error(f"Study plan creation failed: {str(e)}")
            raise e
