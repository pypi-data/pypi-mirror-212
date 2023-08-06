import logging
import socket
import sys

import log.server_log_config
import log.client_log_config

sys.path.append('../')

# метод определения модуля, источника запуска.
if sys.argv[0].find('client_module') == -1:
    logger = logging.getLogger('server_module')
else:
    logger = logging.getLogger('client_module')


def logs(func_to_log):
    """
    Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию об имени вызываемой функции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    """

    def log_saver(*args, **kwargs):
        logger.debug(
            f'Была вызвана функция {func_to_log.__name__} '
            f'c параметрами {args}, {kwargs}. '
            f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса на авторизацию.
    Если клиент не авторизован, генерирует исключение TypeError.
    """

    def checker(*args, **kwargs):
        # Проверяем, что первый аргумент - экземпляр Server.
        # Импортировать необходимо тут, иначе ошибка рекурсивного импорта.
        from server import Server
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # Server.
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True
            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presence, то разрешаем.
            for arg in args:
                if isinstance(arg, dict):
                    if 'action' in arg and arg['action'] == 'presence':
                        found = True
            # Если не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
