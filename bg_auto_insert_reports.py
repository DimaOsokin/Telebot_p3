from datetime import datetime
import asyncio
import aioschedule
import logging

from from_excel_table_in_DB import all_del_rows_report, all_load_full_table_report
from update_daily_report import auto_insert_report_sbor, auto_insert_report_auto, auto_insert_report_VRO

# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger('__bg_auto_insert_reports__')
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler(f"log/bg_auto_insert_reports.log", mode='a+', encoding='utf-8')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)


async def schedule_auto_update_reports(morning=False, evening=False, night=False):
    if morning:
        del morning
        try:
            var = await auto_insert_report_sbor(day=0)
            del var
            var = await auto_insert_report_auto(day=0)
            del var
            var = await auto_insert_report_VRO(day=0)
            del var
            py_logger.info(f"Сегодняшние отчёты обновлены успешно")
        except Exception as err:
            py_logger.exception(f"Morning exception - ({err})")
            del err

    elif evening:
        del evening
        try:
            var = await auto_insert_report_sbor(day=1)
            del var
            var = await auto_insert_report_auto(day=1)
            del var
            var = await auto_insert_report_VRO(day=1)
            del var
            py_logger.info(f"Вчерашние отчёты обновлены успешно")
        except Exception as err:
            py_logger.exception(f"Evening exception - ({err})")
            del err

    elif night:
        del night
        print(f'night {datetime.now()}')
        # нужно, что бы данная функция отработала 1 день в месяце, желательно ночью
        try:
            var = await all_del_rows_report()
            del var
            var = await all_load_full_table_report()
            del var
        except Exception as err:
            print(f"Night exception - ({err})")
            del err


async def main():
    # Время, в которое сработает планировщик и запустит функцию и передаст аргумент morning=True
    aioschedule.every().day.at("19:40").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:41").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:42").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:43").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:44").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:45").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:46").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:47").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:48").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:49").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:50").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:51").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:52").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:53").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:54").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:55").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:56").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:57").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:58").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("19:59").do(schedule_auto_update_reports, morning=True)

    aioschedule.every().day.at("20:00").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:01").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:02").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:03").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:04").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:05").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:06").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:07").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:08").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:09").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("20:10").do(schedule_auto_update_reports, morning=True)

    aioschedule.every().day.at("20:30").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("21:00").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("22:00").do(schedule_auto_update_reports, morning=True)
    aioschedule.every().day.at("23:00").do(schedule_auto_update_reports, morning=True)

    # Время, в которое сработает планировщик и запустит функцию и передаст аргумент evening=True
    aioschedule.every().day.at("07:40").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:41").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:42").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:43").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:44").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:45").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:46").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:47").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:48").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:49").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:50").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:51").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:52").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:53").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:54").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:55").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:56").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:57").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:58").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("07:59").do(schedule_auto_update_reports, evening=True)

    aioschedule.every().day.at("08:00").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:01").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:02").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:03").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:04").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:05").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:06").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:07").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:08").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:09").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("08:10").do(schedule_auto_update_reports, evening=True)

    aioschedule.every().day.at("08:30").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("09:00").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("10:00").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("11:00").do(schedule_auto_update_reports, evening=True)
    aioschedule.every().day.at("12:01").do(schedule_auto_update_reports, evening=True)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(45)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
