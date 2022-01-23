from pygame.sprite import Group
from loaddata import LoadData

SIZE = WIDTH, HEIGHT = (800, 600)

all_sprites = Group()
tank_layout = Group()
bullet_layout = Group()
wall_layout = Group()
block_layout = Group()
bush_layout = Group()
under_block_layout = Group()
ice_layout = Group()

ui_layout = Group()


indestructible_wall_sprite = LoadData.load_image("block_wall.png")
bush_sprite = LoadData.load_image("kust.png")
ice_sprite = LoadData.load_image("water.png")
wall_sprite = LoadData.load_image("wall.png")


MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 100
