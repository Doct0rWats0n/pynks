from tank_logic import Tank
from board import Board
from GLOBAL import all_sprites
import pygame as pg
import os
import sys


def load_image(name: str):
    """
    Загрузка изображения
    """
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
    board.set_view(0, 0)
    board.set_size(40)
    tank = Tank(board, load_image("Tank.png"))
    tank1 = Tank(board, load_image("Tank.png"))
    clocker = pg.time.Clock()
    FPS = 60
    playing = True
    is_touch = False
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                is_touch = True
                touch_pos = event.pos
                xy = board.get_cell(event.pos)
                left, top = board.left, board.top
                if xy:
                    tank.transform.set_position(xy[0], xy[1])
                    tank.render()
            if event.type == pg.MOUSEMOTION:
                mpos = event.pos
                if is_touch:
                    r = list(map(lambda x, y: y - x, touch_pos, mpos))
                    board.set_view(left + r[0], top + r[1])
            if event.type == pg.MOUSEBUTTONUP:
                is_touch = False
                touch_pos = event.pos
            if event.type == pg.KEYDOWN:
                board.set_size(board.cell_size + 1)
        # Увеличивает/уменьшает при нажатии и удержании
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_UP]:
            board.set_size(board.get_size() + 1)
        if pressed_keys[pg.K_DOWN]:
            board.set_size(board.get_size() - 1)
        surf.fill("black")
        board.render(surf)
        all_sprites.draw(surf)
        pg.display.flip()
        clocker.tick(FPS)
    pg.quit()
