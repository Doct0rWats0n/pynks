from ui import UI
import pygame as pg
from loaddata import LoadData
from base import Transform
from event_system import Event
from GLOBAL import *
from main import App


class UI_Object(pg.sprite.Sprite):
    def __init__(self, x, y, imagepath, ui_menu, *sprite_group):
        super().__init__(*sprite_group)
        self.image = LoadData.load_image(imagepath)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.transform = Transform()
        self.ui_menu = ui_menu
        self.ui_menu.change_sprite_size.connect(self.resize_image)

    def get_image_width(self):
        return self.image.get_width()

    def get_image_height(self):
        return self.image.get_height()

    def resize_image(self, width, height):
        self.image = pg.transform.scale(self.image, (width, height))

    def move_image(self, x, y):
        self.rect.x, self.rect.y = x, y


class Background(UI_Object):
    def __init__(self, x, y, imagename, *sprite_group):
        super().__init__(x, y, imagename, *sprite_group)


class Button(UI_Object):
    def __init__(self, x, y, imagename, *sprite_group):
        super().__init__(x, y, imagename, *sprite_group)

        self.click = Event()
        self.hover = Event()

    def check_click(self, x, y):
        if self.rect.x < x < self.rect.x + self.rect.width and self.rect.y < y < self.rect.y + self.rect.height:
            self.click()

    def add_event_to_click(self, function):
        self.click.connect(function)


class Menu_Ui(UI):
    def __init__(self):
        super().__init__()
        self.change_sprite_size = Event()

    def show_menu(self):
        pg.init()
        screen = pg.display.set_mode(SIZE)
        pg.display.set_caption('TankMenu')

        self.change_sprite_size = Event()
        pics = ['start.png', 'settings.png', 'shop.png', 'exit.png']
        x, y = 100, 450
        spacer = 20
        for pic in pics:
            a = Button(x, y, pic, self, buttons_layout)
            if 'exit' in pic:
                a.add_event_to_click(lambda: self.exit())
            else:
                a.add_event_to_click(lambda: print('Hello World'))
            x += a.get_image_width() + spacer
        self.playing = True
        while self.playing:
            screen.fill('white')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in buttons_layout:
                        i.check_click(*event.pos)
            buttons_layout.draw(screen)
            pg.display.flip()
        pg.quit()

    def start_game(self):
        app = App()
        app.run()

    def open_settings(self):
        pass

    def exit(self):
        self.playing = False

    def do_resize(self):
        pass


if __name__ == '__main__':
    menu = Menu_Ui()
    menu.show_menu()
