from pdf2image import convert_from_path
import os

def pdf_to_png(pdf_file_path, output_dir='output_images', dpi=300):
    """
    Converts each page of a PDF file to PNG images.

    Parameters:
    - pdf_file_path (str): The path to the PDF file to be converted.
    - output_dir (str): The directory where the PNG images will be saved.
    - dpi (int): The resolution of the output images.
    """
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_file_path, dpi=dpi)

    # Save each page as a PNG file
    for i, image in enumerate(images):
        output_file_path = os.path.join(output_dir, f'output_page_{i + 1}.png')
        image.save(output_file_path, 'PNG')
        print(f'Saved: {output_file_path}')

    print("Conversion completed!")
    return output_file_path

# Example usage:
# pdf_to_png('path/to/your/file.pdf')
