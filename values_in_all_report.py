from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def full_values_report_sbor(need_date=None) -> list:
    # При изменении этих областей удалите файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1i8N8nYFk4dRuSuZRYl5brP-yhBwso_uVT_kroLY_-h4'
    SAMPLE_RANGE_NAME = 'Ответы на форму (1)!A2:J'

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('Таблица пуста.')
            return None
    except HttpError as err:
        print(f'full_values_report_sbor\n{err}')

    if need_date is not None:
        need_values = []
        for row in values:
            if row:
                if row[3] == need_date:
                    need_values.append(list(row))
        values_return = need_values
        return values_return
    else:
        return values


def full_values_report_auto(need_date=None) -> list:
    # При изменении этих областей удалите файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1Y96B1z1TO4MgfjCP4b8qjhxwUdShVSs85VBhIxW8EQg'
    SAMPLE_RANGE_NAME = 'Ежесменные отчёты П3!A2:V'

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

    except HttpError as err:
        print(err)

    if need_date is not None:
        need_values = []
        for row in values:
            if row:
                if row[3] == need_date:
                    need_values.append(list(row))
        values = need_values
        return values
    else:
        return values


def full_values_report_VRO(need_date=None) -> list:
    # При изменении этих областей удалите файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1bW4fyjOvUQtX2NkLN49LU_tNOHswjFmIOlGgwnvvR0I'
    SAMPLE_RANGE_NAME = 'Ответы на форму (4)!A2:H'

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('Таблица пуста.')
            return None
    except HttpError as err:
        print(err)
    if need_date != None:
        need_values = []
        for row in values:
            if row:
                if row[3] == need_date:
                    need_values.append(list(row))
        values = need_values
        return values
    else:
        return values


if __name__ == '__main__':

    # full_values_report_sbor()
    # full_values_report_auto()
    full_values_report_VRO()

    pass
