import streamlit as st
import json

user_profile_path = 'user_profile.json'

# Function to load the JSON file
def load_profile(file_path=user_profile_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to save the updated profile back to the JSON file
def save_profile(data, file_path=user_profile_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to display the profile and allow updates
def display_tab():
    st.header("User Profile")

    # Load user profile data
    if 'profile' not in st.session_state:
        st.session_state['profile'] = load_profile()
    
    profile = st.session_state['profile']

    # Create input fields for each key-value pair
    updated_profile = {}
    for key, value in profile.items():
        updated_value = st.text_input(f"{key.capitalize()}", value)
        updated_profile[key] = updated_value

    # Section to add a new field
    st.subheader("Add a New Field")
    new_field_name = st.text_input("New Field Name")
    new_field_value = st.text_input("New Field Value")

    if st.button("Add New Field"):
        if new_field_name and new_field_value:
            st.session_state['profile'][new_field_name] = new_field_value
            st.success(f"New field '{new_field_name}' added!")
        else:
            st.error("Please provide both a field name and value.")
    
    # Update profile when the user clicks the button
    if st.button("Update Profile"):
        # Merge updated_profile with the session profile data
        st.session_state['profile'].update(updated_profile)
        save_profile(st.session_state['profile'])
        st.success("Profile updated successfully!")

    # Display updated profile
    st.write("Updated profile data:", st.session_state['profile'])

# Run the app
if __name__ == "__main__":
    display_tab()
