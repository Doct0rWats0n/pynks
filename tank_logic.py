import pygame
from sprite_groups import all_sprites, tank_group


class Tank(pygame.sprite.Sprite):
    def __init__(self, board, sprite, bullet_sprite, speed,
                 bullet_speed, bullet_power, health):
        super().__init__(tank_group, all_sprites)
        self.board = board
        self.health = health
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.sprite = sprite
        self.bullet_sprite = bullet_sprite
        self.bullet_power = bullet_power

    def render(self):
        pass

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
