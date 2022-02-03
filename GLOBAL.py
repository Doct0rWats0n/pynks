from pygame.sprite import Group
import pygame
from loaddata import LoadData
from event_system import Event
from PIL import Image

SIZE = WIDTH, HEIGHT = [800, 600]

all_sprites = Group()
animated_layout = Group()
tank_layout = Group()
bullet_layout = Group()
enemy_bullet_layout = Group()
player_bullet_layout = Group()
wall_layout = Group()
block_layout = Group()
bush_layout = Group()
brick_layout = Group()
under_block_layout = Group()
ice_layout = Group()
base_layout = Group()
barrel_layout = Group()
ui_layout = Group()
menu_ui_layout = Group()
game_ui_layout = Group()
collide_layout = Group()

ALL_GROUPS = [all_sprites,
              animated_layout,
              tank_layout,
              bullet_layout,
              enemy_bullet_layout,
              player_bullet_layout,
              wall_layout,
              block_layout,
              bush_layout,
              brick_layout,
              under_block_layout,
              ice_layout,
              base_layout,
              barrel_layout,
              ui_layout,
              game_ui_layout,
              collide_layout]

player_sprite = LoadData.load_image("Tank.png")
enemy_sprite = LoadData.load_image("enemy.png")
bullet_sprite = LoadData.load_image("bullet.png")
indestructible_wall_sprite = LoadData.load_image("block_wall.png")
bush_sprite = LoadData.load_image("kust.png")
ice_sprite = LoadData.load_image("water.png")
wall_sprite = LoadData.load_image("wall.png")
base_sprite = LoadData.load_image("baseRU.png")
game_over_sprite = LoadData.load_image('gameover.png')
barrel_sprite = LoadData.load_sheet("red_barrel_sheet.png", columns=2)
boom_sprite = LoadData.load_sheet("boom_sheet.png", columns=3)

hit_sound = LoadData.load_sound("tank_hit.wav")
shoot_sound = LoadData.load_sound("bullet.wav")
explosion = LoadData.load_sound("explosion.wav")
bip = LoadData.load_sound('bip.wav')
win_sound = LoadData.load_sound('win.wav')

event_defeat = Event()
event_tick = Event()
event_change_size = Event()
event_change_view = Event()
event_window_resize = Event()
event_click = Event()
event_hold = Event()
event_move = Event()
event_kill = Event()

MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 100
OPEN_CELLS = ['.', '"', 'B', 'T', 'X', '~']

im = Image.new(mode='1', size=(1, 1))
collide_sprite = pygame.image.fromstring(im.tobytes(), im.size, 'P')
