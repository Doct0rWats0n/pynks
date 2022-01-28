from pygame.sprite import Group
from loaddata import LoadData

SIZE = WIDTH, HEIGHT = (800, 600)

all_sprites = Group()
animated_layout = Group()
tank_layout = Group()
bullet_layout = Group()
wall_layout = Group()
block_layout = Group()
bush_layout = Group()
under_block_layout = Group()
ice_layout = Group()
base_layout = Group()
barrel_layout = Group()

ui_layout = Group()


indestructible_wall_sprite = LoadData.load_image("block_wall.png")
bush_sprite = LoadData.load_image("kust.png")
ice_sprite = LoadData.load_image("water.png")
wall_sprite = LoadData.load_image("wall.png")
base_sprite = LoadData.load_image("baseUK.png")
barrel_sprite = LoadData.load_sheet("red_barrel_sheet.png", columns=2)


MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 100
