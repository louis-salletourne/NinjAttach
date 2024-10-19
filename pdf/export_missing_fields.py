import os

from read_pdf.read_pdf import read_pdf_informations
from read_pdf.missing_field import identify_missing_fields
from read_pdf.to_json import to_json

pdf_file = "./tests/test_pdf/test/test_1.pdf"
json_file = "json_file.json"

def export_missing_fields(pdf_file):
    file, size, metadata = read_pdf_informations(pdf_file)
    json = identify_missing_fields(file, size, metadata)
    to_json(json, json_file)
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Check if the file exists, then delete it
    if os.path.exists(json_file):
        os.remove(json_file)
        print(f"{json_file} has been deleted.")
    else:
        print(f"{json_file} does not exist.")
    return [item['field'] for item in data]
