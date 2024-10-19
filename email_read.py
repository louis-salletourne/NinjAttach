import os.path
import json
import base64
import shutil
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from draft_writer import create_draft  # Importing the create_draft function


# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
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

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            token.write(creds.to_json().encode())
    
    # If credentials are valid, build the Gmail API service
    if creds:
        service = build('gmail', 'v1', credentials=creds)

        # Search query to find all emails received during a time
        # Format: after:2023/09/30 before:2023/11/01
        # query = 'after:2024/09/30 before:2024/11/01'

        # Get the user's inbox and retrieve emails based on the query
        results = service.users().messages().list(userId='me', q='', maxResults=1).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
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

                        # Copy the PDF to the completed_files folder
                        completed_file = copy_to_completed_files(attachment_file)

                        # Create draft reply with the updated PDF attached
                        create_draft(service, sender, subject, completed_file)


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
    folder_path = 'attachments'
    
    # Create a folder for attachments if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the file in the 'attachments' folder
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(data)
    
    print(f"Attachment saved: {file_path}")
    return file_path



def copy_to_completed_files(file_path):
    """Copy the PDF to the completed_files folder and rename it."""
    completed_folder = 'completed_files'
    if not os.path.exists(completed_folder):
        os.makedirs(completed_folder)

    filename = os.path.basename(file_path)
    new_filename = filename.replace(".pdf", "_completed.pdf")
    new_path = os.path.join(completed_folder, new_filename)

    shutil.copy(file_path, new_path)
    print(f"File copied to: {new_path}")
    return new_path


if __name__ == '__main__':
    main()