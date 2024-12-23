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
email_client_id = os.environ.get("EMAIL_CLIENT_ID")

def get_gmail_service():
    """
    Authenticate and return Gmail API service using tokens from token.json.
    This assumes that token.json has already been created via an offline 
    authorization process (InstalledAppFlow) on another machine.
    """
    creds = None
    print("Using Gmail Project A client_id:", email_client_id)
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        print("No token.json found. Please place a valid token.json with gmail.send credentials.")
        return None
    
    # If creds don't exist or are invalid
    if not creds:
        print("Invalid credentials found in token.json. Please re-authorize offline and update token.json.")
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
        print("Gmail service not available. Check token.json and ensure valid credentials exist.")
        return None
    
    try:
        message = create_message(user_id, recipient, subject, message_text)
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {message['id']}")
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
