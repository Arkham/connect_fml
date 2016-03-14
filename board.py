import copy
from itertools import chain, groupby, permutations

class cached_property(object):
    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)
        return attr

EMPTY = '.'

class InvalidColumnException(Exception):
    pass

class InvalidPlayerException(Exception):
    pass

class ColumnFullException(Exception):
    pass

class BoardStatus(object):
    def __init__(self, board, is_over = False, is_win = False, is_draw = False, winner = None):
        self.board = board
        self.is_over = is_over
        self.is_win = is_win
        self.is_draw = is_draw
        self.winner = winner

class Board(object):
    def __init__(self, matrix = None, num_columns = 7, num_rows = 6, required_to_win = 4, players = ['R', 'Y']):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.required_to_win = required_to_win
        self.players = players
        self.matrix = matrix or [[EMPTY] * num_columns for _ in range(num_rows)]

    @property
    def rows(self):
        return self.matrix

    @cached_property
    def columns(self):
        return [list(tuple) for tuple in zip(*self.rows)]

    @cached_property
    def diagonal_indexes(self):
        h = self.num_rows
        w = self.num_columns
        return [[ (p, q) for q in range(min(p, h-1), max(0, p-w+1)-1, -1) ]
            for p in range(h+w-1)]

    @cached_property
    def positive_diagonals(self):
        return [[ self.rows[q][p-q] for (p, q) in diagonal ]
            for diagonal in self.diagonal_indexes]

    @cached_property
    def negative_diagonals(self):
        h = self.num_rows
        return [[ self.rows[h-1-q][p-q] for (p, q) in diagonal ]
            for diagonal in self.diagonal_indexes]

    @cached_property
    def is_empty(self):
        return all(cell == EMPTY for cell in self.rows[0])

    @cached_property
    def is_full(self):
        return all(cell != EMPTY for cell in self.rows[-1])

    @cached_property
    def valid_moves(self):
        return [ index for index in range(self.num_columns) if self.columns[index][-1] == EMPTY]

    def clone(self):
        return Board(
            num_columns = self.num_columns,
            num_rows = self.num_rows,
            required_to_win = self.required_to_win,
            players = self.players,
            matrix = copy.deepcopy(self.matrix)
        )

    def player_move(self, player, column_index):
        if player not in self.players:
            raise InvalidPlayerException('No player has name %s' % player)

        if column_index < 0 or column_index >= self.num_columns:
            raise InvalidColumnException('No column has index %d' % column_index)

        column = self.columns[column_index]

        try:
            empty_row_index = (index for index, cell in enumerate(column) if cell == EMPTY).next()
        except StopIteration:
            raise ColumnFullException('Column %d is full' % column_index)

        new_board = self.clone()
        new_board.rows[empty_row_index][column_index] = player
        return new_board

    @cached_property
    def lines(self):
        return (
            self.rows,
            self.columns,
            self.positive_diagonals,
            self.negative_diagonals
        )

    @cached_property
    def status(self):
        for line in chain(*self.lines):
            for cell, group in groupby(line):
                if cell != EMPTY and len(list(group)) >= self.required_to_win:
                    return BoardStatus(self, is_over = True, is_win = True, winner = cell)

        if self.is_full:
            return BoardStatus(self, is_over = True, is_draw = True)
        else:
            return BoardStatus(self, is_over = False)

    def match_subset(self, player, subset_length):
        needle = ([player] * subset_length) + [EMPTY]
        needle_length = len(needle)
        needles = list(set(permutations(needle)))
        result = 0

        for line in chain(*self.lines):
            line_length_range = range(len(line) - needle_length + 1)
            for n in needles:
                result += sum(1 for i in line_length_range if tuple(line[i:i+needle_length]) == n)

        return result

    def __str__(self):
        return '\n'.join(
            [' '.join(row) for row in reversed(self.rows)] +
            [' '.join(map(str, range(self.num_columns)))]
        )
