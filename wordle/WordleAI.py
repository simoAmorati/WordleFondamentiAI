import numpy as np
from utility.WordProbability import WordProbability
from utility.RemainingOptions import remaining_options_wordle
from utility.OutcomeMinMax import calculate_outcome
WORD_LENGTH = 5
MAX_GUESSES=6

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

        possible_options = remaining_options_wordle(self.words, guess_history)

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
