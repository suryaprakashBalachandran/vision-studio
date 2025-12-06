"""Utility functions for building AI prompts."""
from typing import Dict, Optional


def build_reference_prompt(reference_values: Dict[str, str]) -> str:
    """
    Build a structured prompt for reference-based extraction.
    
    Args:
        reference_values: Dictionary mapping field names to their labels/descriptions
                         e.g., {"invoice_number": "Invoice #", "date": "Date"}
    
    Returns:
        Formatted prompt string for the AI model
    """
    fields_list = "\n".join([
        f"- {key}: Look for '{value}'" 
        for key, value in reference_values.items()
    ])
    
    prompt = f"""You are a data extraction assistant. Extract the following information from the provided document image:

{fields_list}

Instructions:
1. Carefully analyze the document image
2. Extract the exact values for each field listed above
3. If a field is not found, set its value to null
4. Return the results in valid JSON format with the field names as keys

Example output format:
{{
    "field_name_1": "extracted_value_1",
    "field_name_2": "extracted_value_2",
    "field_name_3": null
}}

Return ONLY the JSON object, no additional text or explanation."""
    
    return prompt


def build_instruction_prompt(instructions: str) -> str:
    """
    Build a prompt based on free-text instructions.
    
    Args:
        instructions: Free-text instructions from the user
    
    Returns:
        Formatted prompt string for the AI model
    """
    prompt = f"""You are a data extraction assistant. Follow these instructions to extract data from the provided document image:

{instructions}

Instructions:
1. Carefully analyze the document image
2. Extract the requested information according to the instructions above
3. Return the results in valid JSON format
4. Use descriptive field names based on the extracted data
5. If information cannot be found, set the value to null

Return ONLY a JSON object with the extracted data, no additional text or explanation."""
    
    return prompt


def add_json_formatting_hint(prompt: str) -> str:
    """
    Add additional hints to ensure JSON output.
    
    Args:
        prompt: The base prompt
    
    Returns:
        Enhanced prompt with JSON formatting hints
    """
    return f"""{prompt}

CRITICAL: Your response must be valid JSON that can be parsed by json.loads(). 
Do not include markdown code blocks, explanations, or any text outside the JSON object."""
