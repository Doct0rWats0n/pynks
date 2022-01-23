from tank_logic import Player
from board import Board
import GLOBAL
import pygame as pg
from loaddata import LoadData


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
        LoadData.load_level(board, "map1.txt")
        tank = Player(board, LoadData.load_image("Tank.png"), x=3, y=1)
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
                if event.type == pg.MOUSEMOTION:
                    mpos = event.pos
                    if is_touch:
                        r = list(map(lambda x, y: y - x, touch_pos, mpos))
                        board.set_view(left + r[0], top + r[1])
                if event.type == pg.MOUSEBUTTONUP:
                    is_touch = False
                    touch_pos = event.pos
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        tank.shot()
                    if event.key == pg.K_d:
                        tank.transform.set_angle(270)
                    if event.key == pg.K_a:
                        tank.transform.set_angle(90)
                    if event.key == pg.K_s:
                        tank.transform.set_angle(180)
                    if event.key == pg.K_w:
                        tank.transform.set_angle(0)
                    if event.key == pg.K_UP:
                        board.set_size(board.get_size() + 10)
                    if event.key == pg.K_DOWN:
                        board.set_size(board.get_size() - 10)
                    if event.key == pg.K_q:
                        board.set_view(-tank.transform.x * board.cell_size + GLOBAL.WIDTH // 2 - board.cell_size // 2,
                                       -tank.transform.y * board.cell_size + GLOBAL.HEIGHT // 2 - board.cell_size // 2)
            tank.movement()
            self.screen.fill("black")
            #board.render(self.screen)
            GLOBAL.under_block_layout.draw(self.screen)
            GLOBAL.tank_layout.draw(self.screen)
            for i in GLOBAL.bullet_layout:
                i.move()
            GLOBAL.bullet_layout.draw(self.screen)
            GLOBAL.block_layout.draw(self.screen)
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'{self.clock.get_fps()}')
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
