import json
import fitz  # PyMuPDF

def write_fields_to_pdf(pdf_path, json_path, output_pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Load the JSON file
    with open(json_path, 'r') as json_file:
        fields = json.load(json_file)

    # Iterate through each field and write it to the PDF
    for field in fields:
        field_name = field['field']
        bbox = field['bbox']
        x = bbox['x']
        y = bbox['y']
        width = bbox['width']
        height = bbox['height']

        # Calculate the position for the text
        rect = fitz.Rect(x, y, x + width, y + height)

        # Write the field name to the PDF
        pdf_document[0].insert_textbox(rect, field_name, fontsize=10, color=(0, 0, 0), align=0)  # 0 for left alignment

    # Save the modified PDF to the output path
    pdf_document.save(output_pdf_path)
    pdf_document.close()