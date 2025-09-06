"""
Web crew utility functions for processing and merging web search results.
"""

import json
from typing import Dict, List, Any, Union


def parse_crew_output(value) -> dict:
    """
    Accepts CrewOutput or string and returns a JSON dict.
    
    Parameters
    ----------
    value : CrewOutput or str
        The output from a crew execution or a string representation.
        
    Returns
    -------
    dict
        Parsed JSON dictionary from the input value.
        
    Raises
    ------
    ValueError
        If the input cannot be parsed as valid JSON.
    """
    # If it's a CrewOutput, get the text content
    text = getattr(value, "raw", None)
    if text is None:
        text = str(value)

    # Try direct JSON parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract the first complete JSON object
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        
        raise ValueError(f"Could not parse JSON from input: {text[:200]}...")


def merge_web_resources(crew2_payload: Union[Dict, List], web_results: Dict) -> Union[Dict, List]:
    """
    Merges web search results into the original crew payload.
    
    Parameters
    ----------
    crew2_payload : dict or list
        The original payload from the planning crew.
    web_results : dict
        The web search results to merge, containing sections with web resources.
        
    Returns
    -------
    dict or list
        The merged payload with web resources added to appropriate sections.
    """
    # Create a deep copy to avoid modifying the original
    payload = json.loads(json.dumps(crew2_payload))
    
    # Extract web resources from results
    res_sections = (web_results or {}).get("sections", {})
    if not res_sections:
        return payload  # Nothing to merge

    # Handle case where payload doesn't have sections
    sections = payload.get("sections", None)
    if sections is None:
        payload["web_resources"] = res_sections
        return payload

    # Handle list-type sections
    if isinstance(sections, list):
        # Create index mapping section names to list positions
        index = {}
        for i, section in enumerate(sections):
            name = str(section.get("name", "")).strip().lower()
            if name:
                index[name] = i
        
        # Merge web resources into matching sections
        for sec_name, items in res_sections.items():
            key = str(sec_name).strip().lower()
            if key in index:
                payload["sections"][index[key]]["web_resources"] = items
        
        return payload

    # Handle dictionary-type sections
    if isinstance(sections, dict):
        for sec_name, items in res_sections.items():
            # Try exact match first
            if sec_name in sections:
                payload["sections"][sec_name]["web_resources"] = items
            else:
                # Try case-insensitive match
                for k in list(sections.keys()):
                    if str(k).lower().strip() == str(sec_name).lower().strip():
                        payload["sections"][k]["web_resources"] = items
                        break
        
        return payload

    # Fallback: add as top-level web_resources
    payload["web_resources"] = res_sections
    return payload


def validate_web_resources_format(web_results: Dict) -> bool:
    """
    Validates the format of web search results.
    
    Parameters
    ----------
    web_results : dict
        The web search results to validate.
        
    Returns
    -------
    bool
        True if the format is valid, False otherwise.
    """
    if not isinstance(web_results, dict):
        return False
        
    sections = web_results.get("sections")
    if not isinstance(sections, dict):
        return False
        
    # Check each section has proper resource format
    for section_name, resources in sections.items():
        if not isinstance(resources, list):
            return False
            
        for resource in resources:
            if not isinstance(resource, dict):
                return False
                
            required_fields = ["title", "url", "summary", "citation"]
            if not all(field in resource for field in required_fields):
                return False
                
            # Validate citation format
            citation = resource.get("citation", {})
            if not isinstance(citation, dict):
                return False
                
            citation_fields = ["title", "url", "accessed"]
            if not all(field in citation for field in citation_fields):
                return False
    
    return True
