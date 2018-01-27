import pandas as pd
from model.game import Game2048


def play_one(game, strategy):
    game.reset()
    moves = 0

    while not game.game_over:
        moves += 1
        direction = strategy.get_action(game)

        game.play(direction)

    return game.score, game.max_tile, moves


def play_many(n, strategy):
    game = Game2048()

    data = []
    for idx in range(n):
        score, max_tile, count = play_one(game, strategy)
        data.append([score, max_tile, count])

    return pd.DataFrame(data=data, columns=['score', 'max_tile', 'moves'])
