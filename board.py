import pygame as pg
from signal_slot_system import Signal


class Board:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.board = [[0] * width for _ in range(height)]
        self.left, self.top = 10, 10
        self.cell_size = 30
        self.sig_change_size = Signal()
        self.sig_change_view = Signal()

    def set_size(self, cell_size):
        self.cell_size = cell_size
        self.sig_change_size()

    def set_view(self, left, top):
        self.left = left
        self.top = top
        self.sig_change_view()

    def render(self, screen: pg.Surface):
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                       self.cell_size, self.cell_size), width=1)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.width * self.cell_size + self.left and \
                self.top <= mouse_pos[1] <= self.height * self.cell_size + self.top:
            return (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
