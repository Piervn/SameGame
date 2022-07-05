from SameGame import SameGame
from math import sqrt, log
from copy import deepcopy
from random import choice
from util import Pos
from tqdm import tqdm
from time import time

c = sqrt(2)

class Node:
    def __init__(self, game: SameGame, parent=None):
        self.game = game
        self.parent = parent
        self.children = {}
        self.best_score = 0
        self.sum_of_scores = 0
        self.games = 0
        self.expanded = False
        
    def get_avg_score(self):
        if self.games == 0:
            return 0
        return self.sum_of_scores / self.games

    def get_UCB(self, root):
        return self.best_score + c * sqrt(log(root.games) / (self.games + 1))
    
    def expand(self):
        assert not self.expanded
        moves = self.game.get_moves()
        if any(k != [] for k in moves.values()):
            for color, moves in moves.items():
                for move in moves:
                    game_copy = deepcopy(self.game)
                    game_copy.move(move[0])
                    self.children[move[0]] = Node(game_copy, self)
        else:
            self.children = None
            self.game.game_over = True
        self.expanded = True
    
    def update(self, score):
        current = self
        while current is not None:
            if score > current.best_score:
                current.best_score = score
            current.sum_of_scores += score
            current.games += 1
            current = current.parent
        
    def simulate(self):
        simulated_game = deepcopy(self.game)
        while not simulated_game.game_over:
            simulated_game.random_move()
        return simulated_game.score
    

class MCTS:
    def __init__(self, game: SameGame):
        self.root = Node(game, None)
        
    def select(self):
        selected = self.root
        while selected.expanded:
            if selected.children is None:
                return False
            if all(n.expanded for n in selected.children.values()):
                selected = max(selected.children.values(), key=lambda x: x.get_UCB(self.root))
            else:
                selected = choice([n for n in selected.children.values() if not n.expanded])
        return selected
            
    def run(self, iterations):
        for _ in range(iterations):
            selected = self.select()
            if not selected:
                continue
            selected.expand()
            score = selected.simulate()
            selected.update(score)
    
    def get_move(self):
        if not self.root.children:
            return None
        return max(self.root.children, key=lambda k: self.root.children[k].games)
    
    def make_move(self, move):
        self.root = self.root.children[move]
    
        
def main(game: SameGame, iterations, verbose=False):
    mcts = MCTS(game)
    print(f'\nStart board:\n{game}')
    print('\nMoves:')
    #list_of_moves = []
    while True:
        if verbose:
            moves = game.get_moves()
            print('\nAvailable moves:')
            for color in range(5):
                print(f'{color}: ', end='')
                for move in moves[color]:
                    print(f'{move[0]} ', end='')
                print()
        mcts.run(iterations)
        move = mcts.get_move()
        if game.game_over or move == None:
            print(f'\nGame over!\nEnd board:\n{game}')
            break
        game.move(move)
        mcts.make_move(move)
        #list_of_moves.append(move)
        print(move)
        if verbose:
            print(f'Score: {game.score}')
            print(f'\n{game}')

    print('\nFinal score:', game.score)
    #return list_of_moves
        
if __name__ == '__main__':
    start = time()
    game = SameGame(15)
    sgame = deepcopy(game)
    #mcts = MCTS(game)
    #mcts.run(1000)
    #print(f'\nFinal score: {mcts.root.best_score}')
    main(game, 50)
    end = time()
    t = end - start
    print(f'\nTime: {t: .2f} s')
    # for move in moves:
    #     sgame.move(move)
    # print(f'\nFinal board:\n{sgame}')
    # print(f'\nFinal score: {sgame.score}')
    