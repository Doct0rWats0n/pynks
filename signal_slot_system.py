class Signal:
    def __init__(self):
        self.slots = []

    def __call__(self, *args, **kwargs):
        """
        Запуск всех обработчиков
        """
        for i, slot in enumerate(self.slots):
            if slot is not None:
                slot(*args, **kwargs)
            else:
                del self.slots[i]

    def connect(self, slot):
        """
        Подключение обработчика
        """
        self.slots.append(slot)

    def disconnect(self, slot):
        """
        Отсоедиение обработчика
        """
        del self.slots[self.slots.index(slot)]

    def disconnect_all(self):
        """
        Отсоединение от всех слотов
        """
        self.slots = []

