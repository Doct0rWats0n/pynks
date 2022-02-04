import GLOBAL  # Если убрать этот импорт, вся игра упадёт.
from base import UI


class Button(UI):
    def __init__(self, sprites, *sprite_group, x=0, y=0, center=None, func=None, angle=0, size=1, scene='main'):
        super().__init__(sprites[0], *sprite_group, x=x, y=y, center=center, angle=angle, size=size)
        if func is not None:
            self.on_click.connect(func)
        self.scene = scene
        self.main_image = sprites[0]
        self.on_hold_image = sprites[1]
        self.on_touch_image = sprites[2]
        GLOBAL.event_click.connect(self.click)
        GLOBAL.event_hold.connect(self.hold)
        GLOBAL.event_move.connect(self.touch)

    def click(self, pos, scene):
        if self.rect.collidepoint(pos) and scene == self.scene:
            self.image = self.on_touch_image
            GLOBAL.bip.play()
            self.on_click()

    def hold(self, pos, scene):
        if self.rect.collidepoint(pos) and scene == self.scene:
            self.image = self.on_hold_image
            self.on_hold()

    def touch(self, pos, scene):
        if self.rect.collidepoint(pos) and scene == self.scene:
            self.image = self.on_touch_image
            self.on_touch()
        elif self.image == self.on_touch_image and scene == self.scene:
            self.image = self.main_image


class Image(UI):
    def __init__(self, sprite, *sprite_group, x=0, y=0, center=None, angle=0, size=1, text=''):
        super().__init__(sprite, *sprite_group, x=x, y=y, center=center, angle=angle, size=size)
        t = GLOBAL.main_font.render(text, True, (100, 255, 100))
        x = self.image.get_width() // 2 - t.get_width() // 2
        y = self.image.get_height() // 2 - t.get_height() // 2
        self.image.blit(t, (x, y))
        self.render()
