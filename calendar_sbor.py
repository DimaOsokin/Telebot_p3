from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd


async def calendar_sbor_string(month=None, fio=None, year=None, weekends=False, next_month=False) -> str:
    """
    Возвращает рабочие дни сотрудника (день/ночь)
    Непрерывная последовательность смен занимает отдельную строку
    Если непрерывная последовательность равна 1 элементу, то так же занимает целую строку
    Если смен нет, возвращает пустую строку
    """
    values = ''
    # При изменении этих областей удалите файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1xhseVAqjqOHgSFUX8h-eR4zS588hro01yIsVma0pMQs'

    # в названии листа в конце может стоять пробел
    SAMPLE_RANGE_NAME_no_space = str(month) + f' {year} график 4/2!B1:AG'
    SAMPLE_RANGE_NAME_end_space = str(month) + f' {year} график 4/2 !B1:AG'

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
                                    range=SAMPLE_RANGE_NAME_no_space).execute()
        values = result.get('values', [])
    except HttpError:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME_end_space).execute()
        values = result.get('values', [])
    except Exception as e:
        print('calendar_sbor_string', e)

    # преобразование всех данных в датафрейм
    valuesDF = pd.DataFrame(values)
    if fio is not None:
        # извлечение строки по совпадению с передаваемой fio
        valuesDF = valuesDF.loc[valuesDF[0] == fio]
        # преобразование в список в списке
        values_tolist = valuesDF.values.tolist()
        # извление вложенного списка
        # нулевой индекс Имя с фамилией, затем последовательно дни месяца начиная с первого индекса
        # так же с пустыми значениями
        clear_list = values_tolist[0]
        # строка, в которую заполняются данные из списка
        full_mouth_work_list = ''
        full_mouth_weekends_list = ''
        # end_of_sequence необходимо для отслеживания пустых строк
        # end_of_sequence переключается в True после добавления значения в строку
        # end_of_sequence переключается в False сразу при обнаружении пустого значения
        # так же позволяет не добавлять новую пустую строку лишний раз
        end_of_sequence = False
        for index, value in enumerate(clear_list):
            # пропускает нулевой индекс (ФИ)
            if index != 0:

                if value == type(str):
                    value.strip()

                # проверка на пустую строку
                if not value:
                    import datetime
                    # сегодня в формате строки без нулей перед числом
                    today = datetime.datetime.now().strftime('%#d')
                    # добавляет в строку выходные дни только с завтрашнего дня
                    if next_month is False:
                        if int(index) > int(today):
                            full_mouth_weekends_list += str(index) + ' '
                    else:
                        full_mouth_weekends_list += str(index) + ' '
                    # перенос строки, если присутствуют предыдущие данные
                    if end_of_sequence is True:
                        full_mouth_work_list += '\n\n'
                        end_of_sequence = False


                elif value == 'д':
                    value = str(f"{index}Д  ")
                    full_mouth_work_list += value
                    # True, если след строка пустая, то сделает перенос строки
                    end_of_sequence = True

                elif value == 'н':
                    value = str(f"{index}Н  ")
                    full_mouth_work_list += value
                    end_of_sequence = True

                elif value == 'ОТПУСК' \
                        or value == 'ОТП' \
                        or value == 'БОЛЬНИЧНЫЙ':
                    pass

                else:
                    value = str(index) + f"{value} "
                    full_mouth_work_list += value
                    end_of_sequence = True

        # запрос на получение рабочих смен
        if weekends is True:
            return full_mouth_weekends_list
        # запрос на получение выходных дней
        else:
            return full_mouth_work_list

    else:
        return valuesDF









if __name__ == '__main__':
    pass
