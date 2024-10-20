import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

import ast
def convert_to_list(output_string):
    # Extract the list part from the output string
    try:
        # The output string might have additional formatting like markdown code blocks
        start_index = output_string.index("[")
        end_index = output_string.index("]") + 1
        list_str = output_string[start_index:end_index]
        
        # Safely evaluate the extracted string as a Python list
        python_list = ast.literal_eval(list_str)
        return python_list
    except (ValueError, SyntaxError, IndexError) as e:
        print("Error parsing the output string:", e)
        return []

def clean_fields(missing_infos: dict) -> dict:
    model = genai.GenerativeModel("gemini-1.5-flash")

    list_missing_infos = list(missing_infos.keys()) # Create a list of the keys

    prompt = f"""
    I have a list of user information keys: {list_missing_infos}. 
    Please rename each key to be more descriptive and relevant. 

    ### Instructions:
    - Ensure that each new key clearly conveys its purpose.
    - Provide the new names in the same order as the original keys.
    - The output must be formatted as a Python list, with each new name as a string.
    - For example: 
    - 'Identification no' should be renamed to 'ID Number'.
    Can you try to add details that are not explicit.
    
    Here are the original keys:
    {list_missing_infos}

    Please provide the new names below:
    """

    response = model.generate_content(prompt,
                safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            },)

    new_names = response.text
    new_list = convert_to_list(new_names)

    # Create a mapping from original keys to new descriptive names
    original_keys = list(missing_infos.keys())
    key_mapping = dict(zip(original_keys, new_list))

    # Create a new dictionary with updated keys
    updated_dict = {key_mapping[key]: value for key, value in missing_infos.items() if key in key_mapping}

    return updated_dict

