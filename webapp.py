import streamlit as st
import json
import os
from pdf.export_missing_fields import export_missing_fields
from email_read import read_email, create_draft

@st.cache_resource
def cached_read_email():
    return read_email()

@st.cache_resource
def cached_export_missing_fields(path):
    return export_missing_fields(path)

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

    # Read the email to extract attachments
    output = cached_read_email()
    attachments = output['Attachments']

    if not attachments:
        st.write("No attachments found.")
        return

    # Consider the first attachment
    path = attachments[0]
    st.write("Found and saved PDF attachment")

    # Load current user profile
    user_profile = load_json()

    # Display current user profile if available
    if user_profile:
        st.subheader("Current User Profile")
        st.json(user_profile)
    else:
        st.write("No user profile found.")

    # Extract missing fields from the PDF
    extracted_info = cached_export_missing_fields(path)  # Assume this is a list of missing fields (e.g., ['Name', 'Date of Birth'])
    print(extracted_info)

    # Filter out fields that are already in the user profile
    missing_info = [field for field in extracted_info if field not in user_profile]

    if not missing_info:
        st.write("All required information is already present in the user profile.")
        # complete_pdf(path, user_profile)  # Adjust this function as per your implementation
        create_draft(output, "files/certificate_of_presence_erasmus_2023-2024 (1)_completed.pdf")
        st.write("Draft email created with the updated PDF attached.")
        return

    # Create a form for the user to fill in missing fields
    st.subheader("Fill in the missing fields:")

    # Use a form to delay execution until the submit button is pressed
    with st.form(key='info_form'):
        user_inputs = {}
        for field in missing_info:
            user_inputs[field] = st.text_input(f"Please provide your {field}")

        # Submit button
        submitted = st.form_submit_button(label='Submit')

    # Only process the form when submitted
    if submitted:
        # Debugging: Print user_inputs to see if values are captured
        st.write("User inputs:", user_inputs)

        # Add only non-empty user-provided info to the user profile
        for field, value in user_inputs.items():
            if value.strip():  # Only update if a value was provided and it's not just whitespace
                user_profile[field] = value

        # Save the updated profile to the JSON file
        save_json(user_profile)

        # Debugging: Load and display the saved profile to ensure it was written correctly
        saved_profile = load_json()

        st.success("Profile updated successfully!")
        st.json(saved_profile)  # Display the updated profile

        # Call function to complete the PDF with the updated user profile info
        # complete_pdf(path, user_profile)  # Adjust this function as per your implementation

        # Call function to create an email draft with the updated PDF attached
        create_draft(output, "files/certificate_of_presence_erasmus_2023-2024 (1)_completed.pdf")

        st.write("Draft email created with the updated PDF attached.")


if __name__ == "__main__":
    main()
