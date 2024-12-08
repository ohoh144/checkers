from enum import Enum


class GameState(Enum):
    WHITE_TURN = "white_turn"
    BLACK_TURN = "black_turn"
    WHITE_WON = "white_won"
    BLACK_WON = "black_won"
