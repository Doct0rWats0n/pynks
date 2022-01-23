import os
import pygame as pg
import blocks


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
    def load_level(board, file_name):
        full_name = os.path.join('data/map', file_name)
        with open(full_name, mode='r') as file:
            map = [[j for j in i] for i in file.readlines()]
        for ind_y, data in enumerate(map):
            for ind_x, block in enumerate(data):
                if block == '#':
                    blocks.IndestructibleWall(board, x=ind_x, y=ind_y)
                elif block == 'B':
                    blocks.Block(board, LoadData.load_image("wall.png"), x=ind_x, y=ind_y)
                elif block == '~':
                    blocks.Ice(board, x=ind_x, y=ind_y)
                elif block == '"':
                    blocks.Bush(board, x=ind_x, y=ind_y)
