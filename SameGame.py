from util import Pos
from copy import deepcopy
from random import randint, choice

test = [\
[0,  0,  3,  3,  3,  0],
[1,  4,  2,  3,  2,  2],
[3,  4,  0,  1,  1,  4],
[0,  2,  3,  4,  0,  3],
[4,  1,  3,  3,  4,  3],
[0,  0,  4,  4,  2,  3]]


class SameGame:
    def __init__(self, size):
        self.size = size
        self.board = [[randint(0, 4) for _ in range(size)] for _ in range(size)] # losowa plansza
        self.score = 0
        self.moves = 0
        self.directions = [Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0)] # up, right, down, left
        self.score = 0
        self.game_over = False
        self.number_of_moves = 0
    
    def __getitem__(self, pos):
        return self.board[self.size - pos[1] - 1][pos[0]]
    
    def __setitem__(self, pos, value):
        self.board[self.size - pos[1] - 1][pos[0]] = value
    
    def __str__(self):
        result = ''
        for i in range(self.size):
            result += f'{str(self.size - i - 1): >2} |'
            for j in range(self.size):
                if self.board[i][j] == -1:
                    result += '   '
                else:
                    result += f'{str(self.board[i][j]): >2}' + ' '
            result += '\n'
        result += '    ' + '-'*(self.size*3) + '\n'
        result += '     '
        for i in range(self.size):
            result += f'{str(i): <2}' + ' '
        return result
        
    def __hash__(self) -> int:
        return hash(self.board)
        
    def valid_move(self, pos):
        color = self[pos]
        for d in self.directions:
            if 0 <= (pos + d).x < self.size and 0 <= (pos + d).y < self.size:
                if self[pos + d] == color:
                    return True
        return False
    
    def get_moves(self):
        cboard = deepcopy(self.board)
        moves = {0: [], 1: [], 2: [], 3: [], 4: []}
        for y in range(self.size):
            for x in range(self.size):
                row = self.size - y - 1
                color = cboard[row][x]
                # print(f'{x} {self.size - y - 1} = {self.board[y][x]}')
                if color != -1:
                    if self.valid_move(Pos(x, y)):
                        tiles = []
                        self.get_tiles(cboard, tiles, Pos(x, y), color)
                        moves[color].append(tiles)
                    else:
                        cboard[row][x] = -1
        return moves
    
    def get_tiles(self, cboard, tiles, pos, color):
        i = self.size - pos[1] - 1
        j = pos[0]
        if cboard[i][j] == -1:
            return
        if cboard[i][j] == color:
            tiles.append(pos)
            cboard[i][j] = -1
            for d in self.directions:
                if 0 <= (pos + d).x < self.size and 0 <= (pos + d).y < self.size:
                    self.get_tiles(cboard, tiles, pos + d, color)
                    
    def remove_tiles(self, tiles):
        columns = set([x[0] for x in tiles])
        for tile in tiles:
            self[tile] = -1
        
        for column in columns:
            for i in range(self.size):
                if self[Pos(column, i)] != -1:
                    for j in range(i, 0, -1):
                        if self[Pos(column, j - 1)] == -1:
                            self[Pos(column, j - 1)] = self[Pos(column, j)]
                            self[Pos(column, j)] = -1
                        else:
                            break
                        
    def remove_empty_columns(self):
        first_row = self.board[self.size - 1]
        if -1 not in first_row:
            return
        transpose = list(map(list, zip(*self.board)))
        
        j = 0
        k = self.size
        while j < k:
            if first_row[j] == -1:
                del first_row[j]
                first_row.append(-1)
                del transpose[j]
                transpose.append([-1] * self.size)
                k -= 1
            else:
                j += 1
                
                
        self.board = list(map(list, zip(*transpose)))
                         
    def move(self, pos): # zakładam że pos jest poprawnym ruchem
        if pos is None:
            return
        color = self[pos]
        for set in self.get_moves()[color]:
            if pos in set:
                tiles_to_remove = set
                break
        self.remove_tiles(tiles_to_remove)
        self.remove_empty_columns()
        self.number_of_moves += 1
        self.score += (len(tiles_to_remove) - 2) ** 2
        if self.board[self.size - 1][0] == -1:
            self.game_over = True
            self.score += 1000
    
    def random_move(self):
        moves = self.get_moves()
        if self.is_game_over(moves):
            self.game_over = True
            return
        possible_colors = [x for x in range(5) if moves[x]]
        color = choice(possible_colors)
        region = choice(moves[color])
        self.remove_tiles(region)
        self.remove_empty_columns()
        self.number_of_moves += 1
        self.score += (len(region) - 2) ** 2
        if self.board[self.size - 1][0] == -1:
                self.score += 1000
    
    def is_game_over(self, moves):
        return not any(moves.values())
    
    def real_play(self):
        while True:
            print()
            print(self)
            print(f'Score: {self.score}')
            print(f'Moves: {self.number_of_moves}')
            moves = self.get_moves()
            if self.is_game_over(moves):
                print('Game over!')
                break
            for key in moves:
                print(f'{key}: {self.get_moves()[key]}')
            x, y = map(int, input('Podaj współrzędne: ').split())
            self.move(Pos(x, y))
        

if __name__ == '__main__':
    game = SameGame(6)
    game.real_play()

