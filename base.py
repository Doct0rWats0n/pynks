import math
import pygame
import GLOBAL
from event_system import Event


class UI:
    def __init__(self, size: (100, 50)):
        self.size = size
        self.transform = Transform()
        self.event_init()

    def event_init(self):
        self.on_click = Event()
        self.on_hover = Event()

    def click(self):
        self.on_click()


class Transform:
    def __init__(self, x=0, y=0, angle=0, size=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.size = size
        self.event_change_angle = Event()

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        if angle % 90 != 0:
            raise ValueError(f"The angle must be a multiple of 90. Angle = {angle}")
        if angle >= 360:
            angle = angle - 360
        if angle <= 0:
            angle = angle + 360
        self.angle = angle
        self.event_change_angle()

    def get_cos(self):
        return math.cos(self.angle)

    def get_sin(self):
        return math.sin(self.angle)

    def __str__(self):
        return f"{self.x} {self.y}"


class GameObject(pygame.sprite.Sprite):
    def __init__(self, board, sprite, *sprite_group, x=0, y=0, angle=0, size=1):
        super().__init__(*sprite_group, GLOBAL.all_sprites)
        self.transform = Transform(x, y, size)
        self.transform.event_change_angle.connect(self.change_sprite_size)
        self.orig_image = sprite
        self.image = sprite
        self.board = board
        s = self.orig_image.get_size()
        self.ratio = s[0] / s[1]
        self.board.event_change_size.connect(self.change_sprite_size)
        self.board.event_change_view.connect(self.render)
        self.transform.set_angle(angle)
        self.change_sprite_size()
        self.event_on_move = Event()
        self.event_on_move.connect(self.render)

    def change_sprite_size(self):
        """ Меняет размер спрайта """
        self.image = pygame.transform.scale(self.orig_image, (self.board.cell_size * self.transform.size * self.ratio,
                                                              self.board.cell_size * self.transform.size))
        rotated_image = pygame.transform.rotate(self.image, self.transform.get_angle())
        self.image = rotated_image
        self.render()

    def render(self):
        """ Подстраивание картинки под игровое поле """
        self.rect = self.image.get_rect().move(
            (self.board.cell_size * self.transform.x + self.board.left),
            (self.board.cell_size * self.transform.y + self.board.top))


class AnimatedGameObject(GameObject):
    def __init__(self, board, sprite, *sprite_group, x=0, y=0, angle=0, size=1, animation_speed=20):
        self.frames = sprite
        self.cur_frame = 0
        self.animation_speed = animation_speed
        self.cur_tick = 0
        super().__init__(board, sprite[0], *sprite_group, GLOBAL.animated_layout, x=x, y=y, angle=angle, size=size)
        self.board.event_tick.connect(self.add_tick)

    def render(self):
        self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                            (self.board.cell_size * self.transform.size * self.ratio,
                                             self.board.cell_size * self.transform.size))
        self.rect = self.image.get_rect().move(
            (self.board.cell_size * self.transform.x + self.board.left),
            (self.board.cell_size * self.transform.y + self.board.top))

    def add_tick(self):
        if self.cur_tick == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.render()
        self.cur_tick = (self.cur_tick + 1) % self.animation_speed
