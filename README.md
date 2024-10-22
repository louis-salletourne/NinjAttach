# Email Agent - Powered by Gemini AI

## Overview

The Email Agent is a Streamlit application designed to automate the process of extracting information from emails and PDF attachments, updating user profiles, and generating email drafts with the updated information. This project leverages various functionalities to streamline the workflow and improve efficiency.

## Features

- **Email Reading**: Automatically reads the latest email and extracts attachments.
- **PDF Information Extraction**: Extracts missing fields from PDF attachments.
- **User Profile Management**: Updates the user profile with the extracted information.
- **Form Generation**: Generates a dynamic form for users to fill in missing information.
- **Email Draft Creation**: Creates an email draft with the updated PDF attached.
- **Task Scheduling**: Automatically saves the task in the user’s Google Tasks as a reminder to send the email.

## Installation

To run this project, you need to have Python and Streamlit installed. Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/louis-salletourne/NinjAttach.git
   cd NinjAttach
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment variables**:
    - Create a `.env` file in the root directory.
    - Add the following environment variables to the `.env` file:
      ```bash
      GEMINI_API_KEY=your-gemini-api-key
      GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
      ```
    - Activate the Gmail API and download the `credentials.json` file from the Google Cloud Console.

4. **Run the Streamlit app**:
   ```bash
    streamlit run webapp.py
    ```



   

