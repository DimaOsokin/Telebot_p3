from aiogram import Bot, types


async def start_inlain_only_auto(message):
    from main import bot

    kp = types.InlineKeyboardMarkup()
    # btn1 = types.InlineKeyboardButton(text='Настраиваемый диапазон', callback_data='start_inlain_only_auto_btn1')
    btn2 = types.InlineKeyboardButton(text='Отчёты за вчера', callback_data='start_inlain_only_auto_btn2')
    btn3 = types.InlineKeyboardButton(text='Отчёты за сегодня', callback_data='start_inlain_only_auto_btn3')

    # kp.add(btn1)
    kp.add(btn2)
    kp.add(btn3)

    await bot.send_message(message.from_user.id, 'Отчёты автоматического участка', reply_markup=kp)


async def start_inlain_only_VRO(message):
    from main import bot
    kp = types.InlineKeyboardMarkup()

    # btn1 = types.InlineKeyboardButton(text='Настраиваемый диапазон', callback_data='start_inlain_only_VRO_btn1')
    btn2 = types.InlineKeyboardButton(text='Отчёты за вчера', callback_data='start_inlain_only_VRO_btn2')
    btn3 = types.InlineKeyboardButton(text='Отчёты за сегодня', callback_data='start_inlain_only_VRO_btn3')
    # kp.add(btn1)
    kp.add(btn2)
    kp.add(btn3)
    await bot.send_message(message.from_user.id, 'Отчёты ВРО', reply_markup=kp)


async def start_button_auto_lvl_1(message):
    from main import bot
    from connect_to_DB_p3 import select_first_and_seconds_name
    from aiogram.types import ReplyKeyboardRemove, \
        ReplyKeyboardMarkup, KeyboardButton, \
        InlineKeyboardMarkup, InlineKeyboardButton

    second_first_name = select_first_and_seconds_name(message.from_user.id)
    button_start_lvl_1 = KeyboardButton('Меню')
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start_lvl_1)

    await bot.send_message(message.chat.id, f'{second_first_name} 👋', reply_markup=kb)


async def today_inlain_report_auto(user_fio, report_today_date, report_yesterday_date):
    """
        Возвращает отчёт за: СЕГОДНЯ или ВЧЕРА
        Если отчёта нет, возвращает None
        :param user_fio: Фамилия Имя
        :param report_today_date: Вчера
        :param report_yesterday_date: Сегодня
        :return: str или None
        """
    from aiogram.utils.exceptions import MessageTextIsEmpty
    from connect_to_DB_p3 import check_report_yesterday_or_today_auto
    try:  # автоматический участок СЕГОДНЯ
        today_report_func_auto = check_report_yesterday_or_today_auto(report_today_date, user_fio)
        # при отсутствии отчёта - пустая строка, то принудительная ошибка MessageTextIsEmpty
        if today_report_func_auto == '':
            raise MessageTextIsEmpty("Message text is empty")
        return today_report_func_auto
    # за сегодня отчётов нет
    except MessageTextIsEmpty:
        yesterday_report_func_auto = check_report_yesterday_or_today_auto(report_yesterday_date, user_fio)
        # при отсутствии отчёта - пустая строка, то return None
        if yesterday_report_func_auto == '':
            return None
        return yesterday_report_func_auto


async def today_inlain_report_VRO(user_fio, report_today_date, report_yesterday_date):
    """
        Возвращает отчёт за: СЕГОДНЯ или ВЧЕРА
        Если отчёта нет, возвращает None
        :param user_fio: Фамилия Имя
        :param report_today_date: Вчера
        :param report_yesterday_date: Сегодня
        :return: str или None
        """
    from aiogram.utils.exceptions import MessageTextIsEmpty
    from connect_to_DB_p3 import check_report_yesterday_or_today_VRO
    try:  # ВРО СЕГОДНЯ
        today_report_func_VRO = check_report_yesterday_or_today_VRO(report_today_date, user_fio)
        # при отсутствии отчёта - пустая строка, то принудительная ошибка MessageTextIsEmpty
        if today_report_func_VRO == '':
            raise MessageTextIsEmpty("Message text is empty")
        return today_report_func_VRO
    # за сегодня отчётов нет
    except MessageTextIsEmpty:
        yesterday_report_func_VRO = check_report_yesterday_or_today_VRO(report_yesterday_date, user_fio)
        # при отсутствии отчёта - пустая строка, то return None
        if yesterday_report_func_VRO == '':
            return None
        return yesterday_report_func_VRO