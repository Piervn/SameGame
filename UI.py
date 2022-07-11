import pygame as pg
from game_constants import *


class GameBoard:
    def __init__(self, owner):
        cells = 10
        top_offset = 300
        center_margin = 60
        if owner == 'player':
            side_offset = CENTER_X - (CELL_SIZE * cells) - center_margin - (cells * MARGIN)
        elif owner == 'ai':
            side_offset = CENTER_X + center_margin
        grid = []
        for y in range(cells):
            row = []
            for x in range(cells):
                row.append([side_offset + (x * (CELL_SIZE + MARGIN)), y * (CELL_SIZE + MARGIN) + top_offset])
            grid.append(row)
        self.GRID = grid
        
    def __iter__(self):
        return iter(self.GRID)


class GameWindow:
    def __init__(self):
        self.WIN = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("SameGame")
        self.game_loop()
        
    def game_loop(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.draw_window()
        quit()
        
    def draw_window(self):
        self.WIN.fill(BG_COLOR)
        self.draw_board('player')
        self.draw_board('ai')
        pg.display.update()
        
    def draw_board(self, owner):
        board = GameBoard(owner)
        for row in board:
            for x, y in row:
                pg.draw.rect(self.WIN, CELL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
        
        
    


if __name__ == '__main__':
    game = GameWindow()