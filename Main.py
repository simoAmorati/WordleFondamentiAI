from WordleFondamentiAI import *
import random
import time
import numpy as np


# nel caso facessimo più ai
def play(competitor, word):
    guesses = []
    success = False
    guess_history = []

    for i in range(6):  # max 5 ipotesi
        guess = competitor.guess(guess_history)

        guess_result = []
        for c in range(5):
            if guess[c] not in word:
                guess_result.append(LetterInformation.NOT_PRESENT)
            elif word[c] == guess[c]:
                guess_result.append(LetterInformation.CORRECT)
            else:
                guess_result.append(LetterInformation.PRESENT)
        guess_history.append((guess, guess_result))
        guesses.append(guess)

        if guess == word:
            success = True
            break
    return success, guesses


def main(competitors, rounds):
    result = {}
    success_total = {}
    guesses = {}
    points = {}
    round_words = []

    for competitor in competitors:
        result[competitor] = 0
        success_total[competitor] = 0
        guesses[competitor] = []
        points[competitor] = []

    fight_words = WordList('data/combined_wordlist.txt').get_list_copy()
    round_words = []

    start = time.time()
    competitor_times = np.zeros(len(competitors))
    for i in range(rounds):
        correct_word = random.choice(fight_words)
        current_time = time.time() - start
        round_words.append(correct_word)
        c = 0
        for competitor in competitors:
            print("\rRound", i + 1, "/", rounds, "word =", correct_word, "competitior", c + 1, "/", len(competitors),
                  "time", current_time, "/", current_time * rounds / (i + 1), end='')
            competitor_start = time.time()
            success, round_guesses = play(competitor, correct_word)
            round_points = len(round_guesses) if success else 10
            result[competitor] += round_points
            guesses[competitor].append(round_guesses)
            points[competitor].append(round_points)
            if success:
                success_total[competitor] += 1
            competitor_times[c] += time.time() - competitor_start
            c += 1

    print("\n")
    print("Words: ", round_words)
    print("Guesses: ", guesses)
    print("Points per round: ", points)
    print("")


if __name__ == "__main__":
    competitors = []
    letterPopularityAI = WordleFondamentiAI()
    competitors.append(letterPopularityAI)
    main(competitors, 20)