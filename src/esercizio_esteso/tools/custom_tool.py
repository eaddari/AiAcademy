"""
Custom Tools for CrewAI Multi-Agent System.

This module provides custom tools that extend the capabilities of CrewAI agents,
including local Retrieval-Augmented Generation (RAG) functionality and
mathematical equation solving tools.

Classes
-------
MyCustomToolInput : BaseModel
    Pydantic model defining the input schema for custom tools.
LocalRag : BaseTool
    Tool for performing local RAG operations using FAISS and Azure OpenAI.
MathEquationsTool : BaseTool
    Tool for solving mathematical equations and performing calculations.

Notes
-----
The tools require proper environment configuration for Azure OpenAI access
and depend on the FAISS vector database for RAG functionality.
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import AzureOpenAI
load_dotenv()

class MyCustomToolInput(BaseModel):
    """
    Input schema for custom tools.
    
    Defines the standard input format for all custom tools in the system,
    ensuring consistent parameter validation and type checking.
    
    Attributes
    ----------
    question : str
        The question or input text to be processed by the tool.
        This field is required and must contain meaningful content
        for the tool to process effectively.
        
    Examples
    --------
    >>> input_data = MyCustomToolInput(question="What is machine learning?")
    >>> print(input_data.question)
    """
    question: str = Field(..., description="Question to ask the tool.")

class LocalRag(BaseTool):
    """
    Local Retrieval-Augmented Generation (RAG) tool.
    
    This tool performs local RAG operations using FAISS vector database
    and Azure OpenAI for embeddings and response generation. It enables
    agents to answer questions based on local document collections with
    semantic search and citation capabilities.
    
    Attributes
    ----------
    name : str
        Tool identifier used by CrewAI agents.
    description : str
        Detailed description of tool capabilities and usage.
    args_schema : Type[BaseModel]
        Pydantic model defining the input schema.
        
    Methods
    -------
    _get_python_executable()
        Determines the correct Python executable path for the virtual environment.
    _load_rag_functions()
        Dynamically imports RAG functionality modules.
    _run(question: str)
        Executes the RAG pipeline with the provided question.
        
    Examples
    --------
    >>> rag_tool = LocalRag()
    >>> result = rag_tool._run("What is the system architecture?")
    
    Notes
    -----
    The tool requires a pre-indexed FAISS database and proper Azure OpenAI
    configuration. Error handling ensures graceful degradation when
    components are unavailable.
    """
    name: str = "Local RAG"
    description: str = (
        "This tool performs local retrieval-augmented generation using FAISS and Azure OpenAI. "
        "It can answer questions based on local documents using a RAG pipeline with embeddings, "
        "vector search, and response generation. Provide a question and get an answer with source citations."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput
    
    def _get_python_executable(self):
        """
        Get the Python executable path for the virtual environment.
        
        Determines the correct Python executable to use, preferring the
        virtual environment Python over the system Python installation.
        
        Returns
        -------
        str
            Absolute path to the Python executable. Returns the virtual
            environment Python if available, otherwise falls back to "python".
            
        Notes
        -----
        This method ensures that RAG operations use the correct Python
        environment with all required dependencies installed.
        """
        webrag_root = Path(__file__).parent.parent.parent.parent
        venv_python = webrag_root / ".venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            return str(venv_python)
        return "python"  # fallback
    
    def _load_rag_functions(self):
        """
        Import RAG functions dynamically.
        
        Dynamically imports the FAISS RAG module, handling path configuration
        to ensure the module can be found regardless of the execution context.
        
        Returns
        -------
        module
            The imported faiss_rag module containing RAG functionality.
            
        Raises
        ------
        RuntimeError
            If the faiss_rag module cannot be imported, typically due to
            missing dependencies or incorrect path configuration.
            
        Notes
        -----
        The function adds the RAG directory to the Python path before
        attempting import, ensuring the module can be found from any
        execution context.
        """
        try:
            # Add the rag directory to Python path
            rag_dir = Path(__file__).parent.parent / "crews" / "rag"
            if str(rag_dir) not in sys.path:
                sys.path.insert(0, str(rag_dir))
            
            # Import the functions we need
            import faiss_rag
            
            return faiss_rag
            
        except ImportError as e:
            raise RuntimeError(f"Could not import faiss_rag module: {str(e)}")

    def _run(self, question: str) -> str:
        """
        Run the RAG system with the provided question.
        
        Executes the complete RAG pipeline including document retrieval,
        context extraction, and response generation using Azure OpenAI.
        
        Parameters
        ----------
        question : str
            The question or query to be processed through the RAG system.
            Should be a well-formed question that can benefit from document
            context and semantic search.
            
        Returns
        -------
        str
            The generated response based on retrieved documents and the
            question context. Includes relevant information and source
            citations when available.
            
        Raises
        ------
        Exception
            If any component of the RAG pipeline fails, returns an error
            message describing the specific failure.
            
        Notes
        -----
        The method attempts to load RAG functions dynamically and falls
        back to a simple query processing approach if the full RAG
        system is unavailable.
        """
        try:
            # Load RAG functions
            faiss_rag = self._load_rag_functions()
            
            # Initialize components
            settings = faiss_rag.SETTINGS
            embeddings = faiss_rag.get_embeddings(settings)
            llm_model = faiss_rag.llm()
            
            # Load or build vector store
            docs = faiss_rag.corpus()
            vector_store = faiss_rag.load_or_build_vectorstore(settings, embeddings, docs)
            
            # Create retriever and chain
            retriever = faiss_rag.make_retriever(vector_store, settings)
            rag_chain = faiss_rag.build_rag_chain(llm_model, retriever)
            
            # Get answer
            answer = faiss_rag.rag_answer(question, rag_chain)
            
            return answer
            
        except Exception as e:
            return f"Error running RAG query: {str(e)}\n\nPlease ensure your Azure OpenAI credentials are properly configured in the .env file."

class MathEquationsTool(BaseTool):
    """
    Mathematical equations solver tool.
    
    This tool provides mathematical problem-solving capabilities using
    Azure OpenAI to parse, solve, and explain mathematical equations
    with step-by-step solutions.
    
    Attributes
    ----------
    name : str
        Tool identifier used by CrewAI agents.
    description : str
        Detailed description of mathematical solving capabilities.
    args_schema : Type[BaseModel]
        Pydantic model defining the input schema.
        
    Methods
    -------
    _run(question: str)
        Processes mathematical questions and returns solutions.
        
    Examples
    --------
    >>> math_tool = MathEquationsTool()
    >>> result = math_tool._run("Solve: 2x + 5 = 15")
    
    Notes
    -----
    The tool uses Azure OpenAI with specific prompting to ensure
    mathematical accuracy and provides Python-executable equations
    when appropriate.
    """
    name: str = "Math Equations Solver"
    description: str = (
        "This tool solves mathematical equations and provides step-by-step solutions. "
        "Input a math problem, and it will return the solution along with the steps taken to solve it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput
    
    def _run(self, question: str) -> str:
        """
        Process mathematical questions and return solutions.
        
        Executes mathematical problem-solving using Azure OpenAI with
        specialized prompting for mathematical accuracy and clarity.
        
        Parameters
        ----------
        question : str
            The mathematical question or equation to be solved.
            Can include algebraic expressions, numerical calculations,
            or word problems requiring mathematical analysis.
            
        Returns
        -------
        str
            The mathematical solution including step-by-step explanation
            and Python-executable equations when applicable.
            
        Raises
        ------
        Exception
            If Azure OpenAI service is unavailable or authentication
            fails, returns an error message with troubleshooting guidance.
            
        Notes
        -----
        The method uses temperature=0 for consistent mathematical results
        and includes retry logic for robust operation.
        """
        try:
            client = AzureOpenAI(
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                model=os.getenv("AZURE_OPENAI_MODEL"),
                temperature=0,
                max_retries=3
            )
    
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_MODEL"),
                messages=[
                    {"role": "system", "content": "You are a helpful math assistant which transforms user input into correct math equations. The equations must be runnable in standard python."},
                    {"role": "user", "content": question}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error executing math solver: {str(e)}"