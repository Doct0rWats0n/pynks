import tank_logic
from board import Board
import sprite_groups
import pygame as pg


if __name__ == '__main__':
    SIZE = WIDTH, HEIGHT = (800, 600)
    surf = pg.display.set_mode(SIZE)
    pg.display.set_caption('Инициализация игры')

    board = Board(4, 3)
    board.set_view(100, 100, 50)
    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(board.get_cell(event.pos))
        board.render(surf)
        pg.display.flip()
    pg.quit()
