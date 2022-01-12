from board import Board
import GLOBAL
from base import GameObject, LoadData
import pygame as pg


class BlockWall(GameObject):
    def __init__(self, board, sprite):
        super().__init__(board, sprite, GLOBAL.wall_layout)


class Tank(GameObject):
    def __init__(self, board: Board, sprite, bullet_sprite=None, speed=0.1,
                 bullet_speed=40, bullet_power=1, health=1, x=0, y=0, angle=0):
        super().__init__(board, sprite, GLOBAL.tank_layout, x=x, y=y, angle=angle)
        self.health = health
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power

    def shot(self):
        """ Обработка выстрела """
        b = Bullet(self.board, LoadData.load_image("bullet.png"),
                   x=self.transform.x + self.transform.size / 2 - 0.1,
                   y=self.transform.y - 0.4,
                   angle=self.transform.get_angle())
        return b

    def move(self, vector):
        """ Обработка перемещения """
        self.transform.x += vector[0] * self.speed
        self.transform.y += vector[1] * self.speed
        self.render()

    def death(self):
        """ Обработка смерти """
        pass

    def taking_damage(self, damage):
        """ Обработка получения урона """
        self.health -= damage
        if self.health <= 0:
            self.death()


class Player(Tank):
    def __init__(self, board: Board, sprite, x=0, y=0, angle=0):
        super().__init__(board, sprite, x=x, y=y, angle=angle)

    def movement(self):
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_w]:
            self.move((0, -1))
        if pressed_keys[pg.K_s]:
            self.move((0, 1))
        if pressed_keys[pg.K_a]:
            self.move((-1, 0))
        if pressed_keys[pg.K_d]:
            self.move((1, 0))


class Bullet(GameObject):
    def __init__(self, board, sprite, speed=20, power=1, x=0, y=0, angle=0):
        super().__init__(board, sprite, GLOBAL.bullet_layout, x=x, y=y, angle=angle)
        self.transform.size = 0.4
        self.speed = speed
        self.power = power
        self.change_sprite_size()

    def move(self):
        self.transform.x += self.speed
        self.transform.y += self.speed
