def log_info(func='log_info', path_file='not_specified', message=None) -> None:
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


def log_err(func='log_err', path_file='not_specified', message=None) -> None:
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

















if __name__ == "__main__":
    pass
