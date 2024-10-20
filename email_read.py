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


def create_draft(service, sender, subject, completed_file):
    """Create and send a draft with an attachment."""
    
    # Create the MIME message
    message = MIMEMultipart()
    message['to'] = sender  # Send it back to the original sender
    message['from'] = 'me'  # The authorized user (you)
    message['subject'] = f"Re: {subject}"  # Reply to the original subject
    
    # Add email body (plain text)
    msg_text = MIMEText("Please find the completed document attached.")
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
    draft = service.users().drafts().create(userId='me', body=create_message).execute()
    
    print(f"Draft created: {draft['id']}")

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
