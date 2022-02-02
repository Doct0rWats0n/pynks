import math
import pygame
import GLOBAL
from event_system import Event


class UI(pygame.sprite.Sprite):
    def __init__(self, sprites, *sprite_group, x=0, y=0, center=None, angle=0, size=1):
        super().__init__(GLOBAL.ui_layout, *sprite_group)
        self.image = sprites
        self.rect = self.image.get_rect()
        self.center = center
        self.transform = Transform(x=x, y=y, angle=angle, size=size)
        self.transform.event_change_pos.connect(self.render)
        GLOBAL.event_window_resize.connect(self.render)
        self.image = pygame.transform.scale(self.image, (self.transform.size * self.image.get_width(),
                                                         self.transform.size * self.image.get_height()))
        self.image = pygame.transform.rotate(self.image, self.transform.get_angle())
        self.render()
        self.scene = 'main'
        self.event_init()

    def event_init(self):
        self.on_click = Event()
        self.on_hold = Event()
        self.on_touch = Event()

    def render(self):
        if self.center:
            self.rect = self.image.get_rect(). \
                move(GLOBAL.SIZE[0] // 2 - self.image.get_width() // 2 + self.transform.x,
                     GLOBAL.SIZE[1] // 2 - self.image.get_height() // 2 + self.transform.y)
        else:
            self.rect = self.image.get_rect().move(self.transform.x,
                                                   self.transform.y)


class Transform:
    def __init__(self, x=0, y=0, angle=0, size=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.size = size
        self.event_change_angle = Event()
        self.event_change_pos = Event()

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y
        self.event_change_pos()

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
        GLOBAL.event_tick.connect(self.check_tick)
        GLOBAL.event_change_size.connect(self.change_sprite_size)
        GLOBAL.event_change_view.connect(self.render)
        GLOBAL.event_tick.connect(self.add_tick)
        self.transform.set_angle(angle)
        self.change_sprite_size()
        self.event_on_move = Event()
        self.event_on_move.connect(self.render)

    def disconnect(self):
        GLOBAL.event_tick.disconnect(self.check_tick)
        GLOBAL.event_change_size.disconnect(self.change_sprite_size)
        GLOBAL.event_change_view.disconnect(self.render)
        GLOBAL.event_tick.disconnect(self.add_tick)

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

    def add_tick(self):
        # virtual method
        pass

    def check_tick(self):
        # virtual method
        pass


class AnimatedGameObject(GameObject):
    def __init__(self, board, sprite, *sprite_group, x=0, y=0, angle=0, size=1, animation_speed=20):
        self.frames = sprite
        self.cur_frame = 0
        self.animation_speed = animation_speed
        self.cur_tick = 0
        super().__init__(board, sprite[0], *sprite_group, GLOBAL.animated_layout, x=x, y=y, angle=angle, size=size)

    def render(self):
        self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                            (self.board.cell_size * self.transform.size * self.ratio,
                                             self.board.cell_size * self.transform.size))
        self.rect = self.image.get_rect().move(
            (self.board.cell_size * self.transform.x + self.board.left),
            (self.board.cell_size * self.transform.y + self.board.top))

    def add_tick(self):
        self.cur_tick = (self.cur_tick + 1) % self.animation_speed
        if self.cur_tick == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.render()


class Collide(pygame.sprite.Sprite):
    def __init__(self, tank, xy1, xy2):
        super().__init__(GLOBAL.collide_layout)
        self.tank = tank
        self.const_pos = xy1
        self.transform = Transform(xy1[0] + self.tank.transform.x, xy1[1] + self.tank.transform.y)
        self.size = xy2

        self.orig_image = GLOBAL.collide_sprite
        self.image = GLOBAL.collide_sprite
        self.is_collide = False
        self.change_sprite_size()

        self.tank.event_on_move.connect(self.move)
        GLOBAL.event_tick.connect(self.check_tick)
        GLOBAL.event_change_size.connect(self.change_sprite_size)
        GLOBAL.event_change_view.connect(self.render)

    def disconnect(self):
        GLOBAL.event_tick.disconnect(self.check_tick)
        GLOBAL.event_change_size.disconnect(self.change_sprite_size)
        GLOBAL.event_change_view.disconnect(self.render)

    def check_tick(self):
        if pygame.sprite.spritecollideany(self, GLOBAL.wall_layout) or \
                len(pygame.sprite.spritecollide(self, GLOBAL.collide_layout, dokill=False)) > 1:
            self.is_collide = True
        else:
            self.is_collide = False

    def move(self):
        self.transform.set_position(self.const_pos[0] + self.tank.transform.x,
                                    self.const_pos[1] + self.tank.transform.y)
        self.render()

    def change_sprite_size(self):
        self.image = pygame.transform.scale(self.orig_image, (self.size[0] * self.tank.board.cell_size,
                                                              self.size[1] * self.tank.board.cell_size))
        self.render()

    def render(self):
        self.rect = self.image.get_rect().move(
            (self.tank.board.cell_size * self.transform.x + self.tank.board.left),
            (self.tank.board.cell_size * self.transform.y + self.tank.board.top))
