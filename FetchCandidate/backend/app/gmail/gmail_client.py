import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    token_file = os.getenv("GMAIL_TOKEN_FILE")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET_FILE")

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    service = build("gmail", "v1", credentials=creds)
    return service
