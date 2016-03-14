import math
import random
import sys
import hashlib

from board import *

def human_move(board):
    while True:
        try:
            move = raw_input('> Choose your move: ')
            if move == "q":
                sys.exit(0)
            return board.player_move('O', int(move))
        except InvalidColumnException:
            print "Invalid column"
        except ColumnFullException:
            print "Column full"
        except ValueError:
            print "Try again"

def main():
    print '{{ === ConnectFML === }}'

    human_name = raw_input('> Hello human, what is your name? ')
    print '= Nice to meet you, %s, good luck!' % human_name

    game = Game()
    board = Board(num_rows = 6, num_columns = 7, required_to_win = 4, players=['X', 'O'])
    turn = 'computer'

    print board

    while not board.status.is_over:
        if turn == 'human':
            print
            board = human_move(board)
            turn = 'computer'
        else:
            print
            print '= The computer is thinking...',
            sys.stdout.flush()

            decision = minimax_decision(game, board, 5)
            board = board.player_move('X', decision)

            print ' Computer plays %d' % decision
            turn = 'human'

        print board

    if board.status.is_win:
        print 'Winner is: %s' % board.status.winner
    else:
        print 'Draw'

UTILITY_CACHE = {}

class Game(object):
    def successors(self, board, player):
        return [(move, self.make_move(player, move, board))
                for move in self.legal_moves(board)]

    def make_move(self, player, move, board):
        return board.player_move(player, move)

    def legal_moves(self, board):
        return board.valid_moves

    def utility(self, board):
        key = hashlib.md5(board.__str__())
        value = UTILITY_CACHE.get(key)

        if value:
            return value
        else:
            status = board.status
            result = 0

            if status.is_win:
                if status.winner == 'X':
                    return 10000
                else:
                    return -10000

            result += board.match_subset('X', board.required_to_win - 1) * 100
            result -= board.match_subset('O', board.required_to_win - 1) * 100

            UTILITY_CACHE[key] = result

            return result

    def terminal_test(self, board):
        status = board.status
        return status.is_over

INFINITY = 100000

def max_value(game, board, alpha, beta, depth, max_depth):
    if game.terminal_test(board) or depth >= max_depth:
        return game.utility(board)

    v = -INFINITY
    for (a, s) in game.successors(board, 'X'):
        v = max(v, min_value(game, s, alpha, beta, depth + 1, max_depth))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(game, board, alpha, beta, depth, max_depth):
    if game.terminal_test(board) or depth >= max_depth:
        return game.utility(board)

    v = INFINITY
    for (a, s) in game.successors(board, 'O'):
        v = min(v, max_value(game, s, alpha, beta, depth + 1, max_depth))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def minimax_decision(game, board, max_depth):
    values = [ (min_value(game, next_board, -INFINITY, INFINITY, 0, max_depth), move)
              for (move, next_board) in game.successors(board, 'X') ]

    print values

    best_score, best_move = max(values)
    return random.choice([move for (score, move) in values if score == best_score])

if __name__ == '__main__':
    main()
