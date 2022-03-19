from WordList import *

wordlist = WordList()

dict = wordlist.get_best_score_dict()

print("first word ->", list(dict.keys())[0])

print("second word ->", wordlist.get_next_best_guesses(list(dict.keys())[0]))