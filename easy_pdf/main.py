from easy_pdf.list_missing_fields import list_widgets

pdf_path = 'tests/test_pdf/test/test_1.pdf'
output_path = 'output.pdf'

def export_missing_fields(pdf_file: str) -> list:

    widgets = list_widgets(pdf_path = pdf_file)
    return widgets

