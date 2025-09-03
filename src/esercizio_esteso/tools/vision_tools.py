"""
Vision and Image Generation Tools for CrewAI Multi-Agent System.

This module provides tools for image generation and visual content creation
using DALL-E API integration. The tools enable agents to create visual
content based on textual descriptions.

Classes
-------
MyCustomToolInput : BaseModel
    Pydantic model defining the input schema for vision tools.
DallETool : BaseTool
    Tool for generating images from textual descriptions using DALL-E.

Notes
-----
The tools require proper Azure OpenAI configuration and DALL-E API access.
The generated images are high-quality and suitable for various applications.
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import AzureOpenAI
from crewai_tools import DallETool

dalle_tool = DallETool()

load_dotenv()

class MyCustomToolInput(BaseModel):
    """
    Input schema for vision tools.
    
    Defines the input format for vision-related tools, ensuring proper
    validation and type checking for image generation requests.
    
    Attributes
    ----------
    question : str
        The description or prompt for image generation. Should be detailed
        and descriptive to achieve the best results from DALL-E.
        
    Examples
    --------
    >>> input_data = MyCustomToolInput(
    ...     question="A futuristic cityscape with flying cars at sunset"
    ... )
    """
    question: str = Field(..., description="Question to ask the tool.")

class DallETool(BaseTool):
    """
    DALL-E image generation tool.
    
    This tool provides image generation capabilities using the DALL-E API,
    allowing agents to create high-quality images from textual descriptions.
    The tool integrates with Azure OpenAI services for robust image generation.
    
    Attributes
    ----------
    name : str
        Tool identifier used by CrewAI agents.
    description : str
        Detailed description of image generation capabilities.
    args_schema : Type[BaseModel]
        Pydantic model defining the input schema.
        
    Methods
    -------
    generate_image(description: str)
        Creates an image based on the provided textual description.
        
    Examples
    --------
    >>> dalle = DallETool()
    >>> image_url = dalle.generate_image("A robot working in a garden")
    
    Notes
    -----
    The tool requires proper DALL-E API configuration and handles errors
    gracefully to ensure reliable operation within agent workflows.
    """
    name: str = "Dall-E Tool"
    description: str = (
        "This tool generates images from textual descriptions using DALL-E. "
        "Provide a detailed description of the image you want to create, and get a high-quality image in response."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def generate_image(self, description: str) -> str:
        """
        Generate an image from the provided description using DALL-E.
        
        Creates a high-quality image based on the textual description
        provided, utilizing the DALL-E API through the CrewAI tools
        integration.
        
        Parameters
        ----------
        description : str
            Detailed textual description of the desired image. Should
            include specific details about style, content, composition,
            and any other relevant visual elements.
            
        Returns
        -------
        str
            URL or path to the generated image, or an error message if
            generation fails. The response format depends on the DALL-E
            tool configuration.
            
        Raises
        ------
        Exception
            If image generation fails due to API issues, invalid input,
            or service unavailability, returns an error message with
            diagnostic information.
            
        Examples
        --------
        >>> dalle = DallETool()
        >>> result = dalle.generate_image("A sunset over a mountain lake")
        >>> print(f"Generated image: {result}")
        
        Notes
        -----
        The method wraps the underlying DALL-E tool functionality with
        error handling to ensure graceful failure in agent workflows.
        """
        try:
            response = dalle_tool.generate_image(description)
            return response
        except Exception as e:
            return f"Error generating image: {str(e)}"

