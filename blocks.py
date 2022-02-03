import pygame as pg
import GLOBAL
import base


class Block(base.GameObject):
    def __init__(self, board, sprite, *layout, x=0, y=0):
        super().__init__(board, sprite, GLOBAL.block_layout, *layout, x=x, y=y)


class AnimatedBlock(base.AnimatedGameObject):
    def __init__(self, board, sprite, *layout, x=0, y=0, animation_speed=20):
        super().__init__(board, sprite, GLOBAL.block_layout, *layout, x=x, y=y, animation_speed=animation_speed)


class UnderBlock(base.GameObject):
    def __init__(self, board, sprite, *layout, x=0, y=0):
        super().__init__(board, sprite, GLOBAL.under_block_layout, *layout, x=x, y=y)


class IndestructibleWall(Block):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.indestructible_wall_sprite, GLOBAL.wall_layout, x=x, y=y)


class Bush(Block):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.bush_sprite, GLOBAL.bush_layout, x=x, y=y)


class Ice(UnderBlock):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.ice_sprite, GLOBAL.ice_layout, x=x, y=y)


class Brick(Block):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.wall_sprite, GLOBAL.wall_layout, GLOBAL.brick_layout, x=x, y=y)


class Base(Block):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.base_sprite, GLOBAL.base_layout, x=x, y=y)
        self.is_defeat = False

    def check_tick(self):
        if pg.sprite.spritecollideany(self, GLOBAL.bullet_layout) and not self.is_defeat:
            self.is_defeat = True
            GLOBAL.event_defeat()
            self.disconnect()
            self.kill()


class RedBarrel(AnimatedBlock):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.barrel_sprite,
                         GLOBAL.barrel_layout, GLOBAL.wall_layout, x=x, y=y, animation_speed=30)
        self.is_boomed = False
        self.explosion = GLOBAL.explosion

    def check_tick(self):
        if pg.sprite.spritecollideany(self, GLOBAL.bullet_layout) and not self.is_boomed:
            self.is_boomed = True
            self.explosion.play()
            Boom(self.board, self.transform.x, self.transform.y)
            self.kill()


class Bonus(AnimatedBlock):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.bonus_speed_sprite, GLOBAL.bonus_layout, x=x, y=y, animation_speed=20)


class Boom(AnimatedBlock):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.boom_sprite, x=x, y=y, animation_speed=5)
        self.is_gone = False

    def check_tick(self):
        if self.is_gone and self.cur_frame == 0:
            self.kill()
            self.disconnect()
        if self.cur_frame == len(self.frames) - 1:
            self.is_gone = True