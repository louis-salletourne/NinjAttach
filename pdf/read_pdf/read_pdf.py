# Step 1: Reading the PDF
import google.generativeai as genai
import PyPDF2
from config import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)
page_number = 1

def read_file(file_path):
    sample_file = genai.upload_file(path=file_path, display_name="Gemini 1.5 PDF")

    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    return file

def get_page_size(file_path, page_number=1):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Initialize the PDF reader
        reader = PyPDF2.PdfReader(file)

        # Get the specified page
        page = reader.pages[page_number - 1]  # Page numbers are 0-indexed

        # Get the media box (page dimensions)
        media_box = page.mediabox

        # Extract the width and height
        width = media_box.width
        height = media_box.height

        return [width, height]

def get_pdf_metadata(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Initialize the PDF reader
        reader = PyPDF2.PdfReader(file)

        # Get the document information (metadata)
        metadata = reader.metadata

        return metadata

def read_pdf_informations(file_path, page_number=1):
    # Open the PDF file
    file = read_file(file_path)
    size = get_page_size(file_path, page_number)
    metadata = get_pdf_metadata(file_path)
    return file, size, metadata
