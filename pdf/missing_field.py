# Step 2: Identify Missing Fields (Example: look for placeholders like "_" or "TBD")
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
            I need a JSON string that accurately identifies and locates all missing fields within a given document.
            To help you, I give you the size of the original document : {size[0]} x {size[1]}.
            And the metadata of the document : {metadata}.
            For each missing field, please provide the following information:

            field: The name of the missing field.
            bbox: A bounding box specifying the field's expected location, defined by:
            x: The x-coordinate of the top-left corner.
            y: The y-coordinate of the top-left corner.
            width: The width of the bounding box.
            height: The height of the bounding box.
            Please ensure the bounding box coordinates are relative to the document's origin.
            And the coordinates must be in the referential as PyMuPDF. Output the response as a valid JSON string."""
        ],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    return response.text
