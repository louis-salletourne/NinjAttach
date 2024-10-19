# Step 2: Identify Missing Fields (Example: look for placeholders like "_____" or "TBD")
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory


def identify_missing_fields(sample_file: str):
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content(
        [
            sample_file,
            "Can you give me a json file with that detects the missing fields, and the position where they should be."
            + "The keys for each missing field are : 'field' : str, 'bbox: [{'x': int, 'y': int, 'width': int, 'height': int}]'",
        ],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    return response.text
