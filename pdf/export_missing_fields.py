from read_pdf.read_pdf import read_pdf_informations
from read_pdf.missing_field import identify_missing_fields
from read_pdf.to_json import to_json

pdf_file = "./tests/test_pdf/test/test_1.pdf"
json_file = "./tests/test_pdf/test/missing_fields.json"

def export_missing_fields(pdf_file, json_file):
    file, size, metadata = read_pdf_informations(pdf_file)
    json = identify_missing_fields(file, size, metadata)
    to_json(json, json_file)
    with open(json_file, 'r') as file:
        data = json.load(file)
    return [item['field'] for item in data]
