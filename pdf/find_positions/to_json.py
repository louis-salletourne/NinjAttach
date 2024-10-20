import json

def create_json_file(data, filename):
    """
    Creates a JSON file from a list of dictionaries, removing None entries.

    Args:
        data (list): List of dictionaries containing field names and coordinates.
        filename (str): The name of the JSON file to be created.

    Returns:
        filename (str): The name of the created JSON file.
    """
    # Filter out None values
    cleaned_data = [entry for entry in data if entry is not None]
    
    # Write to the JSON file
    with open(filename, 'w') as json_file:
        json.dump(cleaned_data, json_file, indent=4)
    
    print(f"JSON file '{filename}' created successfully.")
    return filename