"""
EY Junior Accelerator - AI Study Plan Generator
Main Streamlit application entry point
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.components.study_plan_generator import StudyPlanGenerator

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="EY Junior Accelerator - AI Study Plan Generator",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    .stTitle {
        text-align: center;
        color: #FFD500;
        margin-bottom: 2rem;
    }
    .step-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .step-title {
        font-weight: bold;
        color: #2E4057;
        margin-bottom: 5px;
        font-size: 16px;
    }
    .progress-container {
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and header
    st.title("🎓 EY Junior Accelerator")
    st.markdown("### AI-Powered Study Plan Generator")
    st.markdown("Create personalized learning paths using AI agents")
    st.markdown("---")
    
    # Main content - simplified single column
    st.subheader("📝 Tell us about yourself")
    st.markdown("Provide details about your background, experience, and learning goals to get a personalized study plan.")
    
    # User input form
    with st.form("user_input_form", clear_on_submit=False):
        user_input = st.text_area(
            "Describe your role, past experience, and learning goals:",
            placeholder="Example: I'm a finance professional with a bachelor's degree in economics. I want to become proficient in AI and machine learning to transition into an AI Engineer role.",
            height=150,
            help="Be specific about your background, current role, and what you want to learn",
            key="user_input_text"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🚀 Generate My Study Plan", use_container_width=True)
        
    # Process the request
    if submit_button and user_input.strip():
        # Initialize components
        generator = StudyPlanGenerator()
        
        # Create containers for real-time updates
        progress_container = st.container()
        output_container = st.container()
        
        # Start the study plan generation process
        with st.spinner("🤖 Initializing AI agents..."):
            try:
                # Show progress steps
                with progress_container:
                    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                    st.markdown("### 🔄 Generation Progress")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate study plan with real-time updates
                def update_progress(step, progress):
                    progress_bar.progress(progress)
                    status_text.text(f"🔄 {step}...")
                
                def update_output(step, output):
                    with output_container:
                        with st.expander(f"📋 {step} Output", expanded=False):
                            st.text_area("", value=output, height=100, disabled=True)
                
                result = generator.generate_study_plan(
                    user_input=user_input,
                    progress_callback=update_progress,
                    output_callback=update_output
                )
                
                # Clear progress
                progress_bar.progress(1.0)
                status_text.text("✅ Study plan generated successfully!")
                
                # Display final result
                if result and result.get("study_plan"):
                    st.success("🎉 Your personalized study plan is ready!")
                    
                    # Display the final study plan
                    with st.expander("📋 Your Complete Study Plan", expanded=True):
                        st.markdown(result["study_plan"])
                        
                    # Display additional sections in tabs
                    tab1, tab2, tab3 = st.tabs(["🔗 Web Resources", "📚 Academic Papers", "📊 Learning Plan"])
                    
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
                            
                    # Download options
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download Study Plan",
                            data=result.get("study_plan", ""),
                            file_name="my_study_plan.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.download_button(
                            label="📥 Download Resources",
                            data=result.get("resources", ""),
                            file_name="learning_resources.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col3:
                        st.download_button(
                            label="📥 Download Papers",
                            data=result.get("papers", ""),
                            file_name="academic_papers.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                else:
                    st.error("❌ Could not generate study plan. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                with st.expander("🔍 Error Details", expanded=False):
                    st.code(str(e))
                st.info("💡 Please try rephrasing your request or contact support if the issue persists.")
    
    elif submit_button and not user_input.strip():
        st.warning("⚠️ Please describe your background and learning goals before generating a study plan.")
    # Add helpful information at the bottom
    st.markdown("---")
    
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        The AI Study Plan Generator uses 5 specialized AI agents working together:
        
        1. **🔍 Input Validation** - Analyzes and structures your input
        2. **📋 Plan Generation** - Creates a personalized learning roadmap  
        3. **🌐 Web Research** - Finds online resources and courses
        4. **📚 Paper Research** - Discovers relevant academic materials
        5. **📝 Final Assembly** - Combines everything into a comprehensive study plan
        
        **Built with:** CrewAI, OpenAI, and Streamlit
        """)

if __name__ == "__main__":
    main()
