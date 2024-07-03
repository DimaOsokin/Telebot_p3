from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from operator import itemgetter
from cachetools import TTLCache
import gspread
from gspread_formatting import *

import my_logers
from my_logers import *
from telegram_bot_calendar import WMonthTelegramCalendar
from main import bot, types


calendar_data_cache = TTLCache(maxsize=50, ttl=300)
calendar_message_cache = TTLCache(maxsize=100, ttl=300)


async def send_email_True(id_user) -> None:
    """
    Отправляет ссылку на таблицу "Отчет на почту" на электронную почту
    :param id_user:
    :return: None
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from connect_to_DB_p3 import check_fio
    import data_report_email

    server = None
    user_fio = await check_fio(id_user)


    link = "https://docs.google.com/spreadsheets/d/1EdCRFoJ83-ia4qGRPjtfmK6KlOuWEuO3EFqWuYhB4Ys/edit?usp=sharing"
    msg = MIMEText('<a href="{link}">Ссылка на таблицу</a>'.format(link=link), 'html', 'utf-8')
    msg['Subject'] = Header("T_bot | Ссылка на табл: Отчет на почту", 'utf-8')
    msg['From'] = data_report_email.login_email

    for fio in data_report_email.check_fio_for_send_email_address:
        if fio == user_fio:
            if fio == data_report_email.check_fio_for_send_email_address[0]:
                msg['To'] = data_report_email.email_address_K
            elif fio == data_report_email.check_fio_for_send_email_address[1]:
                msg['To'] = data_report_email.email_address_M
            elif fio == data_report_email.check_fio_for_send_email_address[2]:
                msg['To'] = data_report_email.email_address_O

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(data_report_email.login_email, data_report_email.pswd_email)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        await my_logers.log_info(
            func='send_email_True',
            path_file='report_email',
            message=f'Успех\n{msg}')
    except Exception as err:
        await my_logers.log_err(
            func='send_email_True',
            path_file='report_email',
            message=err)
    server.quit()


async def reaction_calendar_callback_report_email(query):
    """
    При нажатии на дату изменяет инлайн календарь на строку с указанием, что вы выбрали дату: {нажатая инлайн кнопка}
    :param query:
    :return:
    """
    user_id = query.from_user.id
    # получение данных из нажатой инлайн кнопки календаря
    call_back_date, key, step = WMonthTelegramCalendar(locale='ru').process(query.data)
    data_str_valid = ''
    # если нажата дата
    if call_back_date is not None:
        # Преобразование объекта datetime в строку в формате "DD.MM.YYYY"
        data_str_valid = call_back_date.strftime("%d.%m.%Y")
        # идентификатор юзера служит ключом к словарю
        if user_id not in calendar_data_cache:
            calendar_data_cache[user_id] = {'date_first': data_str_valid}
            message_id_call = await create_calendar_for_email_report(query.message)
        elif 'date_first' in calendar_data_cache[user_id] and 'date_second' not in calendar_data_cache[user_id]:
            calendar_data_cache[user_id]['date_second'] = data_str_valid
    # если нажата не дата
    if not call_back_date and key:
        await bot.edit_message_text(f"Выберите дату:",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    if call_back_date:
        if len(calendar_data_cache[user_id]) == 1:
            you_change = 'первую'
        elif len(calendar_data_cache[user_id]) == 2:
            you_change = 'вторую'
        await bot.edit_message_text(f"Вы выбрали {you_change} дату: *{data_str_valid}*",
                                    query.message.chat.id,
                                    query.message.message_id, parse_mode='Markdown')
    if user_id in calendar_data_cache:
        if len(calendar_data_cache[user_id]) == 2:
            kp = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Отправить ссылку на почту ❌', callback_data='Отправить ссылку False')
            btn2 = types.InlineKeyboardButton(text='Начать формирование отчёта', callback_data='Начать формирование отчёта')
            btn3 = types.InlineKeyboardButton(text='Отмена', callback_data='Отмена формирования отчёта')

            kp.add(btn1)
            kp.add(btn2)
            kp.add(btn3)

            id_call_message_calendar_menu = await bot.send_message(query.from_user.id, 'Заключительное меню:', reply_markup=kp)
            calendar_message_cache[user_id].update({'id_call_message_calendar_menu': id_call_message_calendar_menu.message_id})
            calendar_message_cache[user_id].update({'send_to_email': False})


async def create_calendar_for_email_report(message):
    """
    Создает инлайн календарь для выбора значений дат
    :param message:
    :return:
    """
    user_id = message['chat']['id']
    calendar, step = WMonthTelegramCalendar(locale='ru').build()
    message_id_call = await bot.send_message(message.chat.id, f"Введите дату:", reply_markup=calendar)
    if user_id not in calendar_message_cache:
        calendar_message_cache[user_id] = {'id_call_message_calendar_1': message_id_call.message_id}
    elif len(calendar_message_cache[user_id]) == 1:
        calendar_message_cache[user_id].update({'id_call_message_calendar_2': message_id_call.message_id})


async def call_main_report_email(message, date_range_list):
    try:
        ads
        await main_report_email(message=message, date_range_list=date_range_list)
        calendar_message_cache.clear()
        calendar_data_cache.clear()
    except Exception as err:
        calendar_message_cache.clear()
        calendar_data_cache.clear()
        if 'gspread.exceptions.APIError_429' in str(err):
            await log_err(func='main_report_email', path_file='report_email', message=err)
            await bot.send_message(message.chat.id, f"Лист с выбранным диапазоном уже существует "
                                                    f"{date_range_list[0]} - {date_range_list[-1]}\n"
                                                    "Удалите лист с данным значением, либо введите другой диапазон")
        elif 'gspread.exceptions.APIError_400' in str(err):
            await log_err(func='two_dates_to_str', path_file='report_email', message=err)
            await bot.send_message(message.chat.id, text=f"Превышено количество записей в минуту\n"
                                                         f"Таблица заполнена не полностью\n"
                                                         f"Удалите лист и попробуйте не менее чем, через минуту")
        else:
            await log_err(func='call_main_report_email', path_file='report_email', message=err)
            await bot.send_message(message.chat.id, f"Неизвестная ошибка\n"
                                                    f"{err}\nПопробуйте снова")

async def two_dates_to_list(dates=dict) -> list:
    """
    Принимает на вход словарь с вложенными датами выбранными на инлайн календаре
    Формирует список из всех дат, которые входят в этот список последовательно по возрастанию
    :param dates:
    :return: list
    """
    full_date = f"{dates['date_first']} - {dates['date_second']}"
    date_list = []
    try:
        # date превращается во вложенный список со всеми промежуточными датами
        start_date_str, end_date_str = full_date.split(" - ")
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
        # если указали вначале последнюю дату
        if end_date < start_date:
            tmp_date = start_date
            start_date = end_date
            end_date = tmp_date
            del tmp_date
            # вычисление временного диапазона дат
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            # запись диапазона в список
            date_list = [x.strftime("%d.%m.%Y") for x in date_range]

        # если значения дат одинаковы
        elif start_date_str == end_date_str:
            date_list = [start_date_str]
        else:
            # вычисление временного диапазона дат
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            # запись диапазона в список
            date_list = [x.strftime("%d.%m.%Y") for x in date_range]
    except Exception as err:
        await log_err(
            func='Формирование дат (other Except)',
            message=err,
            path_file='report_email')
        raise ValueError

    return date_list


async def main_report_email(message, date_range_list):
    main_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    main_SAMPLE_SPREADSHEET_ID = '1EdCRFoJ83-ia4qGRPjtfmK6KlOuWEuO3EFqWuYhB4Ys'  # Aleksey
    # main_SAMPLE_SPREADSHEET_ID = '1tu01FT1f6khAVmJXpSuVX4EuL8aHEWlEf3wkC9GREz4'  # Dima
    main_SAMPLE_RANGE_NAME = 'Образец!A1:G'
    worksheet = None
    full_date_str = ''
    creds = Credentials.from_service_account_file("credentials_report_email.json", scopes=main_SCOPES)
    client = gspread.authorize(creds)
    workbook = client.open_by_key(main_SAMPLE_SPREADSHEET_ID)
    title_table = [
        "Оборудование / Сборочный участок",
        "Выполненная операция",
        "Название изделий",
        "Количество годных изделий",
        "Количество задержанных изделий",
        "Сколько затрачено времени? (часов\минут)"]

    try:
        # если значения дат одинаковы
        if len(date_range_list) == 1:
            full_date_str = date_range_list[0]
        else:
            full_date_str = f"{date_range_list[0]} - {date_range_list[-1]}"
        # создание листа в google sheet
        worksheet = workbook.add_worksheet(title=f"{full_date_str} t_bot", rows=1000, cols=6)
        await bot.send_message(message.chat.id,
                               f"Я создал лист с названием\n*{full_date_str} t_bot*",
                               parse_mode='Markdown')
    # ошибки вызванные с API например данный лист уже создан
    except gspread.exceptions.APIError as err:
        # лист уже создан
        if 'already exists. Please enter another name' in str(err):
            raise Exception('gspread.exceptions.APIError_429')
        elif 'Quota exceeded for quota metric' in str(err):
            raise Exception('gspread.exceptions.APIError_400')
    # все остальные ошибки
    except Exception as err:
        await log_err(
            func='report_email_AUTO_values (workbook.add_worksheet)',
            message=err,
            path_file='report_email')
        raise Exception(err)
    worksheet.clear()

    # визуальное редактирование листа
    cell_format = {
        "backgroundColor": {
            "red": 55.0,
            "green": 55.0,
            "blue": 55.0
        },
        "textFormat": {
            "foregroundColor": {
                "red": 0.0,
                "green": 0.0,
                "blue": 0.0
            },
            "fontSize": 12,
            "bold": True
        }
    }
    cell_format_line = {"borders": {
        "bottom": {
            "style": "SOLID",
            "width": 1,
            "color": {
                "red": 0.0,
                "green": 0.0,
                "blue": 0.0
            }}}}
    # Горизонтальное выравнивание
    horizontal_alignment = {
        "A": "LEFT",
        "B": "LEFT",
        "C": "LEFT",
        "D": "RIGHT",
        "E": "RIGHT",
        "F": "RIGHT"
    }
    # Перенос текста
    wrap_strategy = {
        "B": "WRAP"
    }
    # Формат ко всем ячейкам
    worksheet.format("A1:F3", cell_format)

    # Горизонтальное выравнивание
    for col in ["A", "B", "C", "D", "E", "F"]:
        worksheet.format(f"{col}4:{col}", {"horizontalAlignment": horizontal_alignment[col]})

    # Перенос текста
    for col, strategy in wrap_strategy.items():
        worksheet.format(f"{col}1:{col}3", {"wrapStrategy": strategy})

    # установить ширину столбцов
    set_column_width(worksheet, 'A:F', 330)
    set_column_width(worksheet, 'F', 355)
    # заполнение первых строк
    worksheet.update([["Дата выполнения работ", f"{full_date_str}"]], 'A1:B1')
    worksheet.update([[
        title_table[0],
        title_table[1],
        title_table[2],
        title_table[3],
        title_table[4],
        title_table[5]]], 'A3:F3')
    

    # получает значения с отчётов
    automatic_dict = await report_email_AUTO_values(date_range_list)
    sbor_and_UC_dict = await report_email_SBOR_and_UniCrimp_values(date_range_list)
    await bot.send_message(message.chat.id, f"Приступаю к формированию листа, это займёт около минуты")

    # изменяющийся номер строки
    count_str = 4
    # цикл по вложенному словарю
    for name_dict in automatic_dict:
        try:
            # начертить линию перед следующей автоматической линией
            worksheet.format(f"A{count_str-1}:F{count_str-1}", cell_format_line)
            # заполнение первого столбца с названием оборудования
            worksheet.update_cell(count_str, 1, value=name_dict)
            operation_value_automatic_line = automatic_dict[name_dict]['Выполненная операция']
            name_cable_Zeta_automatic_line = automatic_dict[name_dict]['Название изделий']
            count_good_Zeta_automatic_line = automatic_dict[name_dict]['Количество годных изделий']
            spend_time_Zeta_automatic_line = automatic_dict[name_dict]['Сколько затрачено времени? (часов\минут)']

            completed_operation = []
            name_cable = []
            count_good = []
            not_good = []
            spend_time = []


            for index, x in enumerate(range(0, len(operation_value_automatic_line))):
                completed_operation.append([operation_value_automatic_line[x]])
                name_cable.append([name_cable_Zeta_automatic_line[x]])
                count_good.append([count_good_Zeta_automatic_line[x]])
                not_good.append([0])
                spend_time.append([spend_time_Zeta_automatic_line[x]])
            # пакетное добавление данных
            worksheet.update(completed_operation, f"B{count_str}")
            worksheet.update(name_cable, f"C{count_str}")
            worksheet.update(count_good, f"D{count_str}")
            worksheet.update(not_good, f"E{count_str}")
            worksheet.update(spend_time, f"F{count_str}")
            # номер последней добавленной строки + 1 для визуального разделения
            count_str += len(not_good) + 1

        except gspread.exceptions.APIError as err:
            if 'Quota exceeded for quota metric' in str(err):
                raise Exception('gspread.exceptions.APIError_400')
        except Exception as err:
            await log_err(func='log_err (for automatic_dict)', message=err, path_file='report_email')

    # цикл по вложенному словарю
    for name_dict in sbor_and_UC_dict:
        try:
            # начертить линию перед следующей операцией
            worksheet.format(f"A{count_str - 1}:F{count_str - 1}", cell_format_line)
            # заполнение первого столбца с названием изделия
            worksheet.update_cell(count_str, 1, value=name_dict)
            operation_value_SBOR_report = sbor_and_UC_dict[name_dict]['Выполненная операция']
            name_cable_SBOR_report = sbor_and_UC_dict[name_dict]['Название изделий']
            count_good_SBOR_report = sbor_and_UC_dict[name_dict]['Количество годных изделий']
            spend_time_SBOR_report = sbor_and_UC_dict[name_dict]['Сколько затрачено времени? (часов\минут)']

            completed_operation = []
            name_cable = []
            count_good = []
            not_good = []
            spend_time = []

            for index, x in enumerate(range(0, len(operation_value_SBOR_report))):
                completed_operation.append([operation_value_SBOR_report[x]])
                name_cable.append([name_cable_SBOR_report[x]])
                count_good.append([count_good_SBOR_report[x]])
                not_good.append([0])
                spend_time.append([spend_time_SBOR_report[x]])

            worksheet.update(completed_operation, f"B{count_str}")
            worksheet.update(name_cable, f"C{count_str}")
            worksheet.update(count_good, f"D{count_str}")
            worksheet.update(not_good, f"E{count_str}")
            worksheet.update(spend_time, f"F{count_str}")
            # номер последней добавленной строки + 1 для визуального разделения
            count_str += len(not_good) + 1
        except gspread.exceptions.APIError as err:
            if 'Quota exceeded for quota metric' in str(err):
                raise Exception('gspread.exceptions.APIError_400')
        except Exception as err:
            await log_err(func='log_err (for automatic_dict)', message=err, path_file='report_email')

    await bot.send_message(message.chat.id, f"Готово")

async def report_email_AUTO_values(date=None) -> dict:
    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    auto_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    auto_SAMPLE_SPREADSHEET_ID = '1Y96B1z1TO4MgfjCP4b8qjhxwUdShVSs85VBhIxW8EQg'
    auto_SAMPLE_RANGE_NAME = 'Ежесменные отчёты П3!D2:N'

    values = []

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', auto_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', auto_SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=auto_SAMPLE_SPREADSHEET_ID,
                                    range=auto_SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
    except HttpError as err:
        await log_info(func="report_email_auto_values", path_file='report_email', message=f"{err}")

    # сортировать список "values" по "Название изделий StarLine"
    values.sort(key=itemgetter(5))

    automatic_dict = {
        'Komax Zeta 633/651 (№457)': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        },
        'Komax Zeta 633/651 (№458)': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        },
        'Multi Strip 9480M': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        },
        'Komax Alpha 488S': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        },
        'Crimp Center 36S': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        }
    }

    for row in values:
        for colum in row:
            if colum in date:
                try:
                    if row[1] in automatic_dict:
                        automatic_dict[row[1]]['Выполненная операция'].append(row[2])
                        automatic_dict[row[1]]['Название изделий'].append(row[5])
                        automatic_dict[row[1]]['Количество годных изделий'].append(row[7])
                        automatic_dict[row[1]]['Сколько затрачено времени? (часов\минут)'].append(row[10])

                except Exception as err:
                    await log_err(func='report_email_AUTO_values', message=err, path_file='report_email')
    del values

    return automatic_dict


async def report_email_SBOR_and_UniCrimp_values(date=None) -> dict:
    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    sbor_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    sbor_SAMPLE_SPREADSHEET_ID = '1i8N8nYFk4dRuSuZRYl5brP-yhBwso_uVT_kroLY_-h4'
    sbor_SAMPLE_RANGE_NAME = 'Ответы на форму (1)!D2:J'

    values = []

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', sbor_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', sbor_SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sbor_SAMPLE_SPREADSHEET_ID,
                                    range=sbor_SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
    except HttpError as err:
        await log_info(
            func="report_email_SBOR_and_UniCrimp_values",
            path_file='report_email',
            message=err)

    # сортировать список "values" по "Наименование изделия"
    values.sort(key=itemgetter(1))

    sbor_dict = {
        'Обжатие проводов на UniCrimp 100': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        },
        'Сборочный участок': {
            'Выполненная операция': [],
            'Название изделий': [],
            'Количество годных изделий': [],
            'Количество задержанных изделий': [],
            'Сколько затрачено времени? (часов\минут)': []
        }
    }
    for index, row in enumerate(values):
        for colum in row:
            if colum in date:
                try:
                    # строка "Выполненные операции" не пустая
                    if row[5] != '':
                        if row[2] == "Обжатие проводов на UniCrimp 100":
                            sbor_dict['Обжатие проводов на UniCrimp 100']['Выполненная операция'].append(row[2])
                            sbor_dict['Обжатие проводов на UniCrimp 100']['Название изделий'].append(row[1])
                            sbor_dict['Обжатие проводов на UniCrimp 100']['Количество годных изделий'].append(row[5])
                            sbor_dict['Обжатие проводов на UniCrimp 100'][
                                'Сколько затрачено времени? (часов\минут)'].append(row[6])
                        # всё кроме UniCrimp 100
                        else:
                            # вложенный список "Название изделий" не пустой
                            if len(sbor_dict['Сборочный участок']['Название изделий']) != 0:
                                # присваивается название иделия для дальнейшего сравнения
                                past_elem_name_cable_SBOR = list(sbor_dict['Сборочный участок']['Название изделий'])[-1]
                            else:
                                # если элементов нет
                                past_elem_name_cable_SBOR = ''
                            # сравнивается текущее "Название изделий" с past_elem_name_cable_SBOR
                            if values[index][1] != past_elem_name_cable_SBOR:
                                sbor_dict['Сборочный участок']['Выполненная операция'].append(
                                    "Сборка кабельных изделий")
                            else:
                                # если значение values[index][1] == past_elem_name_cable_SBOR, то пустая строка
                                sbor_dict['Сборочный участок']['Выполненная операция'].append(" ")
                            sbor_dict['Сборочный участок']['Название изделий'].append(row[1])
                            sbor_dict['Сборочный участок']['Количество годных изделий'].append(row[5])
                            sbor_dict['Сборочный участок'][
                                'Сколько затрачено времени? (часов\минут)'].append(row[6])
                except Exception as err:
                    await log_err(
                        func='report_email_SBOR_and_UniCrimp_values',
                        message=err,
                        path_file='report_email')
    del values
    return sbor_dict


































if __name__ == '__main__':
    pass
