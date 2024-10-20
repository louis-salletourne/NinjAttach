import google.generativeai as genai

import ast

def string_to_dict(string):
    # Extract the part of the string that contains the dictionary
    start_index = string.find('{')
    end_index = string.rfind('}') + 1
    
    # Extract the dictionary portion from the string
    dict_string = string[start_index:end_index]
    
    # Convert the string representation of the dictionary to an actual dictionary
    try:
        dictionary = ast.literal_eval(dict_string)
        return dictionary
    except (ValueError, SyntaxError):
        return None

def find_missing_files(file, list_missing_fields):
    # Choose a Gemini model.
    output = []
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    for elt in list_missing_fields:
        prompt = f"""
        I have an image of a pdf document with missing fields.
        I want you to find where the field "{elt}" must be filled in the document.
        The output must be a dict python with the following form :
        {{
            "field": "{elt}",
            "coordinates": [x, y, width, height]
        }}
        """
        response = model.generate_content([file, prompt])
        dict_field = string_to_dict(response.text)
        output.append(dict_field)

    return output