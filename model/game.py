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

    def has_cells_available(self):
        return self._grid.min() == 0

    def has_tile_match_available(self):
        return False

    def has_move_available(self):
        return self.has_cells_available() or self.has_tile_match_available()

    def play(self, direction):
        moved, score = self.move(direction)
        self.score += score

        if moved:
            self.add_random_tile()

            if not self.has_move_available():
                self.game_over = True
            
        return score
