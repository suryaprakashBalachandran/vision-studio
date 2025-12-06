"""Utility functions for parsing AI model responses."""
import json
import re
from typing import Dict, Any


def parse_ai_response(response_text: str) -> Dict[str, Any]:
    """
    Parse AI model response and extract JSON data.
    
    Handles various response formats:
    - Pure JSON
    - JSON wrapped in markdown code blocks
    - JSON with additional text
    
    Args:
        response_text: Raw response text from AI model
    
    Returns:
        Parsed JSON data as dictionary
    
    Raises:
        ValueError: If no valid JSON can be extracted
    """
    # Try to parse as direct JSON first
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, response_text, re.DOTALL)
    
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Try to find any JSON object in the text
    json_object_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_object_pattern, response_text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    raise ValueError(f"Could not extract valid JSON from response: {response_text[:200]}...")


def validate_extracted_data(
    data: Dict[str, Any],
    expected_fields: list = None
) -> Dict[str, Any]:
    """
    Validate and clean extracted data.
    
    Args:
        data: Extracted data dictionary
        expected_fields: Optional list of expected field names
    
    Returns:
        Validated and cleaned data dictionary
    """
    if not isinstance(data, dict):
        raise ValueError("Extracted data must be a dictionary")
    
    # Remove any None values or empty strings if needed
    cleaned_data = {
        k: v for k, v in data.items()
        if v is not None and v != ""
    }
    
    return cleaned_data


def extract_confidence_scores(response_text: str) -> Dict[str, float]:
    """
    Extract confidence scores if provided by the AI model.
    
    Some models may include confidence scores in their responses.
    This function attempts to extract them.
    
    Args:
        response_text: Raw response text from AI model
    
    Returns:
        Dictionary of field names to confidence scores
    """
    # This is a placeholder - actual implementation depends on model output format
    # Most vision models don't provide confidence scores by default
    return {}
