from utility.RemainingOptions import remaining_options_wordle

import string
MAX_GUESSES = 6
WORD_LENGTH = 5

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
