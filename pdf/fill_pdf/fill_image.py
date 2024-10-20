from PIL import Image, ImageDraw, ImageFont
import json

def fill_image(image_path, json_path, output_image_path='output_image.png'):
    """
    Draws fields on the image at specified coordinates from a JSON file.

    Args:
        image_path (str): Path to the input image.
        json_path (str): Path to the JSON file with fields and coordinates.
        output_image_path (str): Path to save the output image. Default is 'output_image.png'.
        
    Returns:
        None
    """
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Load the JSON data
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Define a font
    try:
        font = ImageFont.truetype("arial.ttf", 14)  # Use Arial font, size 14
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if Arial is not available

    # Iterate over the JSON data and draw each field
    for entry in data:
        if entry:  # Skip None entries
            field_text = entry['field']
            coordinates = entry['coordinates']
            
            # Draw the field text at the specified coordinates
            draw.text((coordinates[0], coordinates[1]), field_text, font=font, fill="black")

    # Save the new image
    img.save(output_image_path)
    print(f"Image saved as {output_image_path}")
    return output_image_path