from utility.RemainingOptions import remaining_options_wordle
from utility.WordList import *
from enum import Enum, auto
import string
MAX_GUESSES = 6
WORD_LENGTH = 5


class LetterInformation(Enum):
    UNKOWN = auto()  # light grey in the game
    PRESENT = auto()  # yellow in the game
    NOT_PRESENT = auto()  # dark grey in the game
    CORRECT = auto()  # green in the game


class WordleAI_lettersProbability:

    def __init__(self, words):
        self.words = words

    def guess(self, guess_history):
        options = remaining_options_wordle(self.words, guess_history)
        letters_popularity = get_dict_letters_percentages(options)
        best_option = ""
        highest_score = 0
        for option in options:
            score = get_score(option, letters_popularity)
            if score > highest_score:
                highest_score = score
                best_option = option
        return best_option


def get_dict_letters_percentages(words):
    letter_popularity = dict.fromkeys(list(string.ascii_lowercase), 0)
    for word in words:
        for letter in word:
            letter_popularity[letter] += 1
    return letter_popularity


def get_score(word, letters_probability):
    word_probability = 0
    for letter in set(word):
        word_probability += letters_probability[letter]
    return word_probability


def remaining_options(words, guess_history):
    """
    Filters a word list with all the known information.
    Returns the list of remaining options.
    """
    present = set()
    not_present = set()
    correct = set()
    present_letters = set()
    for entry in guess_history:
        for i in range(5):
            if entry[1][i] == LetterInformation.CORRECT:
                correct.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            elif entry[1][i] == LetterInformation.PRESENT:
                present.add((entry[0][i], i))
                present_letters.add(entry[0][i])
            else:
                not_present.add(entry[0][i])

    for c in present_letters:
        words = [w for w in words if c in w]
    for c in not_present:
        words = [w for w in words if c not in w]
    for c in correct:
        words = [w for w in words if w[c[1]] == c[0]]
    for c in present:
        words = [w for w in words if w[c[1]] != c[0]]

    return words