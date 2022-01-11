from board import Board
import GLOBAL
from base import GameObject


class BlockWall(GameObject):
    def __init__(self, board, sprite):
        super().__init__(board, sprite, GLOBAL.wall_group)


class Tank(GameObject):
    def __init__(self, board: Board, sprite, bullet_sprite=None, speed=0.1,
                 bullet_speed=40, bullet_power=1, health=1):
        super().__init__(board, sprite, GLOBAL.tank_group)
        self.health = health
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power

    def shot(self):
        """ Обработка выстрела """
        pass

    def move(self, vector):
        """ Обработка перемещения """
        self.transform.x += vector[0] * self.speed
        self.transform.y += vector[1] * self.speed
        self.render()

    def rotate(self, angle: float):
        """ Обработка поворота """
        self.transform.set_angle(angle)
        self.change_sprite_size()

    def death(self):
        """ Обработка смерти """
        pass

    def taking_damage(self, damage):
        """ Обработка получения урона """
        self.health -= damage
        if self.health <= 0:
            self.death()


class Bullet(GameObject):
    def __init__(self, board, sprite, speed, power):
        super().__init__(board, sprite, GLOBAL.bullet_group)
        self.speed = speed
        self.power = power
