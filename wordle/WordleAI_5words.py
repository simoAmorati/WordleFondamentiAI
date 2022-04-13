from utility.RemainingOptions import remaining_options_wordle
from utility.WordProbability import WordProbability
MAX_GUESSES = 6
WORD_LENGTH = 5

class WordleAI_5words:

    def __init__(self, words):
        self.magic_words = ["bemix", "grypt", "clunk", "waqfs", "vozhd"]
        self.words = words
        self.word_probability = WordProbability()

    def guess(self, guess_history):
        guess_number = len(guess_history)
        if guess_number < MAX_GUESSES-1:
            next_guess = self.magic_words[guess_number]
        else:
            possible_options = remaining_options_wordle(self.words, guess_history)
            word_evaluations = [self.word_probability.is_wordle_probability(word) for word in possible_options]
            best_score = max(word_evaluations)
            next_guess = possible_options[word_evaluations.index(best_score)]
        return next_guess
