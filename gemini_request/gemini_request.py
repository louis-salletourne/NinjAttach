import json
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

def found_and_missing_infos(user_profile: dict, widgets: dict) ->  (dict, dict): # type: ignore
    model = genai.GenerativeModel("gemini-1.5-flash")

    list_missing_infos = list(widgets.keys()) # Create a list of the keys

    prompt = f"""
    I have a list of user information keys: {list_missing_infos}. 
    I also have a dictionary with user information: {user_profile}. 
    Please analyze the list and find corresponding keys in the dictionary. 
    The keys in the list may not match exactly with the dictionary keys, but they should represent similar information. 
    For example, 'email' in the list could correspond to 'email_address' in the dictionary.
    Your output should be a valid JSON string, evenf if it is empty, containing only the matched keys from the list and their corresponding values from the dictionary. 
    Do not include any additional text or explanations, just return the JSON string.
    """

    response = model.generate_content(prompt,
                safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            },)
    
    informations_in_user_profile = json.loads(response.text.strip())
    informations_not_in_user_profile = {key: widgets[key] for key in list_missing_infos if key not in informations_in_user_profile}

    return informations_in_user_profile, informations_not_in_user_profile