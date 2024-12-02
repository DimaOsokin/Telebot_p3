async def log_info(func='log_info', path_file='not_specified', message=None) -> None:
    """

    :param func: Название функции
    :param path_file: Название файла
    :param message: Описание ошибки
    :return: None
    """
    import logging

    # получение пользовательского логгера и установка уровня логирования
    py_logger = logging.getLogger(func)
    py_logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика в соответствии с нашими нуждами
    py_handler = logging.FileHandler(f"log/{path_file}.log", mode='a+', encoding='utf-8')
    py_formatter = logging.Formatter("\n%(name)s %(asctime)s %(levelname)s %(message)s",
                                     datefmt='%d.%m.%y %H:%M:%S')

    # добавление форматировщика к обработчику
    py_handler.setFormatter(py_formatter)
    # добавление обработчика к логгеру
    py_logger.addHandler(py_handler)

    py_logger.info(message)


async def log_err(func='log_err', path_file='not_specified', message=None) -> None:
    """

    :param func: Название функции
    :param path_file: Название файла
    :param message: Описание ошибки
    :return: None
    """
    import logging

    # получение пользовательского логгера и установка уровня логирования
    py_logger = logging.getLogger(func)
    py_logger.setLevel(logging.ERROR)

    # настройка обработчика и форматировщика в соответствии с нашими нуждами
    py_handler = logging.FileHandler(f"log/{path_file}.log", mode='a+', encoding='utf-8')
    py_formatter = logging.Formatter("\n%(name)s %(asctime)s %(levelname)s %(message)s",
                                     datefmt='%d.%m.%y %H:%M:%S')

    # добавление форматировщика к обработчику
    py_handler.setFormatter(py_formatter)
    # добавление обработчика к логгеру
    py_logger.addHandler(py_handler)

    py_logger.exception(message)


    await alert_message_to_telegram(func=func, path_file=path_file, message=message)


async def alert_message_to_telegram(func, path_file, message) -> None:
    """
    Отправляет сообщение об ошибках в тг-канал
    :param func: Наименование функции в которой произошла ошибка
    :param path_file: Файл с ошибкой
    :param message: Сообщение об ошибке
    :return: None
    """
    from main import bot
    chat_id_chanel = "-1002180252930"
    await bot.send_message(chat_id=chat_id_chanel, text=f"Функция: {func}\nФайл: {path_file}\nОшибка: {message}")











if __name__ == "__main__":
    pass
