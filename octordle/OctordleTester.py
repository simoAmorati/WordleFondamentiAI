import random
import time

from utility.WordList import *
from octordle.OctordleAI import *
from utility.LetterPositionInformation import LetterInformation
import numpy as np

MAX_GUESSES = 13
WORD_LENGTH = 5
GAMES = 8


class OctordleTester:

    def __init__(self, wordlist_filename="data/combined_wordlist.txt"):
        self.wordlist = WordList(wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = OctordleAI(self.words)

    def fight(self, rounds, solution_wordlist_filename="data/shuffled_real_wordles.txt", results_filename="results/OctordleResults.txt", printOnFile=False):
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
            word = [random.choice(fight_words) for _ in range(GAMES)]
            #word = ['slime', 'inept', 'lurid', 'curvy', 'racer', 'ninja', 'dream', 'extol']
            #shuffle(word)
            current_time = time.time() - start
            round_words.append(word)

            print("\rRound", r + 1, "/", rounds, "word =", word, "time", current_time, "/",
                  current_time * rounds / (r + 1), end='')
            success, round_guesses = self.play(self.competitor, word)
            round_points = len(round_guesses) if success else 10
            points += round_points
            guesses.append(round_guesses)
            points_per_round.append(round_points)

            if np.array_equal(success, [True, True, True, True, True, True, True, True]):
                success_total += 1
            else:
                index_list = []
                cont = 0
                for value in success:
                    if value == False:
                        index_list.append(cont)
                    cont += 1
                for index in index_list:
                    mistakes.append(word[index])

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

        print("")
        print("Competition finished with ", rounds, " rounds \n")

        if printOnFile:
            #os.chdir("../")
            with open(results_filename, 'a') as file:
                file.write("on file " + solution_wordlist_filename.split("/")[1] + " with " + str(rounds) + " rounds (" + time.strftime("%d/%m/%Y") + ")\n")
                file.write("Mistakes " + str(len(mistakes)) + "\n")
                file.write("Success rate: " + str(success_rate) + "\n")
                file.write("Average of guesses per round: " + str(result) + "\n")
                file.write("------------------------------------\n")

    def play(self, competitor, word):
        answered_guesses = []
        guess_history = []
        check_success = [False, False, False, False, False, False, False, False]

        for i in range(MAX_GUESSES):  # Up to 13 guesses
            guess = competitor.guess(guess_history)

            if not self.guess_is_legal(guess):
                print("guess ->", guess)
                print("Competitor ", competitor.__class__.__name__, " is cheating")
                print("Competition aborted.")
                quit()

            guess_result = []
            for g in range(GAMES):
                game_result = [None] * WORD_LENGTH
                for letter in range(WORD_LENGTH):
                    if guess[letter] not in word[g]:
                        game_result[letter] = LetterInformation.NOT_PRESENT
                    elif word[g][letter] == guess[letter]:
                        game_result[letter] = LetterInformation.CORRECT
                    else:
                        game_result[letter] = LetterInformation.PRESENT
                guess_result.insert(g, game_result)
            guess_history.append((guess, guess_result))
            answered_guesses.append(guess)

            for g in range(GAMES):
                if guess == word[g]:
                    check_success[g] = True
                    guess_history.remove((guess, guess_result))
                    guess_result[g] = []
                    guess_history.append((guess, guess_result))

            if np.array_equal(check_success, [True, True, True, True, True, True, True, True]):
                break

        return check_success, answered_guesses

    def guess_is_legal(self, guess):
        if len(guess) == 5 and guess.lower() == guess and guess in self.words:
            return True
        else:
            return False


def main():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(suppress=True)

    competition = OctordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=1, solution_wordlist_filename="data/shuffled_real_wordles.txt", printOnFile=True)


if __name__ == "__main__":
    main()
