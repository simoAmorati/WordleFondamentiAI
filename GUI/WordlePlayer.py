from LetterPositionInformation import LetterInformation
from WordList import WordList
from WordleAISofia import WordleAISofia
import random

MAX_GUESSES = 6
WORD_LENGTH = 5


class WordlePlayer:

    def __init__(self):
        self.wordlist_filename = "data/combined_wordlist-txt"
        self.wordlist = WordList(self.wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = WordleAISofia(self.words)

        word = random.choice(self.words)
        self.game = self.play_game(self.competitor, word)

    def play_game(self, competitor, word):
        answered_guesses = []
        success = False
        guess_history = []

        for i in range(MAX_GUESSES):  # Up to 6 guesses
            guess = competitor.guess(guess_history)

            if self.guess_is_legal(guess):
                guess_result = []
                for letter in range(WORD_LENGTH):
                    if guess[letter] not in word:
                        guess_result.append(LetterInformation.NOT_PRESENT)
                    elif word[letter] == guess[letter]:
                        guess_result.append(LetterInformation.CORRECT)
                    else:
                        guess_result.append(LetterInformation.PRESENT)
                guess_history.append((guess, guess_result))
                answered_guesses.append(guess)

                if guess == word:
                    success = True
                    break

            return success, answered_guesses

    def guess_is_legal(self, guess):
        if len(guess) == 5 and guess.lower() == guess and guess in self.words:
            return True
        else:
            return False
