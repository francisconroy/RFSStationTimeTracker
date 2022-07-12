import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Jfo-YVt05Wy1beb5UrsWdKHm4qM9bBOCKvhBmIss8BA'
PERSONS_RANGE = 'persons!A2:B'
RECORDS_RANGE = 'records_mike!A2:L'

service = None


def setup_service():
    global service
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        service = build('sheets', 'v4', credentials=creds)

    except HttpError as err:
        print(err)


def get_employee_list():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=PERSONS_RANGE).execute()
    return result.get('values', [])


def lookup_name_from_id(id):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=PERSONS_RANGE).execute()
    valpairs = result.get('values', [])
    lookup = {k: v for k, v in valpairs}
    return lookup.get(id, "unregistered")


def log_check_in(person_id, time, date, reason):
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.
    value_range_body = {
        "values": [
            ["1", # Timestamp
             lookup_name_from_id(person_id), # Name
             "", # Blank
             "", # CheckIn/CheckOut
             "", # Date In
             "", # Time In
             "",  # Date Out
             "",  # Time Out
             "", # Reason - selection
             "", # Text reason
             "", # Email address
             person_id, # ID
             ]
        ]
    }

    request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RECORDS_RANGE,
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
