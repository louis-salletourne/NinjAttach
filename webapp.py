import streamlit as st
import json
import os
from pdf.export_missing_fields import export_missing_fields
from email_read import read_email

# JSON file path
json_file_path = "user_profile.json"

# Initialize or load the JSON file
def load_json():
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, 'r') as f:
        return json.load(f)

# Save the updated JSON data
def save_json(data):
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Main Streamlit app
def main():
    st.title("Email Agent - Powered by Gemini AI")
    st.write("Fetching the latest email...")
    output = read_email()
    print(output)
    
    attachments = output['Attachments']
    if not attachments:
        st.write("No attachments found.")
        return

    # Consider the first attachment
    path = attachments[0]
    st.write("Found and saved PDF attachement")

    # Load current user profile
    user_profile = load_json()

    # Display current user profile
    if user_profile:
        st.subheader("Current User Profile")
        st.json(user_profile)
    else:
        st.write("No user profile found.")
    
    # Extract missing fields
    extracted_info = export_missing_fields(path)  # extracted_info is a list of strings (missing fields)

    # Create a form for the user to fill in missing fields
    st.subheader("Fill in the missing fields:")
    
    # Create a dictionary to hold user inputs
    new_info = {}
    
    # Create text inputs for each missing field
    for field in extracted_info:
        new_info[field] = st.text_input(f"Enter {field}:")

    # Submit button to update the JSON file
    if st.button("Submit"):
        # Update user profile with new info
        user_profile.update(new_info)
        
        # Save the updated user profile
        save_json(user_profile)
        
        st.success("User profile updated successfully!")
        st.json(user_profile)

if __name__ == "__main__":
    main()
