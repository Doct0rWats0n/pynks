import inspect


class Event:
    def __init__(self):
        self.subscribers = []

    def __call__(self, *args, **kwargs):
        """ Уведомление подписчиков """
        for ind,  function in enumerate(self.subscribers):
            if function is not None:
                function(*args, **kwargs)
            else:
                del self.subscribers[ind]

    def connect(self, function):
        """ Подключение к событию """
        if function in self.subscribers:
            raise EventException(f'The function "{function.__name__}" was already signed')
        if not inspect.isfunction(function) and not inspect.ismethod(function):
            raise EventException(f'"{function.__name__} is not function or method"')
        self.subscribers.append(function)

    def disconnect(self, slot):
        """ Отключение от события """
        del self.subscribers[self.subscribers.index(slot)]

    def disconnect_all(self):
        """ Отключение всех событий """
        self.subscribers.clear()


class EventException(Exception):
    pass
