from PyPDF2 import PdfReader

def list_widgets(pdf_path):
    """Lists all the widget names in a PDF file."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            fields = reader.get_fields()
            
            return fields
            
    except FileNotFoundError:
        print(f"The file {pdf_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")