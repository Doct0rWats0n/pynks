from tank_logic import Tank, BlockWall, Player
from event_system import Event
from board import Board
from GLOBAL import all_sprites
import GLOBAL
import pygame as pg
import os
import sys


class LoadData:
    @staticmethod
    def load_image(name: str):
        """ Загрузка изображения """
        fullname = os.path.join('data/image', name)
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f"Image '{fullname}' not found")
        image = pg.image.load(fullname)
        return image

    @staticmethod
    def load_level():
        return


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(GLOBAL.SIZE)
        self.clock = pg.time.Clock()
        self.FPS = 60

    def run(self):
        pg.init()
        board = Board(8, 6)
        board.set_view(0, 0)
        board.set_size(40)
        tank = Player(board, LoadData.load_image("Tank.png"))
        tank.transform.set_position(0, 0)
        tank.render()
        playing = True
        is_touch = False
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    xy = board.get_cell(event.pos)
                    is_touch = True
                    touch_pos = event.pos
                    left, top = board.left, board.top
                    if xy:
                        b = BlockWall(board, LoadData.load_image("wall.png"))
                        b.transform.set_position(xy[0], xy[1])
                        b.render()
                if event.type == pg.MOUSEMOTION:
                    mpos = event.pos
                    if is_touch:
                        r = list(map(lambda x, y: y - x, touch_pos, mpos))
                        board.set_view(left + r[0], top + r[1])
                if event.type == pg.MOUSEBUTTONUP:
                    is_touch = False
                    touch_pos = event.pos
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_d:
                        tank.rotate(270)
                    if event.key == pg.K_a:
                        tank.rotate(90)
                    if event.key == pg.K_s:
                        tank.rotate(180)
                    if event.key == pg.K_w:
                        tank.rotate(0)
                    if event.key == pg.K_UP:
                        board.set_size(board.get_size() + 10)
                    if event.key == pg.K_DOWN:
                        board.set_size(board.get_size() - 10)
                    if event.key == pg.K_q:
                        board.set_view(-tank.transform.x * board.cell_size + GLOBAL.WIDTH // 2 - board.cell_size // 2,
                                       -tank.transform.y * board.cell_size + GLOBAL.HEIGHT // 2 - board.cell_size // 2)
            tank.movement()
            self.screen.fill("black")
            board.render(self.screen)
            all_sprites.draw(self.screen)
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'{self.clock.get_fps()}')
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
