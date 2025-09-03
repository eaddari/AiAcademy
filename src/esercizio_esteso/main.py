#!/usr/bin/env python
"""
Main entry point for the Esercizio Esteso CrewAI application.

This module serves as the primary entry point for the CrewAI-based multi-agent
system that handles documentation generation through specialized AI crews and flows.

Examples
--------
Run the application directly:
    $ python main.py

Or import and use programmatically:
    >>> from main import run_flow, plot_flow
    >>> result = run_flow()
    >>> plot_flow()

Notes
-----
The module suppresses SyntaxWarning from the pysbd module to prevent
unnecessary warnings during execution.
"""
import warnings
from .flow_documentation import kickoff as flow_kickoff, plot as flow_plot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_flow():
    """
    Execute the documentation generation flow.
    
    Initiates the main CrewAI flow that coordinates multiple AI agents
    to generate comprehensive documentation based on RAG research and
    structured templates.
    
    Returns
    -------
    Any
        The result object from the flow execution, typically containing
        the generated documentation and metadata about the process.
        
    Raises
    ------
    Exception
        If an error occurs during flow execution, with details about
        the specific failure wrapped in a descriptive message.
        
    Examples
    --------
    >>> result = run_flow()
    >>> print("Flow completed successfully")
    
    Notes
    -----
    This function acts as a wrapper around the flow_kickoff function
    from the flow_documentation module, providing error handling and
    a consistent interface.
    """
    try:
        result = flow_kickoff()
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow: {e}")

def plot_flow():
    """
    Generate and display flow visualization.
    
    Creates a visual representation of the CrewAI flow structure,
    showing the relationships between different agents, tasks, and
    the overall workflow architecture.
    
    Raises
    ------
    Exception
        If an error occurs during visualization generation, with details
        about the specific failure wrapped in a descriptive message.
        
    Examples
    --------
    >>> plot_flow()
    >>> print("Flow visualization generated")
    
    Notes
    -----
    This function is useful for understanding the flow structure and
    debugging the agent interaction patterns. The visualization output
    format depends on the underlying plotting implementation.
    """
    try:
        flow_plot()
    except Exception as e:
        raise Exception(f"An error occurred while plotting the flow: {e}")


if __name__ == "__main__":
    """
    Main execution block.
    
    When the script is run directly, this block executes both the
    documentation generation flow and the flow visualization.
    """
    run_flow()
    plot_flow()
