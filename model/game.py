import numpy as np

N = 4

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

POSITION_TURNS = {
    UP: lambda i, j: (j, i),
    RIGHT: lambda i, j: (i, N - j - 1),
    DOWN: lambda i, j: (N - j - 1, i),
    LEFT: lambda i, j: (i, j),
}

class Game2048:
    def __init__(self):
        self.reset()

    def copy(self):
        game = Game2048()
        game._grid = np.copy(self._grid)
        game.game_over = self.game_over
        game.score = self.score

        return game

    def reset(self):
        self.game_over = False
        self.score = 0
        self._grid = np.zeros((N, N)).astype(np.uint8)
        self.add_random_tile()
        self.add_random_tile()

    def _get(self, i, j, direction=None):
        if direction is not None:
            i, j = POSITION_TURNS[direction](i, j)
        return self._grid[i][j]

    def _set(self, i, j, v, direction=None):
        if direction is not None:
            i, j = POSITION_TURNS[direction](i, j)
        self._grid[i][j] = v

    def add_random_tile(self):
        value = 1 if np.random.random() < 0.9 else 2

        i, j = self.get_random_available_cell()
        
        self._set(i, j, value)
        
    def get_random_available_cell(self):
        cells = self.get_available_cells()
        
        if len(cells) == 0:
            raise Exception('No available cell :/')
        
        return cells[int(np.random.random() * len(cells))]
    
    def get_available_cells(self):
        return [
            (i, j)
            for i, xi in enumerate(self._grid)
            for j, value in enumerate(xi)
            if value == 0
        ]
    
    @property
    def grid(self):
        return np.vectorize(lambda v: 2**v if v > 0 else 0)(self._grid)

    @property
    def max_tile(self):
        return self.grid.max()

    def move(self, direction):
        if self.game_over:
            raise Exception('Game is over :/')

        score = 0
        moved = 0
        # Collapse & merge
        for i in range(N):
            offset = 0
            collapse_value = None
            
            for j in range(N):
                value = self._get(i, j, direction=direction)
                if value == 0:
                    offset += 1
                elif value == collapse_value:
                    self._set(i, j, 0, direction=direction)
                    self._set(i, j - offset - 1, value + 1, direction=direction)
                    offset += 1
                    collapse_value = None
                    
                    score += 2**(value+1)
                    moved += 1
                elif offset > 0:
                    self._set(i, j, 0, direction=direction)
                    self._set(i, j - offset, value, direction=direction)
                    collapse_value = value
                    moved += 1
                else:
                    collapse_value = value
        
        return moved, score

    def can_move(self, direction):
        for i in range(N):
            for j in range(N-1):
                value = self._get(i, j, direction=direction)
                next_value = self._get(i, j+1, direction=direction)
                if value != 0 and value == next_value:
                    return True
                elif value == 0 and next_value != 0:
                    return True

        return False

    def has_cells_available(self):
        return self._grid.min() == 0

    def has_tile_match_available(self):
        for i in range(N):
            for j in range(N-1):
                if self._get(i, j) == self._get(i, j+1) and self._get(i, j) != 0:
                    return True
                if self._get(j, i) == self._get(j+1, i) and self._get(j, i) != 0:
                    return True

        return False

    def has_move_available(self):
        return self.has_cells_available() or self.has_tile_match_available()

    def play(self, direction):
        """
        Plays:
        - @args direction [int]: UP (0), RIGHT (1), DOWN (2) or LEFT (3)
        - @return (moved, score) [int, int]: number of tiles that have moved
                                             and the score i.e. the sum of
                                             the values of merged tiles
        """
        moved, score = self.move(direction)
        self.score += score

        if moved:
            self.add_random_tile()

            if not self.has_move_available():
                self.game_over = True
            
        return moved, score
