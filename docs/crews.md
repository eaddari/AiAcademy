# Crews

The project implements multiple specialized crews, each designed for specific domains and tasks.

## Document Generation Crew (`docgen`)

Specializes in creating structured documents and reports.

**Agents:**
- `generation_agent`: Expert in document creation and formatting

**Tasks:**
- `document_generation_task`: Generates comprehensive documents based on input requirements

## Mathematical Crew (`mathcrew`)

Handles mathematical equations and computational problems.

**Agents:**
- `math_tool_agent`: Equipped with mathematical computation tools

**Tasks:**
- `math_task`: Solves mathematical problems and equations

**Tools:**
- `MathEquationsTool`: Specialized tool for mathematical calculations

## OCR Crew (`ocr_crew`)

Processes images and visual content with OCR capabilities.

**Agents:**
- `input_agent`: Analyzes and understands user input
- `dalle_agent`: Generates images using DALL-E

**Tasks:**
- `input_task`: Processes and analyzes input data
- `dalle_task`: Creates visual content based on descriptions

**Tools:**
- `DallETool`: Image generation capabilities

## Summarization Crew (`summarization_crew`)

Focuses on document summarization and content condensation.

**Agents:**
- `document_summarizer`: Expert in creating concise summaries

**Tasks:**
- `summarization_task`: Generates comprehensive summaries of input documents

## Web Research and RAG Crew (`webrag`)

Combines web research with Retrieval-Augmented Generation.

**Agents:**
- `rag_researcher`: Searches through local document collections
- `reporting_analyst`: Analyzes and reports findings

**Tasks:**
- `rag_research_task`: Performs RAG-based research
- `reporting_task`: Creates structured reports from findings

**Tools:**
- `LocalRag`: Custom RAG implementation for local document search

## Summary and Explanation Crew (`summary`)

Creates detailed explanations and summaries of complex topics.

**Agents:**
- `agent_manager`: Oversees explanation strategy
- `web_researcher`: Gathers additional information from web sources
- `expert_writer`: Creates comprehensive explanations

**Tasks:**
- `agent_manager_task`: Plans explanation approach
- `web_researcher_task`: Performs web-based research
- `expert_writer_task`: Writes detailed explanations

**Tools:**
- `SerperDevTool`: Web search capabilities
- `LocalRag`: Document retrieval system

## Crew Configuration

All crews are configured using YAML files:
- `agents.yaml`: Defines agent roles, goals, and capabilities
- `tasks.yaml`: Specifies task descriptions and requirements

Each crew follows the CrewAI framework patterns with:
- `@CrewBase` decoration
- `@agent` decorated methods for agent definitions
- `@task` decorated methods for task definitions
- `@crew` decorated method for crew assembly
