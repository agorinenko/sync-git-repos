from time import sleep
from typing import Optional


class SleepHook:
    """
    Приостановка выполнения на некоторое время
    """

    def __init__(self, seconds: Optional[float] = 2):
        self.seconds = seconds

    def __call__(self):
        sleep(self.seconds)


class InputHook:
    """
    Ожидание ввода пользователя
    """

    def __init__(self, message: Optional[str] = None):
        self.message = message

    def __call__(self):
        text = input(self.message) if self.message else input()
        return text


class PrintHook:
    """
    Вывод
    """

    def __init__(self, message):
        self.message = message

    def __call__(self):
        print(self.message)


def create_hook(name: str, *args, **kwargs):
    """
    Динамическое создание хуков
    :param name: наименование хука
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    :return:
    """
    if name not in HOOKS_REGISTRY:
        raise NotImplementedError(f'Hook "{name}" not implemented.')

    return HOOKS_REGISTRY[name](*args, **kwargs)


HOOKS_REGISTRY = {
    'input': InputHook,
    'sleep': SleepHook,
    'print': PrintHook,
}
