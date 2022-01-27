from board import Board
import GLOBAL
from base import GameObject
from loaddata import LoadData
import pygame as pg


class Tank(GameObject):
    def __init__(self, board: Board, sprite, bullet_sprite=None, speed=0.1,
                 bullet_speed=40, bullet_power=1, health=1, x=0, y=0, angle=0):
        super().__init__(board, sprite, GLOBAL.tank_layout, x=x, y=y, angle=angle)
        self.health = health
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power
        self.shoot_sound = LoadData.load_sound("tank_hit.wav")
        self.explosion_sound = LoadData.load_sound("explosion.wav")

    def shot(self):
        self.shoot_sound.play()
        """ Обработка выстрела """
        if self.transform.angle == 360:
            pos = [self.transform.size / 2 - 0.1, -0.2]
        elif self.transform.angle == 180:
            pos = [self.transform.size / 2 - 0.1, 0.7]
        elif self.transform.angle == 90:
            pos = [-0.2, self.transform.size / 2 - 0.1]
        elif self.transform.angle == 270:
            pos = [0.7, self.transform.size / 2 - 0.1]
        Bullet(self.board, LoadData.load_image("bullet.png"),
               x=self.transform.x + pos[0],
               y=self.transform.y + pos[1],
               angle=self.transform.get_angle())

    def move(self, vector):
        """ Обработка перемещения """
        self.transform.x += vector[0] * self.speed
        if pg.sprite.spritecollideany(self, GLOBAL.wall_layout):
            pass
        self.transform.y += vector[1] * self.speed
        if pg.sprite.spritecollideany(self, GLOBAL.wall_layout):
            pass
        self.event_on_move()

    def death(self):
        """ Обработка смерти """
        self.explosion_sound.play()

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
    def __init__(self, board, sprite, speed=0.3, power=1, x=0, y=0, angle=0):
        super().__init__(board, sprite, GLOBAL.bullet_layout, x=x, y=y, angle=angle)
        self.transform.size = 0.4
        self.speed = speed
        self.power = power
        self.explosion = LoadData.load_sound("bullet.wav")
        self.change_sprite_size()
        self.vec = [0, 0]
        if self.transform.angle == 360:
            self.vec[1] = -1
        elif self.transform.angle == 180:
            self.vec[1] = 1
        elif self.transform.angle == 90:
            self.vec[0] = -1
        elif self.transform.angle == 270:
            self.vec[0] = 1

    def move(self):
        self.transform.x += self.speed * self.vec[0]
        self.transform.y += self.speed * self.vec[1]
        if pg.sprite.spritecollideany(self, GLOBAL.wall_layout):
            self.explosion.play()
            self.kill()
        self.event_on_move()
