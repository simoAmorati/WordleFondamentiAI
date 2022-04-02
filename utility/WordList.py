from typing import List
"""
import requests
import re
"""
import string
import os
from sys import platform

class WordList:
    """
    Reads a list of words from a file and filters it for wordle compatible words.
    Used to provide word list copies.
    """
    words: List[str]

    def __init__(self, filename):
        self.ascii_lowercase = list(string.ascii_lowercase)
        if platform == "win32" or platform == "Windows" or "Win" in platform or "win" in platform:
            filename = filename.replace("/", "\\")

        if filename.startswith("data") and "octordle" in os.getcwd():
            filename = os.getcwd()[:-8] + filename
        elif filename.startswith("data") and "quordle" in os.getcwd():
            filename = os.getcwd()[:-7] + filename
        elif filename.startswith("data") and "wordle" in os.getcwd():
            filename = os.getcwd()[:-6] + filename
        with open(filename, encoding="utf8") as file:
            self.words = file.readlines()
            self.words = [word.rstrip() for word in self.words]
            self.words = [w for w in self.words if len(w) == 5 and self.is_ascii_lowercase(w)]
            self.words = list(dict.fromkeys(self.words))  # remove duplicates
    """
    def __init__(self):
        self.ascii_lowercase = list(string.ascii_lowercase)

        url = 'https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt'
        words_site = requests.get(url)

        with open('data/common_words_5_letters.txt', 'wb') as file:
            file.write(words_site.content)

        with open('data/common_words_5_letters.txt', encoding="utf8") as file:
            self.words = file.readlines()
            self.words = [word.rstrip() for word in self.words]
            self.words = [w for w in self.words if len(w) == 5 and self.is_ascii_lowercase(w)]
            self.words = list(dict.fromkeys(self.words))  # remove duplicates
    """

    def get_list_copy(self):
        return self.words.copy()

    def is_ascii_lowercase(self, word):
        for letter in word:
            if letter not in self.ascii_lowercase:
                return False
        return True

"""
    # da la popolarità della lettera cercando in ogni parola del dizionario conta la popolarità delle lettere
    def get_dict_letters_percentages(self):
        all_letters = string.ascii_lowercase[:]

        letter_stats_dict = {}
        for letter in all_letters:
            letter_stats_dict[letter] = 0

        total_letters = len(self.words) * 5.0

        for letter in all_letters:
            for word in self.words:
                letter_stats_dict[letter] += word.count(letter)

        total = 0
        for letter in all_letters:
            letter_stats_dict[letter] /= total_letters
            total = total + letter_stats_dict[letter]

        return letter_stats_dict

    # da il best score non sapendo la popolarità delle parole usate
    # si basa solo sulla popolarità delle lettere che compongono la parola
    def get_best_score_dict(self):
        letter_stats_dict = self.get_dict_letters_percentages()
        word_stat_dict = {}
        for word in self.words:
            word_stat_dict[word] = 0

        for word in self.words:
            unq_char_word = "".join(set(word))
            for letter in unq_char_word:
                word_stat_dict[word] += letter_stats_dict[letter]

        word_stat_dict = sorted(word_stat_dict.items(), key=lambda x: x[1], reverse=True)
        word_stat_dict = dict(word_stat_dict)
        return word_stat_dict

    def get_next_best_guesses(self, first_word):
        string_regex = '^[^' + first_word + ']+$'
        regex = re.compile(string_regex)

        for word, information_value in self.get_best_score_dict().items():
            if re.search(regex, word):
                return word
"""