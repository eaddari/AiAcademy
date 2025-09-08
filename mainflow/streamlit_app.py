import streamlit as st
import sys
import os
from pathlib import Path
import time
from frontend.utils.style_manager import apply_custom_styles

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mainflow.main import Flow, State
from mainflow.utils.input_validation import is_valid_input
from mainflow.crews.input_crew.input_validation_crew import InputValidationCrew
from mainflow.crews.planner_crew.crew import PlanningCrew
from mainflow.crews.web_crew.crew_new import WebCrew
from mainflow.crews.paper_crew.paper_crew import PaperCrew
from mainflow.crews.study_plan_crew.crew import FinalStudyPlanCrew
from mainflow.crews.calendar_crew.crew import CalendarCrew
from crewai.flow import Flow as CrewAIFlow, listen, start

class StreamlitFlow(CrewAIFlow[State]):
    """Custom Flow for Streamlit that accepts user input directly"""
    
    def __init__(self, user_input: str, progress_callback=None, status_callback=None):
        super().__init__()
        self.user_input = user_input
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        
    @start()
    def insert_topic(self):
        print("="*20, " Welcome to the EY Junior Accelerator! ", "="*20)
        
        if not is_valid_input(self.user_input):
            print("Invalid input detected. Please avoid using escape sequences or empty inputs.")
            raise ValueError("Invalid input provided")
            
        self.state.question = self.user_input

    @listen(insert_topic)
    def sanitize_input(self):
        if self.status_callback:
            self.status_callback("🔍 Sanitizing input...")
        if self.progress_callback:
            self.progress_callback(0.2)
            
        print("Sanitizing input")
        validation_crew = InputValidationCrew()
        crew_output = validation_crew.crew().kickoff(
            inputs={"question": self.state.question}
        )
        print(crew_output.raw)
        self.state.user_info = crew_output.raw

    @listen(sanitize_input)
    def generate_plan(self):
        if self.status_callback:
            self.status_callback("📋 Generating study plan outline...")
        if self.progress_callback:
            self.progress_callback(0.35)
            
        print("Generating plan")
        planning_crew = PlanningCrew()
        crew_output = planning_crew.crew().kickoff(
            inputs={"user_info": self.state.user_info}
        )
        print("Output:", crew_output.raw)
        self.state.plan = crew_output.raw

    @listen(generate_plan)
    def web_search(self):
        if self.status_callback:
            self.status_callback("🌐 Searching for web resources...")
        if self.progress_callback:
            self.progress_callback(0.5)
            
        print("Searching the web for resources")
        web_crew = WebCrew()
        crew_output = web_crew.crew().kickoff(
            inputs={"plan": self.state.plan}
        )
        print("Web crew output:", crew_output.raw)
        self.state.resources = crew_output.raw

    @listen(web_search)
    def paper_research(self):
        if self.status_callback:
            self.status_callback("📚 Researching academic papers...")
        if self.progress_callback:
            self.progress_callback(0.65)
            
        print("Searching for academic papers")
        paper_crew = PaperCrew()
        crew_output = paper_crew.crew().kickoff(
            inputs={"plan": self.state.plan}
        )
        print("Papers crew output:", crew_output.raw)
        self.state.papers = crew_output.raw

    @listen(paper_research)
    def define_calendar(self):
        if self.status_callback:
            self.status_callback("📅 Creating study calendar...")
        if self.progress_callback:
            self.progress_callback(0.8)
            
        print("Defining calendar")
        calendar_crew = CalendarCrew()
        crew_output = calendar_crew.crew().kickoff(
            inputs={
                "web_resources": self.state.resources,
                "papers": self.state.papers,
                "plan": self.state.plan
            }
        )
        print("Calendar defined based on the plan, resources, and papers.")
        self.state.calendar = crew_output.raw

    @listen(define_calendar)
    def create_study_plan(self):
        if self.status_callback:
            self.status_callback("✨ Finalizing your personalized study plan...")
        if self.progress_callback:
            self.progress_callback(0.95)
            
        print("Creating study plan")
        study_plan_crew = FinalStudyPlanCrew()
        crew_output = study_plan_crew.crew().kickoff(
            inputs={
                "resources": self.state.resources,
                "papers": self.state.papers,
                "plan": self.state.plan,
                "calendar": self.state.calendar
            }
        )
        print(crew_output.raw)
        self.state.study_plan = crew_output.raw

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="EY Junior Accelerator",
        page_icon=" ",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state for disclaimer
    if 'disclaimer_accepted' not in st.session_state:
        st.session_state.disclaimer_accepted = False
    
    # Show AI Disclaimer Modal
    if not st.session_state.disclaimer_accepted:
        @st.dialog("🤖 AI-Powered System Notice")
        def show_disclaimer():
            st.warning("⚠️ **Important Notice**")
            st.markdown("""
            **This system uses artificial intelligence to generate personalized study guides based on your input.**
            
            Please note that:
            - **No human is involved** in the generation of these responses
            - This system is powered by **AI (GPT-4.1)** 
            - **Responses are automatically generated**
            - Results should be reviewed and validated independently
            
            By continuing, you acknowledge and accept these terms.
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ I Understand & Continue", use_container_width=True, type="primary"):
                    st.session_state.disclaimer_accepted = True
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.stop()
        
        show_disclaimer()
        return  # Exit early if disclaimer not accepted
    
    # Apply custom styles from external CSS file
    apply_custom_styles()
    
    st.title("EY Junior Accelerator")
    st.markdown("---")
    st.markdown("## Your AI-Powered learning plan generator")
    
    # User input form
    with st.form("user_input_form", clear_on_submit=False):
        user_input = st.text_area(
            "Describe your role, past experience, and learning goals:",
            placeholder="Example: I'm a finance professional with a bachelor's degree in economics. I want to become proficient in AI and machine learning to transition into an AI Engineer role.",
            height=100,
            help="Be specific about your background, current role, and what you want to learn",
            key="user_input_text"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Generate My Study Plan", use_container_width=True)
        
    # Process the request
    if submit_button and user_input:
        # Create containers for real-time updates
        progress_container = st.container()
        output_container = st.container()
        
        # Start the study plan generation process
        with st.spinner("Initializing AI agents..."):
            try:
                # Show progress steps
                with progress_container:
                    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                    st.markdown("###  Generation Progress")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Define callback functions for progress updates
                def update_progress(progress_value):
                    progress_bar.progress(progress_value)
                
                def update_status(status_message):
                    status_text.text(status_message)
                
                # Initialize the main flow with user input and callbacks
                flow = StreamlitFlow(
                    user_input=user_input,
                    progress_callback=update_progress,
                    status_callback=update_status
                )
                
                # Start with initial status
                update_status("🚀 Starting AI agents...")
                update_progress(0.1)
                
                # Run the complete flow
                flow.kickoff()
                
                # Final progress update
                update_progress(1.0)
                update_status("✅ Study plan generated successfully!")
                
                # Extract results from flow state
                result = {
                    "study_plan": flow.state.study_plan,
                    "resources": flow.state.resources, 
                    "papers": flow.state.papers,
                    "plan": flow.state.plan,
                    "calendar": flow.state.calendar
                }
                
                
                # Display final result
                if result and result.get("study_plan"):
                    st.success(" Your personalized study plan is ready!")
                    
                    # Display the final study plan
                    st.markdown("### 📋 Your Complete Study Plan")
                    st.markdown(result["study_plan"])
                        
                    # Display additional sections in tabs
                    tab1, tab2, tab3, tab4 = st.tabs([" Web Resources", " Academic Papers", " Learning Plan", " Calendar"])

                    with tab1:
                        if result.get("resources"):
                            st.markdown(result["resources"])
                        else:
                            st.info("No web resources found.")
                            
                    with tab2:
                        if result.get("papers"):
                            st.markdown(result["papers"])
                        else:
                            st.info("No academic papers found.")
                            
                    with tab3:
                        if result.get("plan"):
                            st.markdown(result["plan"])
                        else:
                            st.info("No detailed plan available.")
                            
                    with tab4:
                        if result.get("calendar"):
                            st.markdown(result["calendar"])
                        else:
                            st.info("No calendar available.")
                            
                    # Download options
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.download_button(
                            label=" Download Study Plan",
                            data=result.get("study_plan", ""),
                            file_name="my_study_plan.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.download_button(
                            label=" Download Resources",
                            data=result.get("resources", ""),
                            file_name="learning_resources.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col3:
                        st.download_button(
                            label=" Download Papers",
                            data=result.get("papers", ""),
                            file_name="academic_papers.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col4:
                        st.download_button(
                            label=" Download Calendar",
                            data=result.get("calendar", ""),
                            file_name="study_calendar.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                else:
                    st.error(" Could not generate study plan. Please try again.")
                    
            except Exception as e:
                st.error(f" An error occurred: {str(e)}")
                with st.expander(" Error Details", expanded=False):
                    st.code(str(e))
                st.info(" Please try rephrasing your request or contact support if the issue persists.")
    
    elif submit_button and not user_input.strip():
        st.warning(" Please describe your background and learning goals before generating a study plan.")

# avvisare utente che sta usando AI



if __name__ == "__main__":
    main()
