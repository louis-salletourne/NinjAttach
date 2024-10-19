import os
import base64

def create_draft(service, sender, attachment_file_path):
    """Create a draft with an attachment."""
    # Create the attachment
    with open(attachment_file_path, 'rb') as f:
        attachment_data = f.read()

    attachment_base64 = base64.urlsafe_b64encode(attachment_data).decode()

    # Create the body of the draft email
    subject = "Re: Your Recent Email"
    body = f"From: me\nTo: {sender}\nSubject: {subject}\n\nThank you for your email. Please find the attached document.\n\nBest regards,\nYour Name"  # Customize your message

    # Construct the draft message
    message = {
        'message': {
            'raw': base64.urlsafe_b64encode(body.encode()).decode(),
            'payload': {
                'headers': [
                    {'name': 'To', 'value': sender},
                    {'name': 'Subject', 'value': subject},
                    {'name': 'From', 'value': 'me'},
                ],
                'attachments': [
                    {
                        'filename': os.path.basename(attachment_file_path),
                        'mimeType': 'application/pdf',
                        'body': {
                            'data': attachment_base64
                        }
                    }
                ]
            }
        }
    }

    # Create the draft in the user's mailbox
    draft = service.users().drafts().create(userId='me', body=message).execute()
    print(f"Draft created with ID: {draft['id']}")
