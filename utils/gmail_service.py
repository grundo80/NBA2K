import os
import base64
import json

from google.oauth2.credentials import Credentials
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
    Authenticate and return Gmail API service using tokens from token.json.
    If token.json does not exist or is invalid, print an error message.
    """
    creds = None
    print("Using client_id:", os.environ.get("GOOGLE_CLIENT_ID"))
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If creds don't exist or are invalid
    if not creds:
        print("No valid credentials found. Please authorise the app by visiting /login/google in the browser")
        return None
    
    # Refresh the token if it is expired and refresh_token is unavailable
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            #Update token.json with the new refreshed token
            with open("token.json", "w") as token_file:
                token_file.write(creds.to_json())
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            return None
        
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(user_id, recipient, subject, message_text):
    """
    Send an email using the Gmail API.
    """
    service = get_gmail_service()
    if not service:
        print("Gmail service not available. Please authorise the app first.")
        return None
    
    try:
        message = create_message(user_id, recipient, subject, message_text)
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {message["id"]}")
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
