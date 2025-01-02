from mysql.connector import connect
from datetime import date
import my_logers
# from update_daily_report import *


async def select_all_employee():
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                sql_command = "SELECT `id_wt`, `id_fio` FROM `id` ORDER BY `id_fio` ASC"
                cursor.execute(sql_command)
                result = cursor.fetchall()
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} select_all_employee", message=err)

    return result


async def select_first_and_seconds_name(id_tg):
    """
    Получает Имя Фамилию
    Если в базе нет, то int(0)
    """
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                sql_command = "SELECT id_fio FROM id WHERE id_tg LIKE '%s'" % id_tg
                cursor.execute(sql_command)
                result_full_fio = cursor.fetchone()
                result_split = result_full_fio[0].split(' ')
                result = result_split[1] + ' ' + result_split[2]

    except Exception as err:
        await my_logers.log_err(func=f"{__name__} select_first_and_seconds_name", message=err)
        return 0

    return result


async def check_lvl_user(id_tg) -> int:
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                sql_command = """SELECT lvl FROM `id` WHERE id_tg LIKE '%s'""" % id_tg
                cursor.execute(sql_command)
                result_fetchone = cursor.fetchone()
                result = result_fetchone[0]
                return result
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} check_lvl_user", message=err)
        return 0


async def check_fio(id_tg) -> str:
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                sql_command = """SELECT id_fio FROM `id` WHERE id_tg LIKE '%s'""" % id_tg
                cursor.execute(sql_command)
                result_fetchone_full_str = cursor.fetchone()
                result_full_str = result_fetchone_full_str[0].split(' ')
                result = str(result_full_str[0]) + ' ' + str(result_full_str[1])
                return result
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} check_fio", message=err)


async def check_report_yesterday_or_today_sbor(need_day, user_fio=None):
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                if user_fio is not None:
                    cursor.execute("SELECT * FROM `Daily_report_sbor` where `Дата выполнения работ` = '%s' AND `Сотрудник` = '%s'" % (need_day, user_fio))
                else:
                    cursor.execute("SELECT * FROM `Daily_report_sbor` where `Дата выполнения работ` = '%s' ORDER BY `Сотрудник` ASC" % need_day)
                result_all = cursor.fetchall()
                result = ''
                for i in result_all:
                    # [0]Отметка времени    [1]Смена    [2]Сотрудник    [3]Дата выполнения работ
                    # [4]Наименование кабельной сборки  [5]Выполненные операции  [6]Номер задачи
                    # [7]Тип задачи [8]Количество изготовленных изделий     [9]Затраченное время
                    # Все строки НЕ пустые

                    if i[3] != '':
                        result += f"*Дата:* {i[3]} {i[1]}"
                    if i[2] != '':
                        result += f"\nСотрудник: {i[2]}"
                    if i[4] != '':
                        result += f"\n*Изделие:* {i[4]}"
                    if i[5] != '':
                        result += f"\n*Операция:* {i[5]}"
                    if i[6] != '' or i[7] != '':  # Номер задачи, Тип задачи

                        if i[7] != '' and i[6] != '':  # если оба элемента не пустые
                            result += f"\nЗадача {i[7]}-{i[6]}"
                        elif i[7] != '':  # если номер пустой
                            result += f"\nТип задачи - {i[7]}"
                        elif i[6] != '':  # если тип пустой
                            result += f"\nНомер задачи - {i[7]}"

                    if i[8] != '':
                        result += f"\n*Количество:* {i[8]}"
                    if i[9] != '':
                        result += f"\nЗатраченное время: {i[9]}"

                    result += '\n\n'
    except IndexError:
        pass
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} check_report_yesterday_or_today_sbor", message=err)

    # вернет строку
    if user_fio is not None:
        return result
    # список строк
    else:
        result_list = result.split("\n\n")
        return result_list


async def check_report_yesterday_or_today_auto(need_day, user_fio=None):
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                if user_fio is not None:
                    cursor.execute("SELECT * FROM `Daily_report_auto` where `Дата выполнения работ` = '%s' AND `Сотрудник` = '%s'" % (need_day, user_fio))
                else:
                    cursor.execute("SELECT * FROM `Daily_report_auto` where `Дата выполнения работ` = '%s' ORDER BY `Сотрудник` ASC" % need_day)
                result_all = cursor.fetchall()
                result = ''
                for i in result_all:
                    if i[3] != '':  # Дата выполнения работ
                        result += f"*Дата:* {i[3]}"
                    if i[1] != '':  # Смена
                        result += ' ' + f" {i[1]}"
                    if i[2] != '':  # Сотрудник
                        result += f"\nСотрудник: {i[2]}"
                    if i[4] != '':  # Оборудование
                        result += f"\n*Оборудование:* {i[4]}"
                    if i[8] == '' and i[9] != '':  # если Название изделий StarLine пустое, и не пустое Изделия контрактного производства
                        result += f"\n*Контрактное изделие:* {i[9]}"
                    if i[5] != '':  # Выполненная операция
                        result += f"\n*Операция:* {i[5]}"
                    if i[6] != '' or i[7] != '':  # Тип задачи, Номер задачи

                        if i[6] != '' and i[7] != '':  # если оба элемента не пустые
                            result += f"\nЗадача {i[7]}-{i[6]}"
                        elif i[6] != '':  # если Номер пустой
                            result += f"\nТип задачи - {i[7]}"
                        elif i[7] != '':  # если Тип пустой
                            result += f"\nНомер задачи - {i[7]}"

                    if i[10] != '':  # Количество
                        result += f"\n*Количество:* {i[10]}"
                    if i[13] != '':  # Затраченное время
                        result += f"\nЗатраченное время: {i[13]}"

                    result += '\n\n'

    except IndexError:
        pass
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} check_report_yesterday_or_today_auto", message=err)

    # вернет строку
    if user_fio is not None:
        return result
    # список строк
    else:
        result_list = result.split("\n\n")
        return result_list


async def check_report_yesterday_or_today_VRO(need_day, user_fio=None):
    try:
        import connection_data
        with connect(
                host=connection_data.host,
                user=connection_data.user,
                passwd=connection_data.passwd,
                database=connection_data.database) as conn:
            with conn.cursor() as cursor:
                if user_fio is not None:
                    cursor.execute("SELECT * FROM `Daily_report_VRO` where `Дата выполнения работ` = '%s' AND `Сотрудник` = '%s'" % (need_day, user_fio))
                else:
                    cursor.execute("SELECT * FROM `Daily_report_VRO` where `Дата выполнения работ` = '%s' ORDER BY `Сотрудник` ASC" % need_day)
                result_all = cursor.fetchall()
                result = ''
                for i in result_all:
                    if i[3] != '':  # Дата выполнения работ
                        result += f"*Дата:* {i[3]}"
                    if i[1] != '':  # Смена
                        result += ' ' + f" {i[1]}"
                    if i[2] != '':  # Сотрудник
                        result += f"\nСотрудник: {i[2]}"
                    if i[4] != '':  # Оборудование
                        result += f"\n{i[4]}"
                    if i[5] != '':  # Время работы
                        result += f"\n*Затраченное время:* {i[5]}"
                    if i[6] != '':  # Комментарий
                        result += f"\nКомментарий: {i[6]}"
                    if i[7] != '':  # Статус
                        result += f"\n_Статус:_ {i[7]}"
                    result += '\n\n'
    except IndexError:
        pass
    except Exception as err:
        await my_logers.log_err(func=f"{__name__} check_report_yesterday_or_today_VRO", message=err)
    # вернет строку
    if user_fio is not None:
        return result
    # список строк
    else:
        result_list = result.split("\n\n")
        return result_list


async def check_in_DB_last_day_sbor() -> str:
    """
    Проверяет последний день в БД
    """
    # импорт данных для соединения с БД
    import connection_data
    # подключение к БД
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = """
            SELECT `Дата выполнения работ` 
            FROM Daily_report_sbor 
            ORDER BY 'Дата выполнения работ' DESC"""
            cursor.execute(sql_command)
            # получаем последний день в БД
            # записываем в переменную последний день в БД
            last_day = cursor.fetchall()[-1][0]
    return last_day


async def check_report_today_sbor():
    """
    Смотрит, есть ли отчеты в БД за сегодня
    Есть -> добавляет недостающие строки
    """
    # получаем сегодня в переменную
    today = date.today().strftime("%d.%m.%Y")
    # последняя дата в БД
    last_day_DB = check_in_DB_last_day_sbor()

    if today == last_day_DB:
        today_return = await check_report_yesterday_or_today_sbor(today)
        return today_return
    else:
        return None


async def check_in_DB_last_day_auto() -> str:
    """
    Проверяет последний день в БД
    """
    # импорт данных для соединения с БД
    import connection_data
    # подключение к БД
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = """
            SELECT `Дата выполнения работ` 
            FROM Daily_report_auto 
            ORDER BY 'Дата выполнения работ' DESC"""
            cursor.execute(sql_command)
            # получаем последний день в БД
            # записываем в переменную последний день в БД
            last_day = cursor.fetchall()[-1][0]
    return last_day


async def check_report_today_auto():
    """
    Смотрит, есть ли отчеты в БД за сегодня
    Есть -> добавляет недостающие строки
    """
    # получаем сегодня в переменную
    today = date.today().strftime("%d.%m.%Y")
    # последняя дата в БД
    last_day_DB = check_in_DB_last_day_auto()

    if today == last_day_DB:
        today_return = await check_report_yesterday_or_today_auto(today)
        return today_return
    else:
        return None


async def check_in_DB_last_day_VRO() -> str:
    """
    Проверяет последний день в БД
    """
    # импорт данных для соединения с БД
    import connection_data
    # подключение к БД
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = """
            SELECT `Дата выполнения работ` 
            FROM Daily_report_VRO 
            ORDER BY 'Дата выполнения работ' DESC"""
            cursor.execute(sql_command)
            # получаем последний день в БД
            # записываем в переменную последний день в БД
            last_day = cursor.fetchall()[-1][0]
    return last_day


async def check_report_today_VRO():
    """
    Смотрит, есть ли отчеты в БД за сегодня
    Есть -> добавляет недостающие строки
    """
    # получаем сегодня в переменную
    today = date.today().strftime("%d.%m.%Y")
    # последняя дата в БД
    last_day_DB = check_in_DB_last_day_VRO()

    if today == last_day_DB:
        today_return = await check_report_yesterday_or_today_VRO(today)
        return today_return
    else:
        return None
