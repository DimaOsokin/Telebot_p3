from __future__ import print_function

import math
from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import my_logers


async def quality_indicators() -> list:
    """
    Показатели качества каждого месяца за текущий год
    :return: list
    """
    # При изменении этих областей удалить файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1fOmQgL7uDLzmNQ6ePdpNn6BVNJ8jcacYeB_6OxErHuU'
    SAMPLE_RANGE_NAME = 'Выходной контроль качества!A2:N'

    # наполнение строками из excel таблицы
    values = []

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
        await my_logers.log_err(func=f"{__name__} quality_indicators", message={err})

    month_list = ['Zero', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    # числовое значение проверенной и дефектной продукции
    count_check_productions, count_defect_productions = 0, 0
    # текущий месяц int
    current_month_start = datetime.now().month
    # итоговый вывод включающий в себя все месяцы за год
    return_values = []

    for i in range(1, current_month_start + 1):
        current_month_iteration = i
        for x in values:
            try:
                # первый str элемент разбивается на 3 части что бы вытащить из него месяц
                values_full_date = x[0].split('.')
                # превращение значения месяца в int
                values_month = int(values_full_date[1])

                if current_month_iteration == values_month:
                    str_not_percent = x[-3].replace('%', '')
                    tmp_check_productions_in_paper = float(x[-5]) / 100 * float(str_not_percent)
                    count_check_productions += round(tmp_check_productions_in_paper, 2)
                    count_defect_productions += int(x[-1])

            except IndexError:  # пустая строка
                pass
            except Exception as err:
                await my_logers.log_err(func=f"{__name__} quality_indicators", message={err})
        # % выхода годной продукции
        percent_good_production = 100 - (count_defect_productions/count_check_productions * 100)
        return_values.append(f"Показатели за *{month_list[i]}*\n"
                             f"Количество проверенных изделий: *{count_check_productions:.0f}*\n"
                             f"Количество изделий с дефектом: *{count_defect_productions}*\n"
                             f"% выхода годной продукции *{percent_good_production:.2f}*\n\n")
        # обнуление числовых показателей
        count_check_productions, count_defect_productions = 0, 0

    return return_values


async def from_excel_table_quality(time_interval=None) -> list:
    # При изменении этих областей удалить файл token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Идентификатор и диапазон образца электронной таблицы.
    SAMPLE_SPREADSHEET_ID = '1fOmQgL7uDLzmNQ6ePdpNn6BVNJ8jcacYeB_6OxErHuU'
    SAMPLE_RANGE_NAME = 'Выходной контроль качества!A2:AC'

    # наполнение строками из excel таблицы
    values = []

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
        await my_logers.log_err(func=f"{__name__} from_excel_table_quality", message={err})

    # глобальная для этой функции переменная для return
    need_values, need_time = [], []

    if time_interval == 'last_week':
        # 7 итераций, для вычисления 7 дней предыдущей недели
        for x in range(7):
            local_day = datetime.today() - timedelta(days=x)
            data = datetime.strftime(local_day, "%d.%m.%y")
            need_time.append(data)
        # проверка по списку дат
        for specific_day in need_time:
            # проверить каждую дату на соответствие во всех строках
            for x in values:
                try:
                    # принудительное добавление ведущих нулей к месяцу и дате первых двух столбцах
                    # по причине различий в linux и windows
                    x[0] = datetime.strptime(x[0], "%d.%m.%y")
                    x[0] = datetime.strftime(x[0], "%d.%m.%y")
                    x[1] = datetime.strptime(x[1], "%d.%m.%y")
                    x[1] = datetime.strftime(x[1], "%d.%m.%y")

                    # в строке присутствует партия с дефектом
                    if x[13] != '0':
                        # проверить что столбец проведений инструктажа пуст (инструктажа проведено не было)
                        if (x[0] == specific_day) and (x[-4] == '-' or x[-4] == '' or x[-4] == ' '):
                            need_values.insert(0, x)
                except IndexError:
                    pass
                except ValueError:  # пустая строка
                    pass
                except Exception as err:
                    await my_logers.log_err(func=f"{__name__} from_excel_table_quality", message={err})
        return need_values

    elif time_interval == 'yesterday':
        local_day = datetime.today() - timedelta(days=1)
        specific_day = local_day.strftime("%d.%m.%y")

        for index, x in enumerate(values):
            try:
                # принудительное добавление ведущих нулей к месяцу и дате первых двух столбцах
                # по причине различий в linux и windows
                x[0] = datetime.strptime(x[0], "%d.%m.%y")
                x[0] = datetime.strftime(x[0], "%d.%m.%y")
                x[1] = datetime.strptime(x[1], "%d.%m.%y")
                x[1] = datetime.strftime(x[1], "%d.%m.%y")

                # в строке присутствует партия с дефектом
                if x[13] != '0':
                    # проверить что столбец проведений инструктажа пуст (инструктажа проведено не было)
                    if (x[0] == specific_day) and (x[-4] == '-' or x[-4] == '' or x[-4] == ' '):
                        need_values.insert(0, x)
            except IndexError:
                pass
            except ValueError:  # пустая строка
                pass
            except Exception as err:
                await my_logers.log_err(func=f"{__name__} from_excel_table_quality", message={err})
        return need_values

    elif time_interval == 'today':
        local_day = datetime.today()
        specific_day = datetime.strftime(local_day, "%d.%m.%y")
        for index, x in enumerate(values):
            try:
                # принудительное добавление ведущих нулей к месяцу и дате первых двух столбцах
                # по причине различий в linux и windows
                x[0] = datetime.strptime(x[0], "%d.%m.%y")
                x[0] = datetime.strftime(x[0], "%d.%m.%y")
                x[1] = datetime.strptime(x[1], "%d.%m.%y")
                x[1] = datetime.strftime(x[1], "%d.%m.%y")
                # в строке присутствует партия с дефектом
                if x[13] != '0':
                    # проверить что столбец проведений инструктажа пуст (инструктажа проведено не было)
                    if (x[0] == specific_day) and (x[-4] == '-' or x[-4] == '' or x[-4] == ' '):
                        need_values.insert(0, x)
            except IndexError:
                pass
            except ValueError:  # пустая строка
                pass
            except Exception as err:
                await my_logers.log_err(func=f"{__name__} from_excel_table_quality", message={err})
        return need_values


