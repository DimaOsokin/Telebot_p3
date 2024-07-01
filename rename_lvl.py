from mysql.connector import connect
import connection_data


def rename_to_1():
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = "UPDATE id SET lvl = 1 WHERE id_tg = 830244764"
            cursor.execute(sql_command)
            conn.commit()


def rename_to_2():
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = "UPDATE id SET lvl = 2 WHERE id_tg = 830244764"
            cursor.execute(sql_command)
            conn.commit()


def rename_to_3():
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = "UPDATE id SET lvl = 3 WHERE id_tg = 830244764"
            cursor.execute(sql_command)
            conn.commit()


def rename_to_4():
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = "UPDATE id SET lvl = 4 WHERE id_tg = 830244764"
            cursor.execute(sql_command)
            conn.commit()


def rename_to_5():
    with connect(
            host=connection_data.host,
            user=connection_data.user,
            passwd=connection_data.passwd,
            database=connection_data.database) as conn:
        with conn.cursor() as cursor:
            sql_command = "UPDATE id SET lvl = 5 WHERE id_tg = 830244764"
            cursor.execute(sql_command)
            conn.commit()


async def rename_full_lvls(message):
    from main import bot
    from connect_to_DB_p3 import check_fio
    fio = await check_fio(message.from_user.id)
    if fio == 'Осокин Дмитрий':

        if message.text == '21':
            try:
                rename_to_1()
                await bot.send_message(message.chat.id, 'Ваш уровень доступа изменен 1 - сборщик')
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, f'{e}\nНе удалось изменить уровень доступа - сборщик')

        elif message.text == '22':
            try:
                rename_to_2()
                await bot.send_message(message.chat.id, 'Ваш уровень доступа изменен 2 - оператор')
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, f'{e}\nНе удалось изменить уровень доступа - оператор')

        elif message.text == '23':
            try:
                rename_to_3()
                await bot.send_message(message.chat.id, 'Ваш уровень доступа изменен 3 - контролер')
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, f'{e}\nНе удалось изменить уровень доступа - контролер')

        elif message.text == '24':
            try:
                rename_to_4()
                await bot.send_message(message.chat.id, 'Ваш уровень доступа изменен 4 - кладовщик')
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, f'{e}\nНе удалось изменить уровень доступа - кладовщик')

        elif message.text == '25':
            try:
                rename_to_5()
                await bot.send_message(message.chat.id, 'Ваш уровень доступа изменен 5 - руководитель')
            except Exception as e:
                print(e)
                await bot.send_message(message.chat.id, f'{e}\nНе удалось изменить уровень доступа - руководитель')


if __name__ == '__main__':
    pass
    # rename_to_1()
    # rename_to_2()
    # rename_to_3()
    # rename_to_4()
    # rename_to_5()
