import streamlit as st
import json
import os
from pdf.export_missing_fields import export_missing_fields
from email_read import read_email, create_draft

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

    with st.form(key='info_form'):
        user_inputs = {}
        for field in extracted_info:
            user_inputs[field] = st.text_input(f"Please provide your {field}")

        # Submit button
        submitted = st.form_submit_button(label='Submit')

# Only run this when the form is submitted
    if submitted:
        # Add provided info to the user profile
        user_profile.update(user_inputs)

        # Save the updated profile to the JSON file
        save_json(user_profile)

        st.success("Profile updated successfully!")
        st.json(user_profile)  # Display updated profile

        # complete_pdf(original_pdf_path, user_profile) -> outputs a new PDF with the missing fields filled in and returns the path to the new PDF

        create_draft(output, "files/certificate_of_presence_erasmus_2023-2024 (1)_completed.pdf")

        st.write("Draft email created with the updated PDF attached.")
        st.stop()

if __name__ == "__main__":
    main()
