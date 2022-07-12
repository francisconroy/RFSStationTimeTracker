from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

currentflow = None


def accept_token(code):
    global currentflow
    currentflow.fetch_token(code=code)
    with open('token.json', 'w') as token:
        token.write(currentflow.credentials.to_json())


def do_login(redirect_uri):
    global currentflow
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    logged_in = True
    auth_url = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            currentflow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            currentflow.redirect_uri = redirect_uri
            auth_url = currentflow.authorization_url()[0]
            logged_in = False

    return logged_in, auth_url
