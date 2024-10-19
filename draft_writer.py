import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import shutil

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
