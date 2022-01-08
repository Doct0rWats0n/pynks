import pygame
from board import Board
import GLOBAL


class Transform:
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"{self.x} {self.y}"


class GameObject(pygame.sprite.Sprite):
    def __init__(self, board, sprite, *sprite_group):
        super().__init__(*sprite_group, GLOBAL.all_sprites)
        self.transform = Transform()
        self.orig_image = sprite
        self.image = sprite
        self.board = board
        self.board.sig_change_size.connect(self.change_sprite_size)
        self.change_sprite_size()
        self.render()

    def change_sprite_size(self):
        self.image = pygame.transform.scale(self.orig_image, (self.board.cell_size, self.board.cell_size))
        self.render()

    def render(self):
        self.rect = self.image.get_rect().move(
            self.board.cell_size * self.transform.x + self.board.left,
            self.board.cell_size * self.transform.y + self.board.top)


class Tank(GameObject):
    def __init__(self, board: Board, sprite, bullet_sprite=None, speed=20,
                 bullet_speed=40, bullet_power=1, health=1):
        super().__init__(board, sprite, GLOBAL.tank_group)
        self.health = health
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power

    def shot(self):
        pass

    def move(self, vector):
        pass

    def rotate(self, angle):
        pass

    def death(self):
        pass

    def taking_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death()


class Bullet(GameObject):
    def __init__(self, board, sprite, speed, power):
        super().__init__(board, sprite, GLOBAL.bullet_group)
        self.speed = speed
        self.power = power
