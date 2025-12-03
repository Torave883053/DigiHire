from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle, json

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def generate_token():
    creds = None
    if os.path.exists("token.json"):
        os.remove("token.json")

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES)
    creds = flow.run_local_server(port=8082)

    # Save token
    with open("token.json", "w") as token:
        token.write(creds.to_json())

if __name__ == "__main__":
    generate_token()
