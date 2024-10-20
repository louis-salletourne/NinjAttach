# Step 2: Identify Missing Fields (Example: look for placeholders like "_____" or "TBD")
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory


def identify_missing_fields(sample_file: str, size: list, metadata: dict):
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content(
        [
            sample_file,
            f"""
            I need a JSON string that accurately identifies and locates all missing fields within a given pdf document.
            Missing fields may include empty fields, fields with placeholder text like "_____" or "TBD", fields with inconsistent formatting, or fields that lack expected content.
            The metadata of the document is {metadata}.

            For each missing field, please provide the following information:

            field: The name of the missing field.
           
            Please ensure the bounding box coordinates are relative to the document's origin. Make sure that the original resolution stays the same when processing the same. 
            Output the response as a valid JSON string.

            """
        
        ],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
    )


    return response.text
