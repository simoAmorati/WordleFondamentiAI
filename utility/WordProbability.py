from utility.WordList import WordList
MIN = 0.025

class WordProbability:
    """
    Helper class to take into account how common words are in the English language.
    """

    def __init__(self):
        self.common_words = WordList("data/common_words.txt").words
        self.probability = {}
        self.words = WordList("data/combined_wordlist.txt").words
        for word in self.words:
            self.probability[word] = self._calculate_probability(word)

    def _calculate_probability(self, word):
        if word not in self.common_words:
            return MIN
        relative_position = self.common_words.index(word) / len(self.common_words)
        return 0.95 * (1 - relative_position) + 0.25 * relative_position

    def is_wordle_probability(self, word):
        """
        :param word: a 5 letter word
        :return: the probability of the word being a wordle based on its popularity in the English language
        """
        return self.probability[word]
