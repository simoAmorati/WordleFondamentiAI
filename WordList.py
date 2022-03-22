import os
import string
import requests
from os.path import exists
from os import getcwd

class WordList:
    """
    Reads a list of words from a file and filters it for wordle compatible words.
    Used to provide word list copies.
    """

    def __init__(self, filename='data/common_words_5_letters.txt'):
        self.ascii_lowercase = list(string.ascii_lowercase)
        if exists(filename) == False:
            url = 'https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt'
            words_site = requests.get(url)

            if filename.startswith("data/") == False:
                filename = "data/" + filename

            with open(filename, 'wb')as file:
                file.write(words_site.content)

        with open(filename, encoding="utf8") as file:
            self.words = file.readlines()
            self.words = [word.rstrip() for word in self.words]
            self.words = [w for w in self.words if len(w) == 5 and self.is_ascii_lowercase(w)]
            self.words = list(dict.fromkeys(self.words))  # remove duplicates

    def get_list_copy(self):
        return self.words.copy()

    def is_ascii_lowercase(self, word):
        for letter in word:
            if letter not in self.ascii_lowercase:
                return False
        return True

