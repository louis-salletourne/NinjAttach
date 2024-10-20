import streamlit as st
import json
import os
from easy_pdf.main import export_missing_fields
from email_read import read_email, create_draft
from gemini_request.gemini_request import found_and_missing_infos
from gemini_request.clean_fields import clean_fields
from easy_pdf.fill_missing_files import fill_missing_fields

@st.cache_resource
def cached_read_email():
    return read_email()

@st.cache_resource
def cached_create_draft(_output, completed_file):
    return create_draft(_output, completed_file)

@st.cache_resource
def cached_found_and_missing_fields(user_profile,path):
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
    found_info, missing_info = cached_found_and_missing_fields(user_profile, pdf_path)  # Assume this is a list of missing fields (e.g., ['Name', 'Date of Birth'])
    # found_info = {'Identification no': '123456789', 'Yr Model': '2023', 'Make': 'Toyota'}
    # missing_info = {'Lic Plate No': {'/T': 'Lic Plate No', '/FT': '/Tx', '/TU': 'license plate or CF number.', '/Ff': 8388608, '/V': 'Lic Plate No', '/Kids': [IndirectObject(43, 0, 4633771232), IndirectObject(45, 0, 4633771232)]}, 'M/C Eng No': {'/T': 'M/C Eng No', '/FT': '/Tx', '/TU': 'motorcycle engine number.', '/Ff': 8388608, '/V': 'M/C Eng No', '/Kids': [IndirectObject(46, 0, 4633771232), IndirectObject(48, 0, 4633771232)]}, "Print seller's name": {'/T': "Print seller's name", '/FT': '/Tx', '/TU': "enter seller's name.", '/Ff': 8388608, '/V': "Print seller's name", '/Kids': [IndirectObject(49, 0, 4633771232), IndirectObject(51, 0, 4633771232)]}, "Printed Buyer's name": {'/T': "Printed Buyer's name", '/FT': '/Tx', '/TU': 'enter buyers names.', '/Ff': 8388608, '/V': "Printed Buyer's name", '/Kids': [IndirectObject(52, 0, 4633771232), IndirectObject(54, 0, 4633771232)]}, 'Month': {'/T': 'Month', '/FT': '/Tx', '/TU': 'enter month of transfer.', '/V': 'Month', '/Kids': [IndirectObject(55, 0, 4633771232), IndirectObject(57, 0, 4633771232)]}, 'Day': {'/T': 'Day', '/FT': '/Tx', '/TU': 'day.', '/V': 'Day', '/Kids': [IndirectObject(58, 0, 4633771232), IndirectObject(60, 0, 4633771232)]}, 'Year-1': {'/T': 'Year-1', '/FT': '/Tx', '/TU': 'first number of year of  transfer.', '/V': 'Year-1', '/Kids': [IndirectObject(61, 0, 4633771232), IndirectObject(63, 0, 4633771232)]}, 'Year-2': {'/T': 'Year-2', '/FT': '/Tx', '/TU': 'second number of year of  transfer.', '/V': 'Year-2', '/Kids': [IndirectObject(64, 0, 4633771232), IndirectObject(66, 0, 4633771232)]}, 'Year-3': {'/T': 'Year-3', '/FT': '/Tx', '/TU': 'third number of year of  transfer.', '/V': 'Year-3', '/Kids': [IndirectObject(67, 0, 4633771232), IndirectObject(69, 0, 4633771232)]}, 'Year-4': {'/T': 'Year-4', '/FT': '/Tx', '/TU': 'fourth number of year of  transfer.', '/V': 'Year-4', '/Kids': [IndirectObject(70, 0, 4633771232), IndirectObject(72, 0, 4633771232)]}, 'Selling Price': {'/T': 'Selling Price', '/FT': '/Tx', '/TU': 'enter selling price.', '/V': 'Selling Price', '/Kids': [IndirectObject(73, 0, 4633771232), IndirectObject(77, 0, 4633771232)], '/AA': {'/F': IndirectObject(75, 0, 4633771232), '/K': IndirectObject(76, 0, 4633771232)}}, 'Relationship': {'/T': 'Relationship', '/FT': '/Tx', '/TU': 'enter relationship to buyer if this was a gift. example,  parents, spouse, excetra.', '/Ff': 8388608, '/V': 'Relationship', '/Kids': [IndirectObject(78, 0, 4633771232), IndirectObject(80, 0, 4633771232)]}, 'Gift Value': {'/T': 'Gift Value', '/FT': '/Tx', '/TU': 'enter gift value.', '/V': 'Gift Value', '/Kids': [IndirectObject(81, 0, 4633771232), IndirectObject(85, 0, 4633771232)], '/AA': {'/F': IndirectObject(83, 0, 4633771232), '/K': IndirectObject(84, 0, 4633771232)}}, 'Seller print name 1': {'/T': 'Seller print name 1', '/FT': '/Tx', '/TU': "seller. i certify or declare under penalty of perjury under the laws of the state of california that the foregoing is true and correct. enter first seller's name.", '/Ff': 8388608, '/V': 'Seller print name 1', '/Kids': [IndirectObject(86, 0, 4633771232), IndirectObject(88, 0, 4633771232)]}, 'Sell date 1': {'/T': 'Sell date 1', '/FT': '/Tx', '/TU': 'date of signature.', '/V': 'Sell date 1', '/Kids': [IndirectObject(89, 0, 4633771232), IndirectObject(93, 0, 4633771232)], '/AA': {'/F': IndirectObject(91, 0, 4633771232), '/K': IndirectObject(92, 0, 4633771232)}}, 'DL, ID, Dealer No 1': {'/T': 'DL, ID, Dealer No 1', '/FT': '/Tx', '/TU': 'driver license, I D or dealer number.', '/Ff': 8388608, '/V': 'DL, ID, Dealer No 1', '/Kids': [IndirectObject(94, 0, 4633771232), IndirectObject(96, 0, 4633771232)]}, 'Seller print name 2': {'/T': 'Seller print name 2', '/FT': '/Tx', '/TU': "enter second seller's name.", '/Ff': 8388608, '/V': 'Seller print name 2', '/Kids': [IndirectObject(97, 0, 4633771232), IndirectObject(99, 0, 4633771232)]}, 'Sell date 2': {'/T': 'Sell date 2', '/FT': '/Tx', '/TU': 'DATE OF SIGNATURE.', '/V': 'Sell date 2', '/Kids': [IndirectObject(100, 0, 4633771232), IndirectObject(104, 0, 4633771232)], '/AA': {'/F': IndirectObject(102, 0, 4633771232), '/K': IndirectObject(103, 0, 4633771232)}}, 'DL, ID, Dealer No 2': {'/T': 'DL, ID, Dealer No 2', '/FT': '/Tx', '/TU': 'driver license, I D or dealer number.', '/Ff': 8388608, '/V': 'DL, ID, Dealer No 2', '/Kids': [IndirectObject(105, 0, 4633771232), IndirectObject(107, 0, 4633771232)]}, 'Seller mail address': {'/T': 'Seller mail address', '/FT': '/Tx', '/TU': 'mailing address for sellers.', '/Ff': 8388608, '/V': 'Seller mail address', '/Kids': [IndirectObject(108, 0, 4633771232), IndirectObject(110, 0, 4633771232)]}, 'Seller City': {'/T': 'Seller City', '/FT': '/Tx', '/TU': 'city.', '/Ff': 8388608, '/V': 'Seller City', '/Kids': [IndirectObject(111, 0, 4633771232), IndirectObject(113, 0, 4633771232)]}, 'Seller State': {'/T': 'Seller State', '/FT': '/Tx', '/TU': 'state.', '/Ff': 8388608, '/V': 'Seller State', '/Kids': [IndirectObject(114, 0, 4633771232), IndirectObject(116, 0, 4633771232)]}, 'Sell zip': {'/T': 'Sell zip', '/FT': '/Tx', '/TU': 'zip code.', '/V': 'Sell zip', '/Kids': [IndirectObject(117, 0, 4633771232), IndirectObject(121, 0, 4633771232)], '/AA': {'/F': IndirectObject(119, 0, 4633771232), '/K': IndirectObject(120, 0, 4633771232)}}, 'Daytime phone': {'/T': 'Daytime phone', '/FT': '/Tx', '/TU': 'daytime telephone number.', '/Ff': 8388608, '/V': 'Daytime phone', '/Kids': [IndirectObject(122, 0, 4633771232), IndirectObject(124, 0, 4633771232)]}, 'Buyer print name 1': {'/T': 'Buyer print name 1', '/FT': '/Tx', '/TU': 'buyer. enter name of first buyer.', '/Ff': 8388608, '/V': 'Buyer print name 1', '/Kids': [IndirectObject(125, 0, 4633771232), IndirectObject(127, 0, 4633771232)]}, 'Buyer print name 2': {'/T': 'Buyer print name 2', '/FT': '/Tx', '/TU': 'enter name of second buyer.', '/Ff': 8388608, '/V': 'Buyer print name 2', '/Kids': [IndirectObject(128, 0, 4633771232), IndirectObject(130, 0, 4633771232)]}, 'Buy mail address': {'/T': 'Buy mail address', '/FT': '/Tx', '/TU': "enter buyer's mailing address.", '/Ff': 8388608, '/V': 'Buy mail address', '/Kids': [IndirectObject(131, 0, 4633771232), IndirectObject(133, 0, 4633771232)]}, 'Buyer City': {'/T': 'Buyer City', '/FT': '/Tx', '/TU': 'city.', '/Ff': 8388608, '/V': 'Buyer City', '/Kids': [IndirectObject(134, 0, 4633771232), IndirectObject(136, 0, 4633771232)]}, 'Buyer State': {'/T': 'Buyer State', '/FT': '/Tx', '/TU': 'state.', '/Ff': 8388608, '/V': 'Buyer State', '/Kids': [IndirectObject(137, 0, 4633771232), IndirectObject(139, 0, 4633771232)]}, 'Buyer zip': {'/T': 'Buyer zip', '/FT': '/Tx', '/TU': 'zip code.', '/Ff': 8388608, '/V': 'Buyer zip', '/Kids': [IndirectObject(140, 0, 4633771232), IndirectObject(144, 0, 4633771232)], '/AA': {'/F': IndirectObject(142, 0, 4633771232), '/K': IndirectObject(143, 0, 4633771232)}}, 'Clear Form': {'/T': 'Clear Form', '/FT': '/Btn', '/TU': 'click this button to Clear Form.', '/Ff': 65536}, 'Print': {'/T': 'Print', '/FT': '/Btn', '/TU': 'click this button to Print.', '/Ff': 65536}}

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

        # Add only non-empty user-provided info to the user profile
        for field, value in user_inputs.items():
            if value.strip():  # Only update if a value was provided and it's not just whitespace
                user_profile[field] = value
        
        user_profile_new_part = {key: user_profile[key] for key in missing_info.keys() if key in user_profile}
        new_part_clean = clean_fields(user_profile_new_part)

        original_user_profile.update(new_part_clean)

        # Save the updated profile to the JSON file
        save_json(original_user_profile)

        # Debugging: Load and display the saved profile to ensure it was written correctly
        saved_profile = load_json()

        st.success("Profile updated successfully!")
        st.json(saved_profile)  # Display the updated profile

        output_file_name = pdf_path.replace('.pdf', '') + "_completed.pdf"

        _ = fill_missing_fields(pdf_path = pdf_path, user_profile = user_profile, output_file_name = output_file_name)

        # Call function to create an email draft with the updated PDF attached
        cached_create_draft(output, output_file_name)
        st.write("Draft email created with the updated PDF attached.")


if __name__ == "__main__":
    main()
