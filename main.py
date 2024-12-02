import BOT_TOKEN
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageIsTooLong, MessageTextIsEmpty, BadRequest
from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP
import calendar_all
import calendar_sbor
import calendar_auto
import my_logers
import oreal_quality
import report_email
import update_quality_table
from connect_to_DB_p3 import *
from update_daily_report import *
import oreal_sbor
import oreal_auto


bot = Bot(token=BOT_TOKEN.token)
dp = Dispatcher(bot)

user_lvl = ''


@dp.callback_query_handler(WMonthTelegramCalendar.func())
async def inline_kb_answer_callback_handler_report_email(query: types.CallbackQuery):
    """
    Принимает данные callback от календаря
    :param query: types.CallbackQuery
    :return: None
    """
    await report_email.reaction_calendar_callback_report_email(query)


@dp.callback_query_handler(lambda call: True)
@dp.message_handler(commands=['start', 'help', 'all_personal'])
@dp.message_handler(content_types='text')
async def start(message):
    """
    Обработка всех инлайн кнопок (кроме календаря) и нажатий клавиатур
    :param message: call, commands, content_types
    :return: None
    """
    global user_lvl
    user_lvl = check_lvl_user(message.from_user.id)
    if type(message) == types.Message:
        # команды
        if message.text == '/start':
            await start_message(message)
            return
        elif message.text == '/help':
            await help_message(message)
            return
        elif message.text == '/all_personal':
            await see_all_employees(message)
            return
        else:
            # нажатие кнопок на клавиатуре
            await main_menu_5_lvl(message)
            return
    elif type(message) == types.CallbackQuery:
        # инлайн кнопки
        await start_call_back(message)
        return


async def start_call_back(call: types.CallbackQuery):
    from datetime import datetime
    if call.data == 'start_inlain_sbor_btn1':
        await bot.send_message(call.message.chat.id, 'В разработке 👩🏻‍💻')

    elif call.data == 'start_inlain_sbor_btn2' or call.data == 'start_inlain_sbor_btn3':
        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        report_data_list = ''

        # инлайн кнопка за вчера или сегодня
        if call.data == 'start_inlain_sbor_btn2':
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_sbor(need_day=yesterday)
        elif call.data == 'start_inlain_sbor_btn3':
            today = (datetime.now() - timedelta(days=0)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_sbor(need_day=today)

        try:
            local_values = ''
            # необходимо разбить список символами \n\n
            for x in report_data_list:
                local_values += "".join(f"{x}\n\n")
            await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')

        # если строка длинная
        except (MessageIsTooLong, BadRequest) as err:
            # ошибка MessageIsTooLong и BadRequest (text is too long)
            if type(err) == MessageIsTooLong or "Text is too long" in str(err):
                # сюда добавляется небольшая часть большого списка
                local_values = ''
                # итерация по элементам списка
                for x in report_data_list:
                    # измерить длину local_values после предполагаемого конкентирования
                    future_count_local_values = len(local_values) + len(x)
                    if future_count_local_values <= 3000:
                        local_values += "".join(f"{x}\n\n")
                    else:
                        await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')
                        local_values = ''
                        local_values = "".join(f"{x}\n\n")
                await bot.send_message(call.message.chat.id, f"{local_values}", parse_mode='Markdown')

            elif "Text must be non-empty" in str(err):
                await bot.send_message(call.message.chat.id, text='Нет отчетов за этот день')
            else:
                # другая ошибка BadRequest
                await bot.send_message(call.message.chat.id, f"Неизвестная ошибка BadRequest:\n{err}")

        # пустое сообщение
        except MessageTextIsEmpty:
            await bot.send_message(call.message.chat.id, text='Нет отчетов за выбранный день')
        # другие ошибки
        except Exception as err:
            print('start_inlain_sbor_btn2\n', err)


    if call.data == 'start_inlain_only_auto_btn1':
        await bot.send_message(call.message.chat.id, 'В разработке1 👩🏻‍💻')

    elif call.data == 'start_inlain_only_auto_btn2' or call.data == 'start_inlain_only_auto_btn3':
        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        report_data_list = ''
        # инлайн кнопка за вчера или сегодня
        if call.data == 'start_inlain_only_auto_btn2':
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_auto(need_day=yesterday)
        elif call.data == 'start_inlain_only_auto_btn3':
            today = (datetime.now() - timedelta(days=0)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_auto(need_day=today)

        try:
            local_values = ''
            # необходимо разбить список символами \n\n
            for x in report_data_list:
                local_values += "".join(f"{x}\n\n")
            await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')

        # если строка длинная
        except (MessageIsTooLong, BadRequest) as err:
            # ошибка MessageIsTooLong и BadRequest (text is too long)
            if type(err) == MessageIsTooLong or "Text is too long" in str(err):
                # сюда добавляется небольшая часть большого списка
                local_values = ''
                # итерация по элементам списка
                for x in report_data_list:
                    # измерить длину local_values после предполагаемого конкентирования
                    future_count_local_values = len(local_values) + len(x)
                    if future_count_local_values <= 3000:
                        local_values += "".join(f"{x}\n\n")
                    else:
                        await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')
                        local_values = ''
                        local_values = "".join(f"{x}\n\n")

                await bot.send_message(call.message.chat.id, f"{local_values}", parse_mode='Markdown')
            # пустое сообщение
            elif "Text must be non-empty" in str(err):
                await bot.send_message(call.message.chat.id, text='Нет отчетов за этот день')
            else:
                # другая ошибка BadRequest
                await bot.send_message(call.message.chat.id, f"Неизвестная ошибка BadRequest:\n{err}")

        # пустое сообщение
        except MessageTextIsEmpty:
            await bot.send_message(call.message.chat.id, text='Нет отчетов за вчерашний день')
        # другие ошибки
        except Exception as err:
            print('start_inlain_auto_btn2\n', err)


    if call.data == 'start_inlain_only_VRO_btn1':
        await bot.send_message(call.message.chat.id, 'В разработке4 👩🏻‍💻')
    elif call.data == 'start_inlain_only_VRO_btn2' or call.data == 'start_inlain_only_VRO_btn3':
        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        report_data_list = ''
        # инлайн кнопка за вчера или сегодня
        if call.data == 'start_inlain_only_VRO_btn2':
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_VRO(need_day=yesterday)
        elif call.data == 'start_inlain_only_VRO_btn3':
            today = (datetime.now() - timedelta(days=0)).strftime('%d.%m.%Y')
            report_data_list = check_report_yesterday_or_today_VRO(need_day=today)

        try:
            local_values = ''
            # необходимо разбить список символами \n\n
            for x in report_data_list:
                local_values += "".join(f"{x}\n\n")
            await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')

        # если строка длинная
        except (MessageIsTooLong, BadRequest) as err:
            # ошибка MessageIsTooLong и BadRequest (text is too long)
            if type(err) == MessageIsTooLong or "Text is too long" in str(err):
                # сюда добавляется небольшая часть большого списка
                local_values = ''
                # итерация по элементам списка
                for x in report_data_list:
                    # измерить длину local_values после предполагаемого конкентирования
                    future_count_local_values = len(local_values) + len(x)
                    if future_count_local_values <= 3000:
                        local_values += "".join(f"{x}\n\n")
                    else:
                        await bot.send_message(call.message.chat.id, local_values, parse_mode='Markdown')
                        local_values = ''
                        local_values = "".join(f"{x}\n\n")

                await bot.send_message(call.message.chat.id, f"{local_values}", parse_mode='Markdown')
            # пустое сообщение
            elif "Text must be non-empty" in str(err):
                await bot.send_message(call.message.chat.id, text='Нет отчетов за этот день')
            else:
                # другая ошибка BadRequest
                await bot.send_message(call.message.chat.id, f"Неизвестная ошибка BadRequest:\n{err}")

        # пустое сообщение
        except MessageTextIsEmpty:
            await bot.send_message(call.message.chat.id, text='Нет отчетов за вчерашний день')
        # другие ошибки
        except Exception as err:
            print('start_inlain_auto_btn2\n', err)


    if call.data == 'menu_inlain_lvl_1_check_report':
        # извлекает ИМЯ и ФАМИЛИЯ пользователя
        user_fio = await check_fio(call.from_user.id)
        # дата за СЕГОДНЯ и ВЧЕРА
        report_today_date = (datetime.now() - timedelta(days=0)).strftime('%d.%m.%Y')
        report_yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')

        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        # получить строки с отчётами (None, если пусто)
        get_today_report_inlain_btn_sbor = await oreal_sbor.today_inlain_report_sbor(user_fio, report_today_date,
                                                                                     report_yesterday_date)
        get_today_report_inlain_btn_auto = await oreal_auto.today_inlain_report_auto(user_fio, report_today_date,
                                                                                     report_yesterday_date)
        get_today_report_inlain_btn_VRO = await oreal_auto.today_inlain_report_VRO(user_fio, report_today_date,
                                                                                   report_yesterday_date)
        # все отчёты None
        if (get_today_report_inlain_btn_sbor is None) \
                and (get_today_report_inlain_btn_auto is None) \
                and (get_today_report_inlain_btn_VRO is None):
            await bot.send_message(call.message.chat.id,
                                   text=' За сегодняшний и вчерашний день ваших отчётов не найдено 🙅‍♂️')
        else:
            if get_today_report_inlain_btn_sbor:
                await bot.send_message(call.message.chat.id,
                                       text=get_today_report_inlain_btn_sbor, parse_mode='Markdown')
            if get_today_report_inlain_btn_auto:
                await bot.send_message(call.message.chat.id,
                                       text=get_today_report_inlain_btn_auto, parse_mode='Markdown')
            if get_today_report_inlain_btn_VRO:
                await bot.send_message(call.message.chat.id,
                                       text=get_today_report_inlain_btn_VRO, parse_mode='Markdown')

    elif call.data == 'menu_inlain_lvl_1_my_calendar':
        true_id_user = call.message.chat.id
        # по умолчанию в словаре call.message.from_user находится id бота, а не пользователя
        # копирует id чата в id пользователя (иначе calendar.check_fio не находит пользователя)
        # иначе в БД ищет пользователя по id чата, а не пользователя
        call.message['from']['id'] = true_id_user
        user_lvl = check_lvl_user(call.message.chat.id)
        await get_calendar(call.message, user_lvl)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif (call.data == 'Обновить отчёты за вчера') or (call.data == 'Обновить отчёты за сегодня'):
        if call.data == 'Обновить отчёты за вчера':
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await auto_insert_reports(message=call.message, day='yesterday')
        elif call.data == 'Обновить отчёты за сегодня':
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await auto_insert_reports(message=call.message, day='today')

    elif call.data == 'Вернуться в главное меню':
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            call.message['from']['id'] = call.message.chat.id
            await calendar_all.menu_inlain_lvl_1(call.message)

    elif call.data == 'Инлайн меню уровень 1 подработки':
        true_id_user = call.message.chat.id
        # по умолчанию в словаре call.message.from_user находится id бота, а не пользователя
        # копирует id чата в id пользователя (иначе calendar.check_fio не находит пользователя)
        # иначе в БД ищет пользователя по id чата, а не пользователя
        call.message['from']['id'] = true_id_user
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        kp = types.InlineKeyboardMarkup()

        btn1 = types.InlineKeyboardButton(
            text='Посмотреть мои выходные дни 📖', callback_data='Посмотреть мои выходные дни')
        btn2 = types.InlineKeyboardButton(
            text='Добавить подработку в ДЕНЬ 🌕', callback_data='Добавить подработку в ДЕНЬ')
        btn3 = types.InlineKeyboardButton(
            text='Добавить подработку в НОЧЬ 🌑', callback_data='Добавить подработку в НОЧЬ')
        btn4 = types.InlineKeyboardButton(
            text='Вернуться в главное меню ⬅', callback_data='Вернуться в главное меню')

        kp.add(btn1)
        kp.add(btn2)
        kp.add(btn3)
        kp.add(btn4)

        await bot.send_message(call.message.from_user.id, 'Подработки:', reply_markup=kp)

    elif call.data == 'Посмотреть мои выходные дни':
        true_id_user = call.message.chat.id
        # по умолчанию в словаре call.message.from_user находится id бота, а не пользователя
        # копирует id чата в id пользователя (иначе calendar.check_fio не находит пользователя)
        # иначе в БД ищет пользователя по id чата, а не пользователя
        call.message['from']['id'] = true_id_user

        user_lvl = check_lvl_user(call.message.from_user.id)
        fio = await check_fio(call.message.from_user.id)
        now_year = int(datetime.now().strftime('%Y'))
        # int_to_list_month([[текущий месяц][след месяц]],[[текущий год][след год]]) след год меняется на +1, если тек месяц Декабрь
        int_to_list_month = await calendar_all.identify_month(now_year)
        next_year = int_to_list_month[1][0]
# СБОРЩИК
        if user_lvl == '1':
            try:
                weekends = await calendar_sbor.calendar_sbor_string(
                    month=int_to_list_month[0][0],
                    fio=fio,
                    year=now_year,
                    weekends=True)
                await bot.send_message(call.message.from_user.id,
                                       text=f"Ваши следующие выходные дни на {int_to_list_month[0][0]}:\n{weekends}")
            except:
                pass
            try:
                weekends = await calendar_sbor.calendar_sbor_string(
                    month=int_to_list_month[0][1],
                    fio=fio,
                    year=now_year,
                    weekends=True,
                    next_month=True)
                await bot.send_message(call.message.from_user.id,
                                       text=f"Ваши следующие выходные дни на {int_to_list_month[0][1]}:\n{weekends}")
            except:
                pass
# ОПЕРАТОР
        else:
            try:
                weekends = await calendar_auto.calendar_auto_string(
                    month=int_to_list_month[0][0],
                    fio=fio,
                    year=now_year,
                    weekends=True)
                await bot.send_message(call.message.from_user.id,
                                       text=f"Ваши следующие выходные дни на {int_to_list_month[0][0]}:\n{weekends}")
            except:
                pass
            try:
                weekends = await calendar_auto.calendar_auto_string(
                    month=int_to_list_month[0][1],
                    fio=fio,
                    year=now_year,
                    weekends=True,
                    next_month=True)
                await bot.send_message(call.message.from_user.id,
                                       text=f"Ваши следующие выходные дни на {int_to_list_month[0][1]}:\n{weekends}")
            except:
                pass
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'Добавить подработку в ДЕНЬ':
        call.message['from']['id'] = call.message.chat.id
        # await bot.send_message(call.message.from_user.id, text=f"В разработке")

        import pandas as pd
        import datetime
        now_year = int(datetime.datetime.now().strftime('%Y'))
        # int_to_list_month([[текущий месяц][след месяц]],[[текущий год][след год]]) след год меняется на +1, если тек месяц Декабрь
        int_to_list_month = await calendar_all.identify_month(now_year)
        next_year = int_to_list_month[1][0]
        fio = await check_fio(call.message.from_user.id)
        text = await calendar_sbor.calendar_sbor_string(month=int_to_list_month[0][0], fio=None, year=now_year)
        # loc = pd.DataFrame(text[])
        # print(loc)
        # await bot.send_message(call.message.from_user.id, text='text')


        # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'Добавить подработку в НОЧЬ':
        call.message['from']['id'] = call.message.chat.id
        await bot.send_message(call.message.from_user.id, text=f"В разработке")

    elif call.data == 'Дефекты КК today' \
            or call.data == 'Дефекты КК yesterday' \
            or call.data == 'Дефекты КК last_week':
        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        call.message['from']['id'] = call.message.chat.id
        message_is_beginning = await bot.send_message(call.message.from_user.id, f"⌛ Произвожу поиск...")

        defect_list = []
        count_defect = 0

        if call.data == 'Дефекты КК today':
            defect_list, count_defect = await oreal_quality.get_defect('today')
        elif call.data == 'Дефекты КК yesterday':
            defect_list, count_defect = await oreal_quality.get_defect('yesterday')
        elif call.data == 'Дефекты КК last_week':
            defect_list, count_defect = await oreal_quality.get_defect('last_week')

        local_values = ''

        try:
            # если список пуст
            if not defect_list:
                await bot.send_message(call.message.from_user.id,
                                       f"Количество дефектов: *0*", parse_mode='Markdown')
            else:
                for x in defect_list:
                    local_values += "".join(map(str, x))
                await bot.send_message(call.message.from_user.id,
                                       f"{local_values}\n\n Количество дефектов: *{count_defect}*", parse_mode='Markdown')
        # если строка длинная
        except (MessageIsTooLong, BadRequest)as err:
            # ошибка MessageIsTooLong и BadRequest (text is too long)
            if type(err) == MessageIsTooLong or "Text is too long" in str(err):
                local_values = ''
                # сюда добавляется небольшая часть большого списка
                # итерация по элементам списка
                for x in defect_list:
                    # измерить длину local_values после предполагаемого конкентирования
                    future_count_local_values = len(local_values) + len(x)
                    if future_count_local_values <= 3000:
                        local_values += "".join(map(str, x))
                    else:
                        await bot.send_message(call.message.from_user.id, local_values, parse_mode='Markdown')
                        del local_values
                        local_values = "".join(map(str, x))

                await bot.send_message(call.message.from_user.id,
                                       f"{local_values}Количество дефектов: *{count_defect}*", parse_mode='Markdown')
            else:
                # другая ошибка BadRequest
                await bot.send_message(call.message.from_user.id, f"Неизвестная ошибка BadRequest:\n{err}")

        except MessageTextIsEmpty:
            await bot.send_message(call.message.from_user.id,
                                   'Бот не смог обратиться к таблице КК, '
                                   'вам придется просмотреть её на своём рабочем компьютере')
        except Exception as err:
            await bot.send_message(call.message.from_user.id, f"Неизвестная ошибка:\n{err}")
        # удалить сообщение message_is_beginning
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_is_beginning.message_id)


    elif call.data == 'Показатели качества за год':
        # удалить инлайн кнопки
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        call.message['from']['id'] = call.message.chat.id

        # для читабельного вывода сообщения
        send_message = ''
        # список по месяцам
        quality_indicators_list = await update_quality_table.quality_indicators()

        # добавление в строку
        for i in quality_indicators_list:
            send_message += "".join(i)

        await bot.send_message(call.message.from_user.id, send_message, parse_mode='Markdown')

    elif call.data == 'Отправить ссылку False':
        from report_email import calendar_message_cache
        user_id = call.message.chat.id
        kp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Отправить ссылку на почту ✅', callback_data='Отправить ссылку True')
        btn2 = types.InlineKeyboardButton(text='Начать формирование отчёта', callback_data='Начать формирование отчёта')
        btn3 = types.InlineKeyboardButton(text='Отмена', callback_data='Отмена формирования отчёта')

        kp.add(btn1)
        kp.add(btn2)
        kp.add(btn3)

        await call.message.edit_reply_markup(reply_markup=kp)
        calendar_message_cache[user_id].update({'send_to_email': True})

    elif call.data == 'Отправить ссылку True':
        from report_email import calendar_message_cache
        user_id = call.message.chat.id
        kp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Отправить ссылку на почту ❌', callback_data='Отправить ссылку False')
        btn2 = types.InlineKeyboardButton(text='Начать формирование отчёта', callback_data='Начать формирование отчёта')
        btn3 = types.InlineKeyboardButton(text='Отмена', callback_data='Отмена формирования отчёта')

        kp.add(btn1)
        kp.add(btn2)
        kp.add(btn3)

        await call.message.edit_reply_markup(reply_markup=kp)
        calendar_message_cache[user_id].update({'send_to_email': False})

    elif call.data == 'Отмена формирования отчёта':
        from report_email import calendar_message_cache
        user_id = call.message.chat.id
        try:
            await bot.delete_message(chat_id=call.message.chat.id,
                                     message_id=calendar_message_cache[user_id]['id_call_message_calendar_1'])
            await bot.delete_message(chat_id=call.message.chat.id,
                                     message_id=calendar_message_cache[user_id]['id_call_message_calendar_2'])
            await bot.delete_message(chat_id=call.message.chat.id,
                                     message_id=calendar_message_cache[user_id]['id_call_message_calendar_menu'])
            await bot.send_message(call.message.chat.id, f"Вы отменили составление электронного отчёта")
        except:
            pass
        report_email.calendar_message_cache.clear()
        report_email.calendar_data_cache.clear()

    elif call.data == 'Начать формирование отчёта':
        from report_email import calendar_message_cache
        user_id = call.message.chat.id
        if calendar_message_cache[user_id]['send_to_email']:
            await report_email.send_email_True(id_user=call.message.chat.id)

        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=calendar_message_cache[user_id]['id_call_message_calendar_1'])
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=calendar_message_cache[user_id]['id_call_message_calendar_2'])
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=calendar_message_cache[user_id]['id_call_message_calendar_menu'])

        date_range_list = await report_email.two_dates_to_list(dates=dict(report_email.calendar_data_cache[user_id]))
        await report_email.call_main_report_email(message=call.message, date_range_list=date_range_list)


async def get_calendar(message, user_lvl):
    search_is_beginning = await bot.send_message(message.chat.id, '📈 Строю график...')

    if user_lvl == '1':
        calendar_SU_now_month = await calendar_all.calendar(message, user_lvl='1', now_month=True)
        calendar_SU_next_month = await calendar_all.calendar(message, user_lvl='1', next_month=True)
        await bot.send_message(message.chat.id, str(f"{calendar_SU_now_month}\n\n{calendar_SU_next_month}"))
    elif (user_lvl == '2') or (user_lvl == '3') or (user_lvl == '4'):
        calendar_AU_now_month = await calendar_all.calendar(message, user_lvl='2', now_month=True)
        calendar_AU_next_month = await calendar_all.calendar(message, user_lvl='2', next_month=True)
        await bot.send_message(message.chat.id, str(f"{calendar_AU_now_month}\n\n{calendar_AU_next_month}"))

        calendar_SU_now_month = await calendar_all.calendar(message, user_lvl='1', now_month=True)
        calendar_SU_next_month = await calendar_all.calendar(message, user_lvl='1', next_month=True)
        if calendar_SU_now_month[0] == 'Н':
            pass
        else:
            await bot.send_message(message.chat.id, str(f"{calendar_SU_now_month}"))
        if calendar_SU_next_month[0] == 'Н':
            pass
        else:
            await bot.send_message(message.chat.id, str(f"{calendar_SU_next_month}"))

    elif user_lvl == '5':
        import lvl_5_names
        # преобразование в лист, так как в str читает только первый символ
        fio = await check_fio(message.from_user.id)
        fio_list = list(fio.split(' '))
        # сборочный участок
        if (fio_list[0] == lvl_5_names.name1[0] or
                fio_list[0] == lvl_5_names.name2[0] or
                fio_list[0] == lvl_5_names.name9[0] or
                fio_list[0] == lvl_5_names.name8[0]):
            calendar_SU_now_month = await calendar_all.calendar(message, user_lvl='1', now_month=True)
            calendar_SU_next_month = await calendar_all.calendar(message, user_lvl='1', next_month=True)
            await bot.send_message(message.chat.id, str(f"{calendar_SU_now_month}\n\n{calendar_SU_next_month}"))
        # автоматический участок
        elif (fio_list[0] == lvl_5_names.name4[0] or
              fio_list[0] == lvl_5_names.name5[0] or
              fio_list[0] == lvl_5_names.name6[0]):
            calendar_AU_now_month = await calendar_all.calendar(message, user_lvl='2', now_month=True)
            calendar_AU_next_month = await calendar_all.calendar(message, user_lvl='2', next_month=True)
            await bot.send_message(message.chat.id, str(f"{calendar_AU_now_month}\n\n{calendar_AU_next_month}"))
        # операционный менеджер и ст. сборщик
        elif fio_list[0] == lvl_5_names.name7[0] or fio_list[0] == lvl_5_names.name3[0]:
            await bot.send_message(message.chat.id, 'Ваш график 5/2')
    await bot.delete_message(chat_id=message.chat.id, message_id=search_is_beginning.message_id)


async def start_message(message):
    second_first_name = select_first_and_seconds_name(message.from_user.id)
    if second_first_name != 0:
        if user_lvl == '5':
            await bot.send_message(message.chat.id, f"👋 Здравствуйте, {second_first_name}!")

        if user_lvl =='5':
            await start_message_5(message, user_lvl)
        elif user_lvl =='4':
            await start_message_4(message, user_lvl)
        elif user_lvl =='3':
            await start_message_3(message, user_lvl)
        elif user_lvl =='2':
            await start_message_2(message, user_lvl)
        elif user_lvl =='1':
            await start_message_1(message, user_lvl)
    else:
        await bot.send_message(message.chat.id,
                               'Вас нет в списках сотрудников.'
                               '\nОбратитесь к старшему своего участка, для добавления вас в базу')


async def see_all_employees(message):
    second_first_name = select_first_and_seconds_name(message.from_user.id)
    if second_first_name != 0:
        if user_lvl == '5':
            await bot.send_message(message.chat.id, f"👋 Здравствуйте, {second_first_name}!")

        list_people = select_all_employee()
        peoples = ''
        for row_tup in list_people:
            row_str = '    '.join(map(str, row_tup))
            peoples += f"{row_str}\n"
        await bot.send_message(message.chat.id, peoples)
    else:
        await my_logers.log_err(
            func='see_all_employees',
            path_file='see_all_employees',
            message='Не руководитель пытается посмотреть список всех сотрудников\n'
                    f"Id пользователя: {message.from_user.id}\n"
                    f"Имя: {message.from_user.first_name}\n"
                    f"Фамилия: {message.from_user.last_name}\n"
                    f"Username: {message.from_user.username}\n"
                    )



async def help_message(message):
    await bot.send_message(message.chat.id, "Напишите /start для начала работы")


# кладовщики
async def start_message_4(message, user_lvl):
    await oreal_sbor.start_button_sbor_lvl_1(message)
    await calendar_all.menu_inlain_lvl_1(message, user_lvl)


# контролеры
async def start_message_3(message, user_lvl):
    await oreal_auto.start_button_auto_lvl_1(message)
    await calendar_all.menu_inlain_lvl_1(message)


# операторы
async def start_message_2(message, user_lvl):
    await oreal_auto.start_button_auto_lvl_1(message)
    await calendar_all.menu_inlain_lvl_1(message)


# сборщики
async def start_message_1(message, user_lvl):
    await oreal_sbor.start_button_sbor_lvl_1(message)
    await calendar_all.menu_inlain_lvl_1(message, user_lvl)

 
# руководство
async def start_message_5(message, user_lvl):
    kb = [
        [types.KeyboardButton(text="Сборочный участок 🔌")],
        [types.KeyboardButton(text="Автоматический участок ⚙️")],
        [types.KeyboardButton(text="Контроль качества 🕵️‍♀️️")],
        [types.KeyboardButton(text="Мой график 📅 и отчёт 📋")],
        [types.KeyboardButton(text="Список сотрудников Победит 3 👨‍👨‍👦‍👦")],
        [types.KeyboardButton(text="Обновить отчёты ✍️")],
        [types.KeyboardButton(text="Составить электронный отчёт")],
        # [types.KeyboardButton(text="Посчитать норму")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Что необходимо выбрать?", reply_markup=keyboard)


async def main_menu_5_lvl(message):
    if len(message.text) == 2:
        from rename_lvl import rename_full_lvls
        await rename_full_lvls(message)
    global user_lvl
    user_lvl = check_lvl_user(message.from_user.id)
    if user_lvl == '1':
        if message.text == 'Меню':
            await start_message_1(message, user_lvl)
        else:
            await bot.send_message(message.chat.id,
                                   f"Нет такой команды - '{message.text}'\nНапишите 👉 /start")
    elif user_lvl == '2':
        await start_message_2(message, user_lvl)
    elif user_lvl == '3':
        await start_message_3(message, user_lvl)
    elif user_lvl == '4':
        await start_message_4(message, user_lvl)
    elif user_lvl == '5':
        if message.text == 'Сборочный участок 🔌':
            await sbor_oreal_lvl_5(message)
        elif message.text == 'Автоматический участок ⚙️':
            await automatic_oreal(message)
        elif message.text == 'Отчёты автоматического участка':
            await oreal_auto.start_inlain_only_auto(message)
        elif message.text == 'Отчёты ВРО':
            await oreal_auto.start_inlain_only_VRO(message)
        elif message.text == 'Контроль качества 🕵️‍♀️️':
            await control_oreal(message)
        elif message.text == 'Вернуться в главное меню':
            await start_message(message)
        elif message.text == 'Список сотрудников Победит 3 👨‍👨‍👦‍👦':
            await see_all_employees(message)
        elif message.text == 'Обновить отчёты ✍️':
            from update_daily_report import auto_insert_reports
            await inlain_auto_insert_reports(message)
        elif message.text == 'Мой график 📅 и отчёт 📋':
            kp = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Проверить отчёт 📝',
                                              callback_data='menu_inlain_lvl_1_check_report')
            btn2 = types.InlineKeyboardButton(text='Мой график 🗓',
                                              callback_data='menu_inlain_lvl_1_my_calendar')

            kp.add(btn1)
            kp.add(btn2)

            await bot.send_message(message.from_user.id, 'Выберите, что вам необходимо:',
                                   reply_markup=kp)
        elif message.text == 'Составить электронный отчёт':
            await report_email.create_calendar_for_email_report(message=message)
        elif message.text == 'Посчитать норму':

            from cachetools import TTLCache
            colculation_norm_var = TTLCache(maxsize=50, ttl=300)

            async def calculation_norm():
                await bot.send_message(message.chat.id, colculation_norm_var)

        else:
            await bot.send_message(message.chat.id, f"Нет такой команды - '{message.text}'\nНажмите 👉 /start")

    else:
        await bot.send_message(message.chat.id, 'В доступе отказано')



async def inlain_auto_insert_reports(message):
    kp = types.InlineKeyboardMarkup()

    btn2 = types.InlineKeyboardButton(text='Вчера', callback_data='Обновить отчёты за вчера')
    btn3 = types.InlineKeyboardButton(text='Сегодня', callback_data='Обновить отчёты за сегодня')

    kp.add(btn2)
    kp.add(btn3)
    await bot.send_message(message.from_user.id, 'Обновление отчётов П3:', reply_markup=kp)


async def report_yesterday(message):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    yesterday_report = check_report_yesterday_or_today_sbor(yesterday)
    await bot.send_message(message.chat.id, yesterday_report, parse_mode='Markdown')


async def sbor_oreal_lvl_5(message):
    await oreal_sbor.start_inlain_sbor_lvl_5(message)


async def automatic_oreal(message):
    kb = [
        [types.KeyboardButton(text="Отчёты автоматического участка")],
        [types.KeyboardButton(text="Отчёты ВРО")],
        [types.KeyboardButton(text="Вернуться в главное меню")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Что необходимо выбрать?", reply_markup=keyboard)


async def control_oreal(message):
    kp = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text='За сегодня', callback_data='Дефекты КК today')
    btn2 = types.InlineKeyboardButton(text='За вчера', callback_data='Дефекты КК yesterday')
    btn3 = types.InlineKeyboardButton(text='За неделю', callback_data='Дефекты КК last_week')
    btn4 = types.InlineKeyboardButton(text='Показатели качества за год', callback_data='Показатели качества за год')
    # btn5 = types.InlineKeyboardButton(text='За всё время', callback_data='Дефекты КК all_time')

    kp.add(btn1)
    kp.add(btn2)
    kp.add(btn3)
    kp.add(btn4)
    # kp.add(btn5)

    await bot.send_message(message.from_user.id, 'Сборки *БЕЗ* внепланового инструктажа:',
                           reply_markup=kp,
                           parse_mode='Markdown')








































# message.from_user.id
# message.from_user.first_name
# message.from_user.last_name
# message.from_user.username


async def main():
    await dp.start_polling(bot)
    asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())

