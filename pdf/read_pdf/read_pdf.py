# Step 1: Reading the PDF
import google.generativeai as genai

from config import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)


def read_file(file_path):
    sample_file = genai.upload_file(path=file_path, display_name="Gemini 1.5 PDF")

    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    return file
