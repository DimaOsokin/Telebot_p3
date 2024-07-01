from mysql.connector import connect
from values_in_all_report import *


def del_all_rows_in_DB_tabel_sbor():
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from Daily_report_sbor")
            print('Delete all rows from Daily_report_sbor')
            conn.commit()


def del_all_rows_in_DB_tabel_auto():
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from Daily_report_auto")
            print('Delete all rows from Daily_report_auto')
            conn.commit()


def del_all_rows_in_DB_tabel_VRO():
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from Daily_report_VRO")
            print('Delete all rows from Daily_report_VRO')
            conn.commit()


def load_full_table_report_sbor():
    values_report_sbor = full_values_report_sbor()
    # импорт данных для соединения с БД
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            for i in range(len(values_report_sbor)):
                if len(values_report_sbor[i]) != 10:
                    count_append = 10 - len(values_report_sbor[i])
                    for count in range(count_append):
                        values_report_sbor[i].append('')
                try:
                    cursor.execute("INSERT INTO Daily_report_sbor  VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                                   % (values_report_sbor[i][0], values_report_sbor[i][1], values_report_sbor[i][2],\
                                      values_report_sbor[i][3], values_report_sbor[i][4], values_report_sbor[i][5],\
                                      values_report_sbor[i][6], values_report_sbor[i][7], values_report_sbor[i][8], values_report_sbor[i][9]))
                    if i % 500 == 0 and i != 0:
                        conn.commit()
                        print(f"{i} строк занесены в Daily_report_sbor\nОсталось {(len(values_report_sbor)) - i}")
                except:
                   print(f"Не удалось занести запись в таблицу.\nДанные values_report_sbor\n{values_report_sbor[i]}")
            print('Вся таблица Daily_report_sbor занесена в БД')
            conn.commit()


def load_full_table_report_auto():
    values_report_auto = full_values_report_auto()
    # импорт данных для соединения с БД
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
                for i in range(len(values_report_auto)):
                    if len(values_report_auto[i]) != 22:
                        count_append = 22 - len(values_report_auto[i])
                        for count in range(count_append):
                            values_report_auto[i].append('')
                    try:
                        cursor.execute("INSERT INTO `Daily_report_auto` "
                                   "VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s',"
                                   "'%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s')"
                                   % (values_report_auto[i][0], values_report_auto[i][1], values_report_auto[i][2],
                                      values_report_auto[i][3], values_report_auto[i][4], values_report_auto[i][5],
                                      values_report_auto[i][6], values_report_auto[i][7], values_report_auto[i][8],
                                      values_report_auto[i][9], values_report_auto[i][10], values_report_auto[i][11],
                                      values_report_auto[i][12], values_report_auto[i][13], values_report_auto[i][14],
                                      values_report_auto[i][15], values_report_auto[i][16], values_report_auto[i][17],
                                      values_report_auto[i][18], values_report_auto[i][19], values_report_auto[i][20],
                                      values_report_auto[i][21]))
                        if i % 500 == 0 and i != 0:
                            conn.commit()
                            print(f"{i} строк занесены в Daily_report_auto\nОсталось {(len(values_report_auto)) - i}")
                    except:
                        print(f"Не удалось занести запись в таблицу.\nДанные values_report_auto\n{values_report_auto[i]}")
                print('Вся таблица Daily_report_auto занесена в БД')
                conn.commit()


def load_full_table_report_VRO():
    values_report_VRO = full_values_report_VRO()
    # импорт данных для соединения с БД
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            for i in range(len(values_report_VRO)):
                if len(values_report_VRO[i]) != 7:
                    count_append = 7 - len(values_report_VRO[i])
                    for count in range(count_append):
                        values_report_VRO[i].append('')
                try:
                    cursor.execute("INSERT INTO `Daily_report_VRO`"
                                   "VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s')"
                                   % (values_report_VRO[i][0], values_report_VRO[i][1], values_report_VRO[i][2],
                                      values_report_VRO[i][3], values_report_VRO[i][4], values_report_VRO[i][5],
                                      values_report_VRO[i][6], values_report_VRO[i][7]))
                    if i % 500 == 0 and i != 0:
                        conn.commit()
                        print(f"{i} строк занесены в Daily_report_VRO\nОсталось {(len(values_report_VRO)) - i}")
                except:
                    print(f"Не удалось занести запись в таблицу.\nДанные Daily_report_VRO\n{values_report_VRO[i]}")
            print('Вся таблица Daily_report_VRO занесена в БД')
            conn.commit()


def del_yesterday_report_sbor():
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from `Daily_report_sbor` where `Дата выполнения работ` = '%s'" % yesterday)
            print(f'Delete yesterday rows {yesterday}')
            conn.commit()


def del_yesterday_report_auto():
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from `Daily_report_auto` where `Дата выполнения работ` = '%s'" % yesterday)
            print(f'Delete yesterday rows {yesterday}')
            conn.commit()


def del_yesterday_report_VRO():
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    import connection_data
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from `Daily_report_VRO` where `Дата выполнения работ` = '%s'" % yesterday)
            print(f'Delete yesterday rows {yesterday}')
            conn.commit()


def all_del_rows_report():
    del_all_rows_in_DB_tabel_auto()
    del_all_rows_in_DB_tabel_VRO()
    del_all_rows_in_DB_tabel_sbor()


def all_del_yesterday_report():
    del_yesterday_report_auto()
    del_yesterday_report_VRO()
    del_yesterday_report_sbor()


def all_load_full_table_report():
    load_full_table_report_auto()
    load_full_table_report_VRO()
    load_full_table_report_sbor()


if __name__ == '__main__':
    try:
        import time
        star_time = int(time.time())

# SBOR
#         load_full_table_report_sbor()
#         del_all_rows_in_DB_tabel_sbor()
#         del_yesterday_report_sbor()
# AUTO
#         load_full_table_report_auto()
#         del_all_rows_in_DB_tabel_auto()
#         del_yesterday_report_auto()
# VRO
#         load_full_table_report_VRO()
#         del_all_rows_in_DB_tabel_VRO()
#         del_yesterday_report_VRO()
    #
# ALL
#         all_del_rows_report()
#         all_del_yesterday_report()
#         all_load_full_table_report()

        end_time = float(time.time() - star_time)
        print(f"\nВремя выполнения:\n{end_time / 60:.2f} минут\n{end_time:.1f} секунд")

    except Exception as err:
        print(f"\n\n{err}")

        end_time = float(time.time() - star_time)
        print(f"\nВремя выполнения:\n{end_time/60:.2f} минут\n{end_time:.1f} секунд")

