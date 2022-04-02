import numpy as np
from utility.LetterPositionInformation import LetterInformation
from utility.WordProbability import WordProbability

WORD_LENGTH = 5


class WordleAISofia:
    """words is a list of all wordle possible words"""

    def __init__(self, words):
        self.words = words
        self.indexed_words = {key: value for value, key in enumerate(self.words)}
        self.word_probability = WordProbability()

    def guess(self, guess_history):
        attempts = ['study', 'claim', 'prone']
        num_attempts = len(guess_history)
        if num_attempts == 0:  # precalculated
            return attempts[0]
        if num_attempts == 1:  # precalculated
            return attempts[1]
        if num_attempts == 2:  # precalculated
            return attempts[2]

        possible_options = remaining_options(self.words, guess_history)

        if len(possible_options) == 1:
            return possible_options[0]

        w = 0
        best_worst_outcome = len(possible_options)
        best_word = self.words[0]
        outcomes = np.empty(243, dtype=float)
        for i in range(len(self.words)):
            word = self.words[i]
            outcomes.fill(0)
            for option in possible_options:
                outcome_id = calculate_outcome(word, option)
                outcomes[outcome_id] += self.word_probability.is_wordle_probability(option)
                if outcomes[outcome_id] > best_worst_outcome:
                    break
            outcomes[242] = 0  # don't punish for finding a solution
            worst_outcome = np.max(outcomes)
            if worst_outcome < best_worst_outcome or (worst_outcome == best_worst_outcome and (
                    best_word not in possible_options or self.word_probability.is_wordle_probability(word) > self.word_probability.is_wordle_probability(best_word)) and word in possible_options):
                best_worst_outcome = worst_outcome
                best_word = word
            w += 1

        return best_word


def remaining_options(words, guess_history):
    possible_options = words
    present_letters = set()  # list of present letters
    not_present_letters = set()  # list of not present letters
    present_letter_position = set()  # list of list with present letter with already tried position
    correct_letter_position = set()  # list of correct letters with correct position

    for element in guess_history:  # guess_history is a list of list were the first element =[0] of each sublist is the guesses word and the second element =[1] is a list containing the LetterPositionInformation for each letter in the word
        for i in range(WORD_LENGTH):
            if element[1][i] == LetterInformation.CORRECT:
                present_letters.add(element[0][i])
                correct_letter_position.add((element[0][i], i))  # adds to the set of correct letters the letter and its corresponding correct position

            if element[1][i] == LetterInformation.PRESENT:
                present_letters.add(element[0][i])
                present_letter_position.add((element[0][i], i))

            if element[1][i] == LetterInformation.NOT_PRESENT:
                not_present_letters.add(element[0][i])

    for l in present_letters:
        possible_options = [word for word in possible_options if l in word]
    for l in not_present_letters:
        possible_options = [word for word in possible_options if l not in word]
    for el in correct_letter_position:
        possible_options = [word for word in possible_options if word[el[1]] == el[0]]
    for el in present_letter_position:
        possible_options = [word for word in possible_options if word[el[1]] != el[0]]

    return possible_options


def calculate_outcome(guess, solution):
    outcome = 0
    for i in range(5):
        if guess[i] == solution[i]:
            outcome += 2 * 3 ** i
        elif guess[i] not in solution:
            outcome += 3 ** i
    return outcome  # outcome id (0-242)
