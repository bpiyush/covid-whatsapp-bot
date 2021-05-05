"""Script that has functions to extract data from Google Sheet.
"""
from os.path import join
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

from utils.paths import REPO

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = join(REPO, 'data/keys.json')

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '17aaxSqNpN9Dnr1pSp-G5SCXOwttrbbh3u1N_NiPzRfk'

service = build('sheets', 'v4', credentials=credentials)


def get_gsheet(sheet_id=SAMPLE_SPREADSHEET_ID):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="common-resources-sheet").execute()
    values = result['values']

    header_row = values[0]
    cell_values = values[1:]
    df = pd.DataFrame(cell_values, columns=header_row)

    return df

if __name__ == '__main__':
    df = get_gsheet()
    import ipdb; ipdb.set_trace()
