import random
import time

from utility.WordList import *
from WordleAI import *
from utility.LetterPositionInformation import *

MAX_GUESSES = 6
WORD_LENGTH = 5


class WordleTester:

    def __init__(self, wordlist_filename="data/combined_wordlist.txt"):
        self.wordlist = WordList(wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = WordleAI(self.words)

    def fight(self, rounds, solution_wordlist_filename="data/combined_wordlist.txt"):
        print("Start tournament")
        round_words = []
        success_total = 0
        guesses = []
        points = 0
        points_per_round = []
        mistakes = []

        fight_words = WordList(solution_wordlist_filename).get_list_copy()
        start = time.time()
        competitor_time = 0

        for r in range(rounds):
            word = random.choice(fight_words)
            current_time = time.time() - start
            round_words.append(word)

            print("\rRound", r + 1, "/", rounds, "word =", word, "time", current_time, "/",
                  current_time * rounds / (r + 1), end='')
            success, round_guesses = self.play(self.competitor, word)
            round_points = len(round_guesses) if success else 10
            points += round_points
            guesses.append(round_guesses)
            points_per_round.append(round_points)

            if success:
                success_total += 1
            else:
                mistakes.append(word)

            competitor_time += time.time() - current_time

        result = points / rounds
        success_rate = 100 * success_total / rounds
        print("\n")
        print("Words: ", round_words)
        print("Guesses: ", guesses)
        print("Mistakes, not guessed words", mistakes)
        print("")
        print("Points per round: ", points)
        print("Average of guesses per round: ", result)
        print("Success rate: ", success_rate)
        print("Time per round: ", competitor_time/rounds)

        print("")
        print("Competition finished with ", rounds, " rounds \n")

    def play(self, competitor, word):
        answered_guesses = []
        success = False
        guess_history = []

        for i in range(MAX_GUESSES):  # Up to 6 guesses
            guess = competitor.guess(guess_history)

            if not self.guess_is_legal(guess):
                print("Competitor ", competitor.__class__.__name__, " is cheating")
                print("Competition aborted.")
                quit()

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


def main():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(suppress=True)

    competition = WordleTester(wordlist_filename="data/combined_wordlist.txt")
    #competition.fight(rounds=1000, solution_wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=1000, solution_wordlist_filename="data/shuffled_real_wordles.txt")

if __name__ == "__main__":
    main()
