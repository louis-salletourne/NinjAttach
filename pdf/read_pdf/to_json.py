# Step 3: Fill the Fields Using AI (Example: using a pre-trained GPT model from OpenAI API)
import json


def to_json(missing_file: str, output_path: str):
    # Step 1: Clean the input string
    cleaned_string = missing_file.strip("```json\n").strip("```")

    # Step 2: Parse the string into a JSON object
    data = json.loads(cleaned_string)

    # Step 3: Write the JSON object to a file
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON file created successfully!")
