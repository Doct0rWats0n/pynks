import GLOBAL  # Если убрать этот импорт, вся игра упадёт.
from base import UI


class Button(UI):
    def __init__(self, sprites, *sprite_group, x=0, y=0, center=None, func=None, angle=0, size=1):
        super().__init__(sprites[0], *sprite_group, x=x, y=y, center=center, angle=angle, size=size)
        if func is not None:
            self.on_click.connect(func)
        self.main_image = sprites[0]
        self.on_hold_image = sprites[1]
        self.on_touch_image = sprites[2]
        GLOBAL.event_click.connect(self.click)
        GLOBAL.event_hold.connect(self.hold)
        GLOBAL.event_move.connect(self.touch)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.on_touch_image
            GLOBAL.bip.play()
            self.on_click()

    def hold(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.on_hold_image
            self.on_hold()

    def touch(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.on_touch_image
            self.on_touch()
        else:
            if self.image == self.on_touch_image:
                self.image = self.main_image


class Image(UI):
    def __init__(self, sprite, *sprite_group, x=0, y=0, center=None, angle=0, size=1):
        super().__init__(sprite, *sprite_group, x=x, y=y, center=center, angle=angle,size=size)
