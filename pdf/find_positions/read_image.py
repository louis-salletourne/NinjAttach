# Step 1: Reading the PDF
import google.generativeai as genai
import PyPDF2
from config import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)
page_number = 1

def read_file(file_path):
    # Upload the file and print a confirmation.
    sample_file = genai.upload_file(path=file_path,
                                display_name="Image")

    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    return file