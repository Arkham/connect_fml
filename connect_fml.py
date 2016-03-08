from itertools import chain, groupby

EMPTY = '.'

class InvalidColumnException(Exception):
    pass

class InvalidPlayerException(Exception):
    pass

class ColumnFullException(Exception):
    pass

class Board(object):
    def __init__(self, num_columns = 7, num_rows = 6, required_to_win = 4, players = ['R', 'Y']):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.required_to_win = required_to_win
        self.players = players
        self.board = [[EMPTY] * num_columns for _ in range(num_rows)]

    @property
    def rows(self):
        return self.board

    @property
    def columns(self):
        return [list(tuple) for tuple in zip(*self.rows)]

    @property
    def diagonal_indexes(self):
        h = self.num_rows
        w = self.num_columns
        return [[ (p, q) for q in range(min(p, h-1), max(0, p-w+1)-1, -1) ]
            for p in range(h+w-1)]

    @property
    def positive_diagonals(self):
        return [[ self.board[q][p-q] for (p, q) in diagonal ]
            for diagonal in self.diagonal_indexes]

    @property
    def negative_diagonals(self):
        h = self.num_rows
        return [[ self.board[h-1-q][p-q] for (p, q) in diagonal ]
            for diagonal in self.diagonal_indexes]

    def is_empty(self):
        return all(cell == EMPTY for cell in list(chain(*self.rows)))

    def is_full(self):
        return all(cell != EMPTY for cell in self.rows[-1])

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

        self.board[empty_row_index][column_index] = player

    def is_over(self):
        lines = (
            self.rows,
            self.columns,
            self.positive_diagonals,
            self.negative_diagonals
        )

        for line in chain(*lines):
            for cell, group in groupby(line):
                if cell != EMPTY and len(list(group)) >= self.required_to_win:
                    return [True, 'Win', cell]

        if self.is_full():
            return [True, 'Draw']
        else:
            return [False]

    def display(self):
        return '\n'.join(
            [' '.join(row) for row in reversed(self.board)] +
            [' '.join(map(str, range(self.num_columns)))]
        )
