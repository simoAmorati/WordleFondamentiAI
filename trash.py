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

combined_wordlist_list=[]
with open('data/combined_wordlist.txt', encoding="utf8") as file:
    combined_wordlist = file.readlines()
    combined_wordlist = [word.rstrip() for word in combined_wordlist]
    combined_wordlist = [w for w in combined_wordlist if len(w) == 5]
    combined_wordlist_list = list(dict.fromkeys(combined_wordlist))  # remove duplicates


common_words_5_letters_list=[]
with open('data/common_words_5_letters.txt', encoding="utf8") as file:
    common_words_5_letters = file.readlines()
    common_words_5_letters = [word.rstrip() for word in common_words_5_letters]
    common_words_5_letters = [w for w in common_words_5_letters if len(w) == 5]
    common_words_5_letters_list = list(dict.fromkeys(common_words_5_letters))  # remove duplicates

not_present_list = [word for word in common_words_5_letters_list if word not in combined_wordlist_list]
print(len(not_present_list))