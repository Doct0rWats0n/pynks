import pygame as pg


class Board:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.board = [[0] * width for _ in range(height)]
        self.left, self.top = 10, 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left, self.top = left, top
        self.cell_size = cell_size

    def render(self, screen: pg.Surface):
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                       self.cell_size, self.cell_size), width=1)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.width * self.cell_size + self.left and \
                self.top <= mouse_pos[1] <= self.height * self.cell_size + self.top:
            return (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size


if __name__ == '__main__':
    SIZE = WIDTH, HEIGHT = (800, 600)
    surf = pg.display.set_mode(SIZE)
    pg.display.set_caption('Инициализация игры')

    board = Board(4, 3)
    board.set_view(100, 100, 50)
    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(board.get_cell(event.pos))
        board.render(surf)
        pg.display.flip()
    pg.quit()

