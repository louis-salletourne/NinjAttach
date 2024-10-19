# Step 3: Fill the Fields Using AI (Example: using a pre-trained GPT model from OpenAI API)
import json

def to_json(input_string, output_file_path):
    # Remove the markdown code block syntax
    json_string = input_string.replace('```json\n', '').replace('\n```', '')

    # Parse the JSON string
    data = json.loads(json_string)

    # Write the JSON data to a file
    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("JSON file created successfully!")
    