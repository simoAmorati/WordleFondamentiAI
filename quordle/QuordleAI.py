import numpy as np

from LetterPositionInformation import LetterInformation
from WordProbability import WordProbability

WORD_LENGTH = 5
GAMES = 4
BONUS_CORRECT = 5
BONUS_PRESENT = 3
BONUS_NOT_PRESENT = 1


class QuordleAI:
    """words is a list of all wordle possible words"""

    def __init__(self, words):
        self.words = words
        self.indexed_words = {key: value for value, key in enumerate(self.words)}
        self.word_probability = WordProbability()

    """guess  history in the quordle case has a different structure each element of the list has four sublist with the
     information for each game in the quordle board"""

    def guess(self, guess_history):
        attempts = ["prone", "claim", "study"]
        num_attempts = len(guess_history)
        if num_attempts == 0:  # precalculated more efficient with if than for cycle
            return attempts[0]
        if num_attempts == 1:  # precalculated
            return attempts[1]
        if num_attempts == 2:  # precalculated
            return attempts[2]

        possible_options = remaining_options(self.words, guess_history)

        for i in range(GAMES):
            if len(possible_options[i]) == 1:
                return possible_options[i][0]

        best_game = gameToEnd_LessPossibleOptions(possible_options)

        best_worst_outcome = len(possible_options[best_game])
        best_word = self.words[0]
        outcomes = np.empty(243, dtype=float)

        for i in range(len(self.words)):
            word = self.words[i]
            outcomes.fill(0)
            for option in possible_options[best_game]:
                outcome_id = calculate_outcome(word, option)
                outcomes[outcome_id] += self.word_probability.is_wordle_probability(option)
                if outcomes[outcome_id] > best_worst_outcome:
                    break
            outcomes[242] = 0  # don't punish for finding a solution
            worst_outcome = np.max(outcomes)
            if worst_outcome < best_worst_outcome or (worst_outcome == best_worst_outcome and (
                    best_word not in possible_options[best_game] or self.word_probability.is_wordle_probability(
                word) > self.word_probability.is_wordle_probability(best_word)) and word in possible_options[
                                                          best_game]):
                best_worst_outcome = worst_outcome
                best_word = word

        return best_word


def remaining_options(words, guess_history):
    #   possible_options = [words, words, words, words]
    possible_options = [[] for _ in range(GAMES)]
    present_letters = [set() for _ in range(GAMES)]  # list of present letters
    not_present_letters = [set() for _ in range(GAMES)]  # list of not present letters
    present_letter_position = [set() for _ in
                               range(GAMES)]  # list of list with present letter with already tried position
    correct_letter_position = [set() for _ in range(GAMES)]  # list of correct letters with correct position

    finish_game = {i: False for i in range(GAMES)}
    for element in guess_history:
        for i in range(0, len(element[1])):
            if element[1][i]:
                index_letter = 0
                for letter in element[1][i]:

                    if letter == LetterInformation.CORRECT:
                        present_letters[i].add(element[0][index_letter])
                        correct_letter_position[i].add((element[0][index_letter], index_letter))

                    if letter == LetterInformation.PRESENT:
                        present_letters[i].add(element[0][index_letter])
                        present_letter_position[i].add((element[0][index_letter], index_letter))

                    if letter == LetterInformation.NOT_PRESENT:
                        not_present_letters[i].add(element[0][index_letter])

                    index_letter += 1
            else:
                finish_game[i] = True

    for i in range(GAMES):
        if not finish_game[i]:
            for l in present_letters[i]:
                possible_options[i] = [w for w in words if l in w]
            for l in not_present_letters[i]:
                possible_options[i] = [w for w in possible_options[i] if l not in w]
            for l in correct_letter_position[i]:
                possible_options[i] = [w for w in possible_options[i] if w[l[1]] == l[0]]
            for l in present_letter_position[i]:
                possible_options[i] = [w for w in possible_options[i] if w[l[1]] != l[0]]

    return possible_options


def calculate_outcome(guess, solution):
    outcome = 0
    for i in range(5):
        if guess[i] == solution[i]:
            outcome += 2 * 3 ** i
        elif guess[i] not in solution:
            outcome += 3 ** i
    return outcome  # outcome id (0-242)


"""KnowledgeStrategy"""


def gameToEnd_KnowledgeStrategy(guess_history):
    correct_letters = [0 for _ in range(GAMES)]
    present_letters = [0 for _ in range(GAMES)]
    not_present_letters = [0 for _ in range(GAMES)]
    knowledge = [0 for _ in range(GAMES)]
    for guess in guess_history:
        for j in range(GAMES):
            if guess[1][j]:
                for letter in range(WORD_LENGTH):
                    if guess[1][j][letter] == LetterInformation.CORRECT:
                        correct_letters[j] += 1
                    if guess[1][j][letter] == LetterInformation.PRESENT:
                        present_letters[j] += 1
                    if guess[1][j][letter] == LetterInformation.NOT_PRESENT:
                        not_present_letters[j] += 1

    for i in range(GAMES):
        knowledge[i] = BONUS_CORRECT * correct_letters[i] + BONUS_PRESENT * present_letters[i] + BONUS_NOT_PRESENT * \
                       not_present_letters[i]

    return knowledge.index(max(knowledge))


def gameToEnd_LessPossibleOptions(possible_options):
    minimum = 999999999999
    cont = -1
    for option in possible_options:
        if len(option) < minimum and len(option) != 0:
            minimum = len(option)
            cont = possible_options.index(option)
    return cont
