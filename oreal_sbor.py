

async def start_inlain_sbor_lvl_5(message):
    from main import bot
    from aiogram import types
    kp = types.InlineKeyboardMarkup()

    # btn1 = types.InlineKeyboardButton(text='Настраиваемый диапазон', callback_data='start_inlain_sbor_btn1')
    btn2 = types.InlineKeyboardButton(text='Отчёты за вчера', callback_data='start_inlain_sbor_btn2')
    btn3 = types.InlineKeyboardButton(text='Отчёты за сегодня', callback_data='start_inlain_sbor_btn3')

    # kp.add(btn1)
    kp.add(btn2)
    kp.add(btn3)

    await bot.send_message(message.from_user.id, 'Отчёты сборочного участка', reply_markup=kp)


async def start_button_sbor_lvl_1(message):
    from main import bot
    from connect_to_DB_p3 import select_first_and_seconds_name
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    second_first_name = await select_first_and_seconds_name(message.from_user.id)
    button_start_lvl_1 = KeyboardButton('Меню')
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start_lvl_1)

    await bot.send_message(message.chat.id, f'{second_first_name} 👋', reply_markup=kb)


async def today_inlain_report_sbor(user_fio, report_today_date, report_yesterday_date):
    """
    Возвращает отчёт за: СЕГОДНЯ или ВЧЕРА
    Если отчёта нет, возвращает None
    :param user_fio: Фамилия Имя
    :param report_today_date: Сегодня
    :param report_yesterday_date: Вчера
    :return: str или None
    """
    from aiogram.utils.exceptions import MessageTextIsEmpty
    from connect_to_DB_p3 import check_report_yesterday_or_today_sbor
    try:  # сборочный участок СЕГОДНЯ
        today_report_func_sbor = await check_report_yesterday_or_today_sbor(report_today_date, user_fio)
        # при отсутствии отчёта - пустая строка, то принудительная ошибка MessageTextIsEmpty
        if today_report_func_sbor == '':
            raise MessageTextIsEmpty("Message text is empty")
        return today_report_func_sbor
    # за сегодня отчётов нет
    except MessageTextIsEmpty:
        yesterday_report_func_sbor = await check_report_yesterday_or_today_sbor(report_yesterday_date, user_fio)
        # при отсутствии отчёта - пустая строка, то return None
        if yesterday_report_func_sbor == '':
            return None
        return yesterday_report_func_sbor


# инлайн график
async def calendar_lvl_1(message):
    from main import bot
    from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP
    # LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}
    calendar, step = WMonthTelegramCalendar(locale='ru').build()
    await bot.send_message(message.chat.id,
                           f"Выберите {LSTEP[step]}:",
                           reply_markup=calendar)
