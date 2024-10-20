import streamlit as st
import json
import os
from easy_pdf.main import export_missing_fields
from email_read import read_email, create_draft
from gemini_request.gemini_request import found_and_missing_infos
from gemini_request.clean_fields import clean_fields
from easy_pdf.fill_missing_files import fill_missing_fields
from tabs import profile_settings

@st.cache_resource
def cached_read_email():
    return read_email()

@st.cache_resource
def cached_create_draft(_output, completed_file):
    return create_draft(_output, completed_file)

@st.cache_resource
def cached_found_and_missing_fields(user_profile, path):
    missing_fields = export_missing_fields(path)
    return found_and_missing_infos(user_profile, missing_fields)

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

def IndirectObject(*args):
    return None

# Main Streamlit app
def main():
    st.title("Email Agent - Powered by Gemini AI")
    st.write("Fetching the latest email...")

    # Create tabs
    tab1, tab2 = st.tabs(["Process Email", "Profile Settings"])

    with tab1:
        # Read the email to extract attachments
        output = cached_read_email()
        attachments = output['Attachments']

        if not attachments:
            st.write("No attachments found.")
            return

        # Consider the first attachment
        pdf_path = attachments[0]
        st.write("Found and saved PDF attachment")

        # Load current user profile
        original_user_profile = load_json()
        user_profile = original_user_profile.copy()

        # Display current user profile if available
        if user_profile:
            st.subheader("Current User Profile")
            st.json(user_profile)
        else:
            st.write("No user profile found.")

        # Extract missing fields from the PDF
        found_info, missing_info = cached_found_and_missing_fields(user_profile, pdf_path)

        if not missing_info:
            st.write("All required information is already present in the user profile.")
            create_draft(output, "files/certificate_of_presence_erasmus_2023-2024 (1)_completed.pdf")
            st.write("Draft email created with the updated PDF attached.")
            return

        # Create a form for the user to fill in missing fields
        st.subheader("Fill in the missing fields:")

        # Use a form to delay execution until the submit button is pressed
        with st.form(key='info_form'):
            user_inputs = {}
            for field, answer in found_info.items():
                user_inputs[field] = st.text_input(field, value=answer, key=field)
            for field, info in missing_info.items():
                if info.get('/FT') == '/Tx':
                    help_text = info.get('/TU', '')
                    user_inputs[field] = st.text_input(info.get('/T', field), placeholder=help_text)

            # Submit button
            submitted = st.form_submit_button(label='Submit')

        # Only process the form when submitted
        if submitted:
            for field, value in user_inputs.items():
                if value.strip():
                    user_profile[field] = value
            
            user_profile_new_part = {key: user_profile[key] for key in missing_info.keys() if key in user_profile}
            new_part_clean = clean_fields(user_profile_new_part)

            original_user_profile.update(new_part_clean)
            save_json(original_user_profile)

            saved_profile = load_json()
            st.success("Profile updated successfully!")
            st.json(saved_profile)

            output_file_name = pdf_path.replace('.pdf', '') + "_completed.pdf"
            _ = fill_missing_fields(pdf_path=pdf_path, user_profile=user_profile, output_file_name=output_file_name)

            cached_create_draft(output, output_file_name)
            st.write("Draft email created with the updated PDF attached.")

    with tab2:
        # Call the display_tab function from the profile_settings module
        profile_settings.display_tab()

if __name__ == "__main__":
    main()
