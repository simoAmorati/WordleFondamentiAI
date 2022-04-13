from octordle.OctordleTester import *
import octordle.OctordleAI
from quordle.QuordleTester import *
import quordle.QuordleAI
from wordle.WordleTester import *
import wordle.WordleAI

def main():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(suppress=True)

    print(os.getcwd())

    competition = WordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/shuffled_real_wordles.txt", printOnFile=True)

    competition = WordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/combined_wordlist.txt", printOnFile=True)

    competition = QuordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/shuffled_real_wordles.txt", printOnFile=True)

    competition = QuordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/combined_wordlist.txt", printOnFile=True)

    competition = OctordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/shuffled_real_wordles.txt", printOnFile=True)

    competition = OctordleTester(wordlist_filename="data/combined_wordlist.txt")
    competition.fight(rounds=10000, solution_wordlist_filename="data/combined_wordlist.txt", printOnFile=True)

if __name__ == "__main__":
    main()