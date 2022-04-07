from utility.LetterPositionInformation import LetterInformation

BONUS_CORRECT = 5
BONUS_PRESENT = 3
BONUS_NOT_PRESENT = 1

def gameToEnd_KnowledgeStrategy(guess_history, games, word_length):
    correct_letters = [0 for _ in range(games)]
    present_letters = [0 for _ in range(games)]
    not_present_letters = [0 for _ in range(games)]
    knowledge = [0 for _ in range(games)]
    for guess in guess_history:
        for j in range(games):
            if guess[1][j]:
                for letter in range(word_length):
                    if guess[1][j][letter] == LetterInformation.CORRECT:
                        correct_letters[j] += 1
                    if guess[1][j][letter] == LetterInformation.PRESENT:
                        present_letters[j] += 1
                    if guess[1][j][letter] == LetterInformation.NOT_PRESENT:
                        not_present_letters[j] += 1

    for i in range(games):
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
