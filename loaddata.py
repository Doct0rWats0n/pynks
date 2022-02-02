import os
import pygame as pg
import pygame.image
import blocks
from PIL import Image
pg.init()


class LoadData:
    @staticmethod
    def load_image(file_name: str):
        """ Загрузка изображения """
        full_name = os.path.join('data/image', file_name)
        if not os.path.isfile(full_name):
            raise FileNotFoundError(f"Image '{full_name}' not found")
        return pg.image.load(full_name)

    @staticmethod
    def load_sheet(file_name: str, columns=1, rows=1):
        full_name = os.path.join('data/image', file_name)
        if not os.path.isfile(full_name):
            raise FileNotFoundError(f"Image '{full_name}' not found")
        sheet = Image.open(full_name)
        width, height = sheet.size
        width //= columns
        height //= rows
        images = []
        for r in range(rows):
            for c in range(columns):
                im = sheet.crop((width * c, height * r,
                                 width * c + width, height * r + height))
                images.append(pygame.image.fromstring(im.tobytes(), im.size, im.mode))
        return images

    @staticmethod
    def load_level(board, file_name):
        spwn_points = []
        spwm_pl = None
        full_name = os.path.join('data/map', file_name)
        if not os.path.isfile(full_name):
            raise FileNotFoundError(f"Map '{full_name}' not found")
        with open(full_name, mode='r') as file:
            map = [[j for j in i] for i in file.readlines()]
        for ind_y, data in enumerate(map):
            for ind_x, block in enumerate(data):
                if block == '#':
                    blocks.IndestructibleWall(board, x=ind_x, y=ind_y)
                elif block == 'B':
                    blocks.Brick(board, x=ind_x, y=ind_y)
                elif block == '~':
                    blocks.Ice(board, x=ind_x, y=ind_y)
                elif block == '"':
                    blocks.Bush(board, x=ind_x, y=ind_y)
                elif block == 'X':
                    blocks.Base(board, x=ind_x, y=ind_y)
                elif block == 'R':
                    blocks.RedBarrel(board, x=ind_x, y=ind_y)
                elif block == 'T':
                    spwn_points.append([ind_x, ind_y])
                elif block == 'P':
                    spwm_pl = ind_x, ind_y
        return spwn_points, spwm_pl


    @staticmethod
    def load_sound(file_name):
        full_name = os.path.join('data/sound', file_name)
        if not os.path.isfile(full_name):
            raise FileNotFoundError(f"Sound '{full_name}' not found")
        return pg.mixer.Sound(full_name)

    @staticmethod
    def load_font(file_name, size=30):
        full_name = os.path.join('data/font', file_name)
        if not os.path.isfile(full_name):
            raise FileNotFoundError(f"Font '{full_name}' not found")
        return pygame.font.Font(full_name, size)
