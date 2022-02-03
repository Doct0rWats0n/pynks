from typing import Tuple
from board import Board
import GLOBAL
from base import GameObject, Collide
import pygame as pg
import blocks
import way_finder


class Tank(GameObject):
    def __init__(self, board: Board, sprite, bullet_sprite=None, speed=0.1, reload_speed=20,
                 bullet_speed=40, bullet_power=1, health=1, x=0, y=0, angle=0):
        super().__init__(board, sprite, GLOBAL.tank_layout, x=x, y=y, angle=angle)
        self.health = health
        self.speed = speed
        self.reload_speed = reload_speed
        self.cur_tick = 0
        self.bullet_speed = bullet_speed
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power
        self.enemy_bullet_group = GLOBAL.player_bullet_layout
        self.this_bullet_group = GLOBAL.enemy_bullet_layout
        self.is_dead = False
        self.is_took_bonus = False
        self.collide_up = Collide(self, (0.15, 0.05), (0.7, 0.1))
        self.collide_down = Collide(self, (0.15, 0.85), (0.7, 0.1))
        self.collide_left = Collide(self, (0.05, 0.15), (0.1, 0.7))
        self.collide_right = Collide(self, (0.85, 0.15), (0.1, 0.7))
        self.collides = [self.collide_up, self.collide_down,
                         self.collide_left, self.collide_right]

    def remake_collide(self):
        pass

    @staticmethod
    def live(func):
        def _(self):
            if not self.is_dead:
                return func(self)
        return _

    def check_tick(self):
        if pg.sprite.spritecollideany(self, self.enemy_bullet_group) and not self.is_dead:
            self.death()
        if pg.sprite.spritecollideany(self, GLOBAL.bonus_layout) and not self.is_took_bonus:
            pg.sprite.spritecollideany(self, GLOBAL.bonus_layout).kill()
            self.activate_bonus()

    def activate_bonus(self):
        self.is_took_bonus = True
        self.speed = 0.12

    def add_tick(self):
        self.cur_tick += 1 if self.cur_tick < self.reload_speed else 0

    def shot(self):
        """ Обработка выстрела """
        if self.cur_tick == self.reload_speed:
            self.cur_tick = 0
            GLOBAL.hit_sound.play()
            if self.transform.angle == 360:
                pos = [self.transform.size / 2 - 0.1, -0.2]
            elif self.transform.angle == 180:
                pos = [self.transform.size / 2 - 0.1, 0.7]
            elif self.transform.angle == 90:
                pos = [-0.2, self.transform.size / 2 - 0.1]
            elif self.transform.angle == 270:
                pos = [0.7, self.transform.size / 2 - 0.1]
            Bullet(self.board, GLOBAL.bullet_sprite,
                   x=self.transform.x + pos[0],
                   y=self.transform.y + pos[1],
                   angle=self.transform.get_angle(), bullet_group=self.this_bullet_group)

    def move(self, vector: Tuple[int, int]):
        """ Обработка перемещения """
        if (not self.collide_up.is_collide and vector == (0, -1)) or \
                (not self.collide_down.is_collide and vector == (0, 1)):
            self.transform.y += vector[1] * self.speed
        if (not self.collide_left.is_collide and vector == (-1, 0)) or \
                (not self.collide_right.is_collide and vector == (1, 0)):
            self.transform.x += vector[0] * self.speed
        self.event_on_move()

    def death(self):
        """ Обработка смерти """
        self.is_dead = True
        GLOBAL.event_kill()
        for i in self.collides:
            i.disconnect()
            i.kill()
        self.disconnect()
        blocks.Boom(self.board, x=self.transform.x, y=self.transform.y)
        GLOBAL.explosion.play()
        self.kill()

    def taking_damage(self, damage):
        """ Обработка получения урона """
        self.health -= damage
        if self.health <= 0:
            self.death()


class Player(Tank):
    def __init__(self, board: Board, x=0, y=0, angle=0):
        super().__init__(board, GLOBAL.player_sprite, x=x, y=y, angle=angle)
        self.enemy_bullet_group = GLOBAL.enemy_bullet_layout
        self.this_bullet_group = GLOBAL.player_bullet_layout
        self.reload_speed = 30
        GLOBAL.event_defeat.connect(self.death)

    def disconnect(self):
        GLOBAL.event_tick.disconnect(self.check_tick)
        GLOBAL.event_change_size.disconnect(self.change_sprite_size)
        GLOBAL.event_change_view.disconnect(self.render)
        GLOBAL.event_tick.disconnect(self.add_tick)
        GLOBAL.event_defeat.disconnect(self.death)

    def movement(self):
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_w]:
            self.move((0, -1))
        elif pressed_keys[pg.K_s]:
            self.move((0, 1))
        elif pressed_keys[pg.K_a]:
            self.move((-1, 0))
        elif pressed_keys[pg.K_d]:
            self.move((1, 0))


class Enemy(Tank):
    def __init__(self, board, last_x, last_y, last_map, x=0, y=0):
        super().__init__(board, GLOBAL.enemy_sprite, x=x, y=y)
        self.way = way_finder.get_way(y, x, last_x, last_y, last_map)
        self.cur_move = self.way.pop()[::-1]
        self.t_x, self.t_y = x + self.cur_move[0], y + self.cur_move[1]

    def check_tick(self):
        if pg.sprite.spritecollideany(self, self.enemy_bullet_group) and not self.is_dead:
            self.death()
        if int(self.transform.x) == self.t_x and int(self.transform.y) == self.t_y:
            if self.way:
                self.cur_move = self.way.pop()[::-1]
                if self.cur_move[0] == 1:
                    print("HELOHEOHLEH")
                    self.transform.set_angle(270)
                elif self.cur_move[0] == -1:
                    self.transform.set_angle(90)
                elif self.cur_move[1] == 1:
                    self.transform.set_angle(180)
                elif self.cur_move[1] == -1:
                    self.transform.set_angle(0)
                self.t_x, self.t_y = self.t_x + self.cur_move[0], self.t_y + self.cur_move[1]
            else:
                self.cur_move = (0, 0)
        self.shot()
        self.move(self.cur_move)


class Bullet(GameObject):
    def __init__(self, board, sprite, speed=0.3, power=1, x=0, y=0, angle=0, bullet_group=GLOBAL.player_bullet_layout):
        super().__init__(board, sprite, GLOBAL.bullet_layout, bullet_group, x=x, y=y, angle=angle)
        self.transform.size = 0.4
        self.speed = speed
        self.power = power
        self.change_sprite_size()
        GLOBAL.event_tick.connect(self.move)
        self.is_boomed = False
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
        if pg.sprite.spritecollideany(self, GLOBAL.wall_layout) and not self.is_boomed:
            self.is_boomed = True
            GLOBAL.shoot_sound.play()
            if pg.sprite.spritecollideany(self, GLOBAL.brick_layout):
                pg.sprite.spritecollideany(self, GLOBAL.brick_layout).kill()
            blocks.Boom(self.board, self.transform.x - 0.5,
                        self.transform.y - 0.5)
            self.disconnect()
            GLOBAL.event_tick.disconnect(self.move)
            self.kill()
        self.event_on_move()
