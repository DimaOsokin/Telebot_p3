from mysql.connector import connect
from datetime import datetime, timedelta
import connection_data
from values_in_all_report import *
import my_logers


async def auto_insert_report_sbor(day=1):
    """
    Заполняет отчет за вчера (по умолчанию)
    Может заполнять отчет за сегодня, если передать значение day=0
    """
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            need_day = (datetime.now() - timedelta(days=day)).strftime('%d.%m.%Y')
            # количество строк в эксель за вчера/сегодня
            rows_in_excel_table = full_values_report_sbor(need_day)
            # количество записей в эксель
            count_last_day_rows_excel = len(rows_in_excel_table)
            values_report_sbor = rows_in_excel_table
            # удалить записи за последний день из БД
            sql_command = "DELETE FROM `Daily_report_sbor` WHERE `Дата выполнения работ` = '%s'" % need_day
            cursor.execute(sql_command)
            # получаем данные из эксель таблицы за последний день
            for i in range(0, count_last_day_rows_excel):
                try:
                    # добавляем данные в БД за вчера
                    cursor.execute("INSERT INTO `Daily_report_sbor`  "
                                   "VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                                   % (values_report_sbor[i][0], values_report_sbor[i][1], values_report_sbor[i][2],
                                      values_report_sbor[i][3], values_report_sbor[i][4], values_report_sbor[i][5],
                                      values_report_sbor[i][6], values_report_sbor[i][7], values_report_sbor[i][8],
                                      values_report_sbor[i][9]))
                except Exception as err:
                    await my_logers.log_err(func=f"{__name__} auto_insert_report_sbor", message={err})
            conn.commit()


async def auto_insert_report_auto(day=1):
    """
    Заполняет отчет за вчера (по умолчанию)
    Может заполнять отчет за сегодня, если передать значение day=0
    """
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            need_day = (datetime.now() - timedelta(days=day)).strftime('%d.%m.%Y')
            # количество строк в эксель за вчера/сегодня
            rows_in_excel_table = await full_values_report_auto(need_day)
            # количество записей в эксель
            values_report_auto = rows_in_excel_table
            # удалить записи за последний день из БД
            sql_command = "DELETE FROM `Daily_report_auto` WHERE `Дата выполнения работ` = '%s'" % need_day
            cursor.execute(sql_command)
            # выравнивает длину строки до 21
            for i in range(len(values_report_auto)):
                if len(values_report_auto[i]) != 22:
                    count_append = 22 - len(values_report_auto[i])
                    # выравнивает лист до длины в 22 символа
                    for count in range(count_append):
                        values_report_auto[i].append('')
                try:
                    # добавляет каждый элемент вложенного списка в БД
                    cursor.execute("INSERT INTO `Daily_report_auto` VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s',"
                                   "'%s','%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s')"
                                   % (values_report_auto[i][0], values_report_auto[i][1], values_report_auto[i][2],
                                      values_report_auto[i][3], values_report_auto[i][4], values_report_auto[i][5],
                                      values_report_auto[i][6], values_report_auto[i][7], values_report_auto[i][8],
                                      values_report_auto[i][9], values_report_auto[i][10],
                                      values_report_auto[i][11],
                                      values_report_auto[i][12], values_report_auto[i][13],
                                      values_report_auto[i][14],
                                      values_report_auto[i][15], values_report_auto[i][16],
                                      values_report_auto[i][17],
                                      values_report_auto[i][18], values_report_auto[i][19],
                                      values_report_auto[i][20],
                                      values_report_auto[i][21]))
                except Exception as err:
                    await my_logers.log_err(func=f"{__name__} auto_insert_report_auto", message={err})

            conn.commit()


async def auto_insert_report_VRO(day=1):
    """
    Заполняет отчет за вчера (по умолчанию)
    Может заполнять отчет за сегодня, если передать значение day=0
    """
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            need_day = (datetime.now() - timedelta(days=day)).strftime('%d.%m.%Y')
            # количество строк в эксель за вчера/сегодня
            rows_in_excel_table = await full_values_report_VRO(need_day)
            # количество записей в эксель
            count_last_day_rows_excel = len(rows_in_excel_table)
            values_report_VRO = rows_in_excel_table
            # удалить записи за последний день из БД
            sql_command = "DELETE FROM `Daily_report_VRO` WHERE `Дата выполнения работ` = '%s'" % need_day
            cursor.execute(sql_command)
            for i in range(len(values_report_VRO)):
                if len(values_report_VRO[i]) != 8:
                    count_append = 8 - len(values_report_VRO[i])
                    # выравнивает лист до длины в 8 символов
                    for count in range(count_append):
                        values_report_VRO[i].append('')
                try:
                    # добавляет каждый элемент вложенного списка в БД
                    cursor.execute("INSERT INTO `Daily_report_VRO`"
                                   "VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s')"
                                   % (values_report_VRO[i][0], values_report_VRO[i][1], values_report_VRO[i][2],
                                      values_report_VRO[i][3], values_report_VRO[i][4], values_report_VRO[i][5],
                                      values_report_VRO[i][6], values_report_VRO[i][7]))
                except Exception as err:
                    await my_logers.log_err(func=f"{__name__} auto_insert_report_VRO", message={err})

            conn.commit()


# обновляет отчёты 3‑х участков
async def auto_insert_reports(message, day='yesterday'):
    from main import bot
    if day == 'yesterday':
        day = int(1)
        who_day = 'вчера'
    elif day == 'today':
        day = int(0)
        who_day = 'сегодня'

    try:
        await bot.send_message(message.chat.id, f'Начинаю обновлять отчёты за {who_day}, пожалуйста подождите')
        await auto_insert_report_sbor(day)
        await bot.send_message(message.chat.id, f"Обновлены отчёты СУ")
    except Exception as Exception_SU:
        await bot.send_message(message.chat.id, f'Ошибка обновления отчётов СУ за вчера:\n{Exception_SU}')
    try:
        await auto_insert_report_auto(day)
        await bot.send_message(message.chat.id, f"Обновлены отчёты АУ")
    except Exception as Exception_AU:
        await bot.send_message(message.chat.id, f'Ошибка обновления отчётов АУ за вчера:\n{Exception_AU}')
    try:
        await auto_insert_report_VRO(day)
        await bot.send_message(message.chat.id, 'Обновлены отчёты ВРО')
    except Exception as Exception_VRO:
        await bot.send_message(message.chat.id, f'Ошибка обновления отчётов ВРО за вчера:\n{Exception_VRO}')

    await bot.send_message(message.chat.id, 'Завершено обновление отчётов')


if __name__ == '__main__':
    pass
