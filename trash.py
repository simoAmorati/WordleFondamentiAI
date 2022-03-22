"""
from WordList import *

wordlist = WordList()

dict = wordlist.get_best_score_dict()

print("first word ->", list(dict.keys())[0])

print("second word ->", wordlist.get_next_best_guesses(list(dict.keys())[0]))
"""

"""
import numpy as np

data = np.load('data/precalculated_guesses.npz')

for file in data.files:
    print(data[file])
"""

from WordleFondamentiAI import *
from WordList import *

wordList = WordList()
words = wordList.get_list_copy()
ai = WordleFondamentiAI(words)
ai.guess(words)


