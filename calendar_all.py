import my_logers


async def calendar(message, user_lvl, now_month=False, next_month=False, recursion=False):
    """
    Отправляет пользователю тот график смен, где у него стоят смены
    Если его нет в графике, pass
    Если пустые смены, "График еще не готов"
    """

    from connect_to_DB_p3 import check_fio
    import calendar_sbor
    import calendar_auto
    import datetime

    # год формата '1970'
    now_year = int(datetime.datetime.now().strftime('%Y'))

    # int_to_list_month([[текущий месяц][след месяц]],[[текущий год][след год]]) след год меняется на +1, если тек месяц Декабрь
    int_to_list_month = await identify_month(now_year)
    next_year = int_to_list_month[1][0]
    # получить имя и фамилию
    fio = await check_fio(message.from_user.id)
# СБОРОЧНЫЙ УЧАСТОК
    if user_lvl == '1' or recursion is True:
        if now_month is True:
            try:  # этот месяц
                now_month_work_dates_string_sbor = await calendar_sbor.calendar_sbor_string(int_to_list_month[0][0], fio, now_year)
                return f"График на сборочном участке на {int_to_list_month[0][0]}:\n" + now_month_work_dates_string_sbor
            except Exception as err:
                return f"На сборочном участке на {int_to_list_month[0][0]} график еще не готов"

        elif next_month is True:
            try:  # следующий месяц
                next_month_work_dates_string_sbor = await calendar_sbor.calendar_sbor_string(int_to_list_month[0][1], fio, next_year)
                if next_month_work_dates_string_sbor != '':
                    return f"График на сборочном участке на {int_to_list_month[0][1]}:\n" + next_month_work_dates_string_sbor
                else:
                    return f'На {int_to_list_month[0][1]} график еще не готов'
            except:  # следующий месяц отсутствует
                return f'На сборочном участке на {int_to_list_month[0][1]} график еще не готов'

# АВТОМАТИЧЕСКИЙ УЧАСТОК
    elif user_lvl == '2' or recursion is True:
        if now_month is True:
            try:  # этот месяц
                now_month_work_dates_string_auto = await calendar_auto.calendar_auto_string(int_to_list_month[0][0], fio, now_year)
                return f"График на автоматическом участке на {int_to_list_month[0][0]}:\n" + now_month_work_dates_string_auto
            except:
                return f"На автоматическом участке на {int_to_list_month[0][0]} график еще не готов"
        elif next_month is True:
            try:  # следующий месяц
                next_month_work_dates_string_auto = await calendar_auto.calendar_auto_string(int_to_list_month[0][1], fio, next_year)
                if next_month_work_dates_string_auto != '':
                    return f"График на автоматическом участке на {int_to_list_month[0][1]}:\n" + next_month_work_dates_string_auto
                else:
                    return f'На автоматическом участке на {int_to_list_month[0][1]} график еще не готов'
            except:  # следующий месяц отсутствует
                return f'На автоматическом участке на {int_to_list_month[0][1]} график еще не готов'


async def identify_month(now_year):
    import datetime
    month_list = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    next_year = now_year

    # получить текущий месяц в int
    date_month_now = int(datetime.datetime.now().strftime('%m'))
    # если сейчас НЕ декабрь
    if date_month_now != 12:
        two_months = [date_month_now, date_month_now + 1]
    # если сейчас декабрь
    else:
        two_months = [12, 1]
        next_year = now_year + 1

    # месяцы в буквах
    now_month = month_list[two_months[0]]
    next_month = month_list[two_months[1]]
    two_months_list = [now_month, next_month]
    years_list = [now_year, next_year]
    return two_months_list, years_list


async def menu_inlain_lvl_1(message, user_lvl=None):
    from main import bot
    from aiogram import types
    kp = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text='Проверить отчёт 📝', callback_data='menu_inlain_lvl_1_check_report')
    btn2 = types.InlineKeyboardButton(text='Мой график 🗓', callback_data='menu_inlain_lvl_1_my_calendar')
    # btn3 = types.InlineKeyboardButton(text='Подработки 💰', callback_data='Инлайн меню уровень 1 подработки')

    kp.add(btn1)
    kp.add(btn2)
    # kp.add(btn3)

    await bot.send_message(message.from_user.id, 'Выберите, что вам необходимо:', reply_markup=kp)
