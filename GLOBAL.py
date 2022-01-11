from pygame.sprite import Group

SIZE = WIDTH, HEIGHT = (800, 600)

all_sprites = Group()
tank_group = Group()
bullet_group = Group()
wall_group = Group()
grass_group = Group()

MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 100
