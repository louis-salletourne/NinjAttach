import os.path
import json
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import shutil


# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def read_email():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels and reads emails.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            # Load the file as a dictionary
            token_data = json.load(token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    # If no valid credentials, attempt to get from local env or Streamlit secrets
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Try to get credentials from the environment for local development
            creds_json = os.environ.get('GMAIL_CREDENTIALS')
            # Replace escaped quotes with real quotes
            creds_json = creds_json.replace('\\"', '"')
            print(creds_json)

            if not creds_json:
                # If not found locally, get credentials from Streamlit secrets (for deployment)
                creds_json = st.secrets.get('GMAIL_CREDENTIALS')
                # Replace escaped quotes with real quotes
                creds_json = creds_json.replace('\\"', '"')

            if creds_json:
                creds_info = json.loads(creds_json)
                # Use this info to create flow and obtain credentials
                flow = InstalledAppFlow.from_client_config(creds_info['installed'], SCOPES)
                # Use the console method for OAuth in a cloud environment
                creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            token.write(creds.to_json().encode())
    
    # If credentials are valid, build the Gmail API service
    if not creds:
        print("Authentication failed.")
        return None
    
    service = build('gmail', 'v1', credentials=creds)

    # Search query to find all emails received during a time
    # Format: after:2023/09/30 before:2023/11/01
    query = 'in:inbox'

    # Get the user's inbox and retrieve emails based on the query
    results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return None
    
    # Get the message ID
    message_id = messages[0]['id']

    # Use the message ID to get the email details
    message_data = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    # Extract information from the email headers
    headers = message_data['payload']['headers']
    subject = get_header(headers, 'Subject')
    sender = get_header(headers, 'From')
    recipient = get_header(headers, 'To')
    date = get_header(headers, 'Date')

    # Extract the email body
    email_body = get_message_body(message_data['payload'])

    # Check for attachments
    attachments = []
    if 'parts' in message_data['payload']:
        for part in message_data['payload']['parts']:
            if part.get('filename'):  # Attachment is present
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

                # Save the attachment
                attachment_file = save_attachment(part['filename'], file_data)
                attachments.append(attachment_file)


    # Decode the email body (Base64 encoded)
    if email_body:
        decoded_body = base64.urlsafe_b64decode(email_body).decode('utf-8')
    else:
        decoded_body = "(No body content)"

    # Output the email details
    print(f"From: {sender}")
    print(f"To: {recipient}")
    print(f"Date: {date}")
    print(f"Subject: {subject}")
    print(f"Body: {decoded_body}")
    if attachments:
        print("Attachments:", attachments)
    else:
        print("No attachments found.")
    print("\n" + "="*50 + "\n")  # Separator between emails
    output = {
        "From": sender,
        "To": recipient,
        "Date": date,
        "Subject": subject,
        "Body": decoded_body,
        "Attachments": attachments,
        "service": service,
    }
    return output

def get_header(headers, name):
    """Helper function to retrieve header values."""
    for header in headers:
        if header['name'] == name:
            return header['value']
    return None

def get_message_body(payload):
    """Helper function to extract the message body from the email payload."""
    if 'body' in payload and 'data' in payload['body']:
        return payload['body']['data']
    elif 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return part['body']['data']
    return ''

def save_attachment(filename, data):
    """Helper function to save the attachment to the local filesystem."""
    folder_path = 'files'
    
    # Create a folder for attachments if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the file in the 'attachments' folder
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(data)
    
    print(f"Attachment saved: {file_path}")
    return file_path


model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# JSON file path
json_file_path = "user_profile.json"

# Initialize or load the JSON file
def load_json():
    with open(json_file_path, 'r') as f:
        return json.load(f)

def create_draft(output, completed_file):
    """Create and send a draft with an attachment."""
    
    # Create the MIME message
    message = MIMEMultipart()
    message['to'] = output['From'] # Send it back to the original sender
    message['from'] = output['To']  # The authorized user (you)
    message['subject'] = f"Re: {output['Subject']}" # Reply to the original subject
    
    # Add email body (plain text)
    user_profile=load_json()
    response= model.generate_content(f"""From: {output['From']} Body:{output['Subject']} 
                                     This email contains a pdf that I filled with the appropriate info. 
                                     I want to answer in an email, with the completed file attached. 
                                     Please write only the body of my email, 
                                     starting by greeting the recipient using their name, 
                                     which you should infer from their email address: {output['From']}.
                                     Sign with my name: {user_profile["Name"]}.""")
    msg_text = MIMEText(response.text)
    message.attach(msg_text)
    
    # Attach the PDF file
    with open(completed_file, 'rb') as f:
        mime_base = MIMEBase('application', 'pdf')
        mime_base.set_payload(f.read())
        encoders.encode_base64(mime_base)  # Encode the file as Base64
    
    mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(completed_file)}"')
    message.attach(mime_base)
    
    # Convert the message to a raw string
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    # Create the draft with the encoded message
    create_message = {'message': {'raw': raw_message}}
    draft = output['service'].users().drafts().create(userId='me', body=create_message).execute()
    
    print(f"Draft created: {draft['id']}")