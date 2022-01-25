import GLOBAL
import base


class Block(base.GameObject):
    def __init__(self, board, sprite, *layout, x=0, y=0):
        super().__init__(board, sprite, GLOBAL.block_layout, *layout, x=x, y=y)


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
        super().__init__(board, GLOBAL.wall_sprite, GLOBAL.wall_layout, x=x, y=y)


class Base(Block):
    def __init__(self, board, x=0, y=0):
        super().__init__(board, GLOBAL.base_sprite, GLOBAL.base_layout, x=x, y=y)
