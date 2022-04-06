import numpy as np

from utility.WordProbability import WordProbability
from utility.StrategyGameToEnd import gameToEnd_KnowledgeStrategy, gameToEnd_LessPossibleOptions
from utility.RemainingOptions import remaining_options
from utility.OutcomeMinMax import calculate_outcome
WORD_LENGTH = 5
GAMES = 4


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

        # print("num attempt=", num_attempts)
        possible_options = remaining_options(self.words, guess_history, GAMES)

        for i in range(GAMES):
            if len(possible_options[i]) == 1:
                # print(possible_options[i][0])
                return possible_options[i][0]

        best_game = gameToEnd_LessPossibleOptions(possible_options)
        # print("best game", best_game)

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


