import GLOBAL  # Если убрать этот импорт, вся игра упадёт.
from base import UI


class Button(UI):
    def __init__(self, sprite, *sprite_group, x=0, y=0, center=None, func=None):
        super().__init__(sprite, *sprite_group, x=x, y=y, center=center)
        if func is not None:
            self.on_click.connect(func)


class Image(UI):
    def __init__(self, sprite, *sprite_group, x=0, y=0, center=None):
        super().__init__(sprite, *sprite_group, x=x, y=y, center=center)
