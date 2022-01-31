import ui
from tank_logic import Player, Tank
from board import Board
import GLOBAL
import pygame as pg
from loaddata import LoadData

pg.init()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(GLOBAL.SIZE, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.board = Board(0, 0)
        self.board.set_view(0, 0)
        self.board.set_size(40)
        self.is_touch = False
        self.touch_pos = (0, 0)
        self.left = 0
        self.top = 0
        self.is_dead = False
        GLOBAL.event_defeat.connect(self.game_over_screen)

    def game_over_screen(self):
        ui.Image(GLOBAL.game_over_sprite, GLOBAL.game_ui_layout,center=True)
        self.is_dead = True

    def draw_layouts(self):
        self.screen.fill("black")
        GLOBAL.under_block_layout.draw(self.screen)
        GLOBAL.tank_layout.draw(self.screen)
        GLOBAL.bullet_layout.draw(self.screen)
        GLOBAL.block_layout.draw(self.screen)
        GLOBAL.game_ui_layout.draw(self.screen)

    def clear_groups(self):
        for group in GLOBAL.ALL_GROUPS:
            group.empty()

    def movement(self, tank):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.WINDOWRESIZED:
                GLOBAL.SIZE = self.screen.get_size()
                GLOBAL.event_window_resize()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.is_dead:
                    self.is_dead = False
                    return False
                self.is_touch = True
                self.touch_pos = event.pos
                self.left, self.top = self.board.left, self.board.top
            if event.type == pg.MOUSEMOTION:
                mpos = event.pos
                if self.is_touch:
                    r = list(map(lambda x, y: y - x, self.touch_pos, mpos))
                    self.board.set_view(self.left + r[0], self.top + r[1])
            if event.type == pg.MOUSEBUTTONUP:
                self.is_touch = False
                self.touch_pos = event.pos
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    tank.transform.set_angle(270)
                if event.key == pg.K_a:
                    tank.transform.set_angle(90)
                if event.key == pg.K_s:
                    tank.transform.set_angle(180)
                if event.key == pg.K_w:
                    tank.transform.set_angle(0)
                if event.key == pg.K_UP:
                    self.board.set_size(self.board.get_size() + 10)
                if event.key == pg.K_DOWN:
                    self.board.set_size(self.board.get_size() - 10)
                if event.key == pg.K_q:
                    self.board.set_view(
                        -tank.transform.x * self.board.cell_size + GLOBAL.WIDTH // 2 - self.board.cell_size // 2,
                        -tank.transform.y * self.board.cell_size + GLOBAL.HEIGHT // 2 - self.board.cell_size // 2)
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_m]:
            tank.shot()
        tank.movement()
        return True

    def run_map(self, map):
        LoadData.load_level(self.board, map)
        tank = Player(self.board, x=3, y=1)
        playing = True
        while playing:
            playing = self.movement(tank)
            self.draw_layouts()
            GLOBAL.event_tick()
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'{self.clock.get_fps()}')
        self.clear_groups()

    def run_menu(self):
        but1 = ui.Button(GLOBAL.indestructible_wall_sprite, GLOBAL.menu_ui_layout,
                         x=0, y=-100, center=True, func=lambda: self.run_map("map1.txt"))
        but2 = ui.Button(GLOBAL.indestructible_wall_sprite, GLOBAL.menu_ui_layout,
                         x=0, y=0, center=True, func=lambda: self.run_map("map2.txt"))
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    GLOBAL.event_click(event.pos)
                if event.type == pg.WINDOWRESIZED:
                    GLOBAL.SIZE = self.screen.get_size()
                    GLOBAL.event_window_resize()
            self.screen.fill('blue')
            GLOBAL.menu_ui_layout.draw(self.screen)
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'{self.clock.get_fps()}')
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run_menu()
