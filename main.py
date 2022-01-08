from tank_logic import Tank
from board import Board
from GLOBAL import all_sprites
import pygame as pg
import os
import sys


def load_image(name):
    fullname = os.path.join('data/image', name)
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Image '{fullname}' not found")
    image = pg.image.load(fullname)
    return image


if __name__ == '__main__':
    SIZE = WIDTH, HEIGHT = (800, 600)
    surf = pg.display.set_mode(SIZE)
    pg.display.set_caption('Инициализация игры')

    board = Board(8, 6)
    board.set_view(0, 0, 20)
    tank = Tank(board, load_image("Tank.png"))
    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                xy = board.get_cell(event.pos)
                tank.transform.set_position(xy[0], xy[1])
                tank.render()
            if event.type == pg.KEYDOWN:
                board.set_view(board.left, board.top, board.cell_size + 1)

        surf.fill("black")
        all_sprites.draw(surf)
        board.render(surf)
        pg.display.flip()
    pg.quit()
