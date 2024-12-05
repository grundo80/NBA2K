import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
from flask import url_for

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """
    Authenticate and return Gmail API service.
    """
    creds = None
    print("Using client_id:", os.environ.get("GOOGLE_CLIENT_ID"))
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no valid credentials, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                    "redirect_uris": [os.environ.get("GOOGLE_REDIRECT_URI")],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }, SCOPES)
            creds = flow.run_local_server(port=5000)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(user_id, recipient, subject, message_text):
    """
    Send an email using the Gmail API.
    """
    try:
        service = get_gmail_service()
        message = create_message(user_id, recipient, subject, message_text)
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def create_message(sender, to, subject, message_text):
    """
    Create a message for email.
    """
    message = MIMEText(message_text)
    message["to"] = to
    message["from"]= sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def generate_confirmation_token(email):
    """
    Generating a confirmation token.
    """
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    return serializer.dumps(email, salt=os.environ.get("SECURITY_PASSWORD_SALT"))

def confirm_token(token, expiration=3600):
    """
    Confirming the token.
    """
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        email = serializer.loads(token, salt=os.environ.get("SECURITY_PASSWORD_SALT"), max_age=expiration)
    except:
        return False
    return email
