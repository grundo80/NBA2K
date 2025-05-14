"""
This is the config file containing all necessary information.
"""

from datetime import timedelta
import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

class Config:
    """
    This is the config class.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_key")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Login (Project B) environment variables
    LOGIN_CLIENT_ID = os.environ.get('LOGIN_CLIENT_ID')
    LOGIN_CLIENT_SECRET = os.environ.get('LOGIN_CLIENT_SECRET')
    LOGIN_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    LOGIN_REDIRECT_URI = os.environ.get('LOGIN_REDIRECT_URI')
    
    # Optionally, for Gmail sending (Project A) if you'd like to store them here:
    EMAIL_CLIENT_ID = os.environ.get('EMAIL_CLIENT_ID')
    EMAIL_CLIENT_SECRET = os.environ.get('EMAIL_CLIENT_SECRET')

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Email for sending messages
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Password for the email account
    MAIL_DEFAULT_RECIPIENT = os.environ.get("MAIL_DEFAULT_RECIPIENT")
