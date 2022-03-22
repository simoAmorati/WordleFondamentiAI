import string
import re
from enum import Enum, auto
from WordList import *

class LetterInformation(Enum):
    UNKOWN = auto()  # light grey in the game
    PRESENT = auto()  # yellow in the game
    NOT_PRESENT = auto()  # dark grey in the game
    CORRECT = auto()  # green in the game

class WordleFondamentiAI():

    def __init__(self):
        words = WordList().get_list_copy()
        self.words = words  # list of all legal 5 letter words

    def guess(self, guess_history):
        options = remaining_options(self.words, guess_history)
        letters_popularity = get_dict_letters_percentages(options)
        best_option = ""
        highest_score = 0
        for option in options:
            score = get_score(option, letters_popularity)
            if score > highest_score:
                highest_score = score
                best_option = option
        return best_option

    def get_author(self):
        return "simone e sofia"


# restituisce la popolarità delle lettere a partire da una lista in ingresso
def get_dict_letters_percentages(words):
    letter_popularity = dict.fromkeys(list(string.ascii_lowercase), 0)
    for word in words:
        for letter in word:
            letter_popularity[letter] += 1  # each occurance of the letter is counted
    return letter_popularity


# da il best score non sapendo la popolarità delle parole usate
# si basa solo sulla popolarità delle lettere che compongono la parola
def get_best_score_dict(letter_stats_dict, words):
    word_stat_dict = {}
    for word in words:
        word_stat_dict[word] = 0

    for word in words:
        unq_char_word = "".join(set(word))
        for letter in unq_char_word:
            word_stat_dict[word] += letter_stats_dict[letter]

    word_stat_dict = sorted(word_stat_dict.items(), key=lambda x: x[1], reverse=True)
    word_stat_dict = dict(word_stat_dict)
    return word_stat_dict


def get_score(word, letters_probability):
    word_probability = 0
    for letter in set(word):
        word_probability += letters_probability[letter]
    return word_probability


def get_next_best_guesses(self, first_word):
    string_regex = '^[^' + first_word + ']+$'
    regex = re.compile(string_regex)

    for word, information_value in self.get_best_score_dict().items():
        if re.search(regex, word):
            return word


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
