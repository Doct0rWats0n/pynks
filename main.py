import random
import ui
from tank_logic import Player, Enemy
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
        self.tick = 0
        self.spawn_speed = 10
        self.max_enemies = 10
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.map = ''
        self.playing = True
        self.full_screen = False
        GLOBAL.event_tick.connect(self.spawn_tanks)
        GLOBAL.event_defeat.connect(self.game_over_screen)
        GLOBAL.event_kill.connect(self.add_killed)
        GLOBAL.event_win.connect(self.win)

    def add_killed(self):
        self.killed_enemies += 1
        if self.killed_enemies == self.max_enemies:
            GLOBAL.event_win()

    def terminate(self):
        self.playing = False

    def win(self):
        ui.Image(GLOBAL.win_sprite, GLOBAL.game_ui_layout, center=True, text=f'{self.killed_enemies}')
        ui.Button(GLOBAL.next_button_sprite, GLOBAL.game_ui_layout, center=True, y=-100, func=lambda: self.terminate(),
                  scene=self.map)
        GLOBAL.win_sound.play()

    def game_over_screen(self):
        ui.Image(GLOBAL.game_over_sprite, GLOBAL.game_ui_layout, center=True)
        self.is_dead = True

    def spawn_tanks(self):
        self.tick = (self.tick + 1) % self.spawn_speed
        if self.tick == 0 and self.spawned_enemies < self.max_enemies:
            spwn = random.choice(self.spawn_points)
            Enemy(self.board, self.last_x, self.last_y, self.last_map, x=spwn[0], y=spwn[1])
            self.spawned_enemies += 1

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
                GLOBAL.event_hold(event.pos, self.map)
                if self.is_dead:
                    self.is_dead = False
                    return False
                self.is_touch = True
                self.touch_pos = event.pos
                self.left, self.top = self.board.left, self.board.top
            if event.type == pg.MOUSEMOTION:
                GLOBAL.event_move(event.pos, self.map)
                mpos = event.pos
                if self.is_touch:
                    r = list(map(lambda x, y: y - x, self.touch_pos, mpos))
                    self.board.set_view(self.left + r[0], self.top + r[1])
            if event.type == pg.MOUSEBUTTONUP:
                GLOBAL.event_click(event.pos, self.map)
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
                        -tank.transform.x * self.board.cell_size + GLOBAL.SIZE[0] // 2 - self.board.cell_size // 2,
                        -tank.transform.y * self.board.cell_size + GLOBAL.SIZE[1] // 2 - self.board.cell_size // 2)
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_m]:
            tank.shot()
        tank.movement()
        return True

    def run_map(self, mp):
        self.map = mp
        self.tick = 0
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.spawn_points, (x, y), self.last_x, self.last_y, self.last_map = LoadData.load_level(self.board, mp)
        tank = Player(self.board, x=x, y=y)
        self.playing = True
        playing = True
        while playing:
            playing = self.movement(tank)
            if not self.playing:
                playing = False
            self.draw_layouts()
            GLOBAL.event_tick()
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'{self.clock.get_fps()}')
        self.clear_groups()

    def on_off_full(self):
        self.full_screen = not self.full_screen
        if not self.full_screen:
            self.screen = pg.display.set_mode(GLOBAL.SMALL_SIZE, pg.RESIZABLE)
            GLOBAL.SIZE = GLOBAL.SMALL_SIZE
            GLOBAL.event_window_resize()
        else:
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.RESIZABLE)
            GLOBAL.SIZE = self.screen.get_size()
            GLOBAL.event_window_resize()

    def run_menu(self):
        def close_menu():
            self.running = False

        tank = ui.Image(GLOBAL.player_sprite, GLOBAL.menu_ui_layout, x=100, y=-100, center=True, angle=90, size=3)
        but1 = ui.Button([GLOBAL.indestructible_wall_sprite,
                          GLOBAL.wall_sprite,
                          GLOBAL.ice_sprite], GLOBAL.menu_ui_layout,
                         x=0, y=-100, center=True, func=lambda: self.run_map("map1.txt"))
        but1.on_touch.connect(lambda: tank.transform.set_position(100, -100))
        but2 = ui.Button([GLOBAL.indestructible_wall_sprite,
                          GLOBAL.wall_sprite,
                          GLOBAL.ice_sprite], GLOBAL.menu_ui_layout,
                         x=0, y=0, center=True, func=lambda: self.run_map("map3.txt"))
        but2.on_touch.connect(lambda: tank.transform.set_position(100, 0))
        but3 = ui.Button([GLOBAL.indestructible_wall_sprite,
                          GLOBAL.wall_sprite,
                          GLOBAL.ice_sprite], GLOBAL.menu_ui_layout,
                         x=0, y=100, center=True, func=close_menu)
        but3.on_touch.connect(lambda: tank.transform.set_position(100, 100))
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    GLOBAL.event_hold(event.pos, 'main')
                if event.type == pg.MOUSEBUTTONUP:
                    GLOBAL.event_click(event.pos, 'main')
                if event.type == pg.MOUSEMOTION:
                    GLOBAL.event_move(event.pos, 'main')
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
