import fitz  # PyMuPDF
from pathlib import Path
import json  # Import the json module
output_file_name = 'files/output.pdf'  # Assuming the output file will also be in the current directory

def fill_missing_fields(pdf_path: str, user_profile: dict, output_file_name: str = output_file_name):
    # Load the data from the JSON file
    entry_data = user_profile

    # Open the PDF document
    with fitz.open(pdf_path) as doc:
        target_page = doc[0]  # Assuming we want to edit the first page


        # Iterate over each form field in the PDF and fill it with the data from JSON
        for field in target_page.widgets():
            field_name = field.field_name  # Get the field name
            if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:  # If the field is a text field
                field.field_value = entry_data.get(field_name, '')  # Get the corresponding value from JSON
                field.update()  # Update the field in the PDF

            elif field.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:  # If the field is a checkbox
                field.field_value = entry_data.get(field_name, False)  # Get the checkbox value (True/False)
                field.update()  # Update the field in the PDF
            

        doc.save(output_file_name)  # Save the updated PDF

    print(f"Form filled and saved to {output_file_name}")
    return output_file_name
