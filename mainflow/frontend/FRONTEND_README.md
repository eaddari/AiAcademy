# EY Junior Accelerator - Streamlit Frontend

A simple web interface for the AI Study Plan Generator.

## Quick Start

1. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** and navigate to the displayed URL (typically `http://localhost:8501`)

3. **Use the app:**
   - Enter your background, experience, and learning goals
   - Click "Generate My Study Plan"
   - Wait for the AI agents to work
   - Download your personalized study plan

## Files

- `streamlit_app.py` - Main Streamlit application
- `src/components/study_plan_generator.py` - CrewAI integration
- `.streamlit/config.toml` - UI configuration

## Dependencies

All dependencies are managed in `pyproject.toml`. The main ones for the frontend are:
- streamlit
- plotly  
- pandas
- numpy

## Features

- 🎓 Clean, focused interface
- 🤖 Real-time AI agent progress tracking
- 📊 Organized results display with tabs
- 📥 Multiple download options
- 🎨 EY-branded styling
