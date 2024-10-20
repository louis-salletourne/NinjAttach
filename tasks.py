from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
from datetime import datetime, timezone, timedelta
import time

# Define scopes for Gmail and Tasks
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/tasks'
]

# Authentication function
def authenticate():
    creds = None
    # Token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Function to get Gmail drafts
def get_gmail_drafts(service):
    results = service.users().drafts().list(userId='me').execute()
    drafts = results.get('drafts', [])
    return drafts

# Function to create Google Task
def create_google_task(service, task_title):
    task = {
        'title': task_title,
        'notes': 'This task was created from a Gmail draft.',
        'due': (datetime.now(timezone.utc) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }
    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f'Task created: {result.get("title")}, Task ID: {result.get("id")}')
    return result.get("id")

# Function to mark Google Task as completed
def mark_task_as_completed(service, task_id):
    task = service.tasks().get(tasklist='@default', task=task_id).execute()
    task['status'] = 'completed'
    updated_task = service.tasks().update(tasklist='@default', task=task_id, body=task).execute()
    print(f'Task marked as completed: {updated_task.get("title")}')

# Function to check if draft email was sent
def check_sent_email(service, draft_subject):
    results = service.users().messages().list(userId='me', labelIds=['SENT']).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        for header in headers:
            if header['name'].lower() == 'subject' and header['value'] == draft_subject:
                return True
    return False

def create_task():
    # Authenticate and create service for Gmail and Tasks
    creds = authenticate()

    gmail_service = build('gmail', 'v1', credentials=creds)
    tasks_service = build('tasks', 'v1', credentials=creds)

    # Get Gmail drafts
    drafts = get_gmail_drafts(gmail_service)
    if drafts:
        for draft in drafts:
            draft_id = draft['id']
            draft_message = gmail_service.users().drafts().get(userId='me', id=draft_id).execute()
            subject = None
            headers = draft_message['message']['payload']['headers']
            for header in headers:
                if header['name'].lower() == 'subject':
                    subject = header['value']
                    print("Subject :", subject)
                    break

            if subject:
                # Create Google Task with the draft subject
                task_id = create_google_task(tasks_service, subject)
                
                # Monitor the sent folder for the draft to be sent
                print(f'Waiting for the draft with subject "{subject}" to be sent...')
                while True:
                    sent = check_sent_email(gmail_service, subject)
                    if sent:
                        # Mark the task as completed once the email is sent
                        mark_task_as_completed(tasks_service, task_id)
                        break
                    time.sleep(10)  # Wait for 10 seconds before checking again
    else:
        print('No drafts found.')
