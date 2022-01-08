class Signal:
    def __init__(self):
        self.slots = []

    def __call__(self, *args, **kwargs):
        for i, slot in enumerate(self.slots):
            if slot is not None:
                slot(*args, **kwargs)
            else:
                del self.slots[i]

    def call(self, *args, **kwargs):
        self.__call__(*args, **kwargs)

    def connect(self, slot):

        self.slots.append(slot)

    def disconnect(self, slot):
        del self.slots[self.slots.index(slot)]

    def disconnect_all(self):
        self.slots = []

