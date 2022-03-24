from enum import Enum


class LetterInformation(Enum):
    UNKNOWN = -1  # light grey in the game
    NOT_PRESENT = 0  # dark grey in the game
    PRESENT = 1  # yellow in the game
    CORRECT = 2  # green in the game
