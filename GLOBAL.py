from pygame.sprite import Group
import pygame
from loaddata import LoadData
from event_system import Event
from PIL import Image

SIZE = WIDTH, HEIGHT = (800, 600)

all_sprites = Group()
animated_layout = Group()
tank_layout = Group()
bullet_layout = Group()
enemy_bullet_layout = Group()
player_bullet_layout = Group()
wall_layout = Group()
block_layout = Group()
bush_layout = Group()
under_block_layout = Group()
ice_layout = Group()
base_layout = Group()
barrel_layout = Group()
ui_layout = Group()
collide_layout = Group()

player_sprite = LoadData.load_image("Tank.png")
bullet_sprite = LoadData.load_image("bullet.png")
indestructible_wall_sprite = LoadData.load_image("block_wall.png")
bush_sprite = LoadData.load_image("kust.png")
ice_sprite = LoadData.load_image("water.png")
wall_sprite = LoadData.load_image("wall.png")
base_sprite = LoadData.load_image("baseUK.png")
barrel_sprite = LoadData.load_sheet("red_barrel_sheet.png", columns=2)
boom_sprite = LoadData.load_sheet("boom_sheet.png", columns=3)

hit_sound = LoadData.load_sound("tank_hit.wav")
shoot_sound = LoadData.load_sound("bullet.wav")
explosion = LoadData.load_sound("explosion.wav")

event_defeat = Event()
event_tick = Event()
event_change_size = Event()
event_change_view = Event()

MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 100

im = Image.new(mode='RGB', size=(1, 1))
collide_sprite = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
