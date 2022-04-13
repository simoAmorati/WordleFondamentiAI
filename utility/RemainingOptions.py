from utility.LetterPositionInformation import LetterInformation


WORD_LENGTH = 5


def remaining_options_wordle(words, guess_history):
    possible_options = words
    present_letters = set()  # list of present letters
    not_present_letters = set()  # list of not present letters
    present_letter_position = set()  # list of list with present letter with already tried position
    correct_letter_position = set()  # list of correct letters with correct position

    # guess_history is a list of list were the first element =[0] of each sublist is the guesses word and the second
    # element =[1] is a list containing the LetterPositionInformation for each letter in the word
    for element in guess_history:
        for i in range(WORD_LENGTH):
            if element[1][i] == LetterInformation.CORRECT:
                present_letters.add(element[0][i])
                correct_letter_position.add((element[0][i], i))
                # adds to the set of correct letters the letter and its corresponding correct position

            if element[1][i] == LetterInformation.PRESENT:
                present_letters.add(element[0][i])
                present_letter_position.add((element[0][i], i))

            if element[1][i] == LetterInformation.NOT_PRESENT:
                not_present_letters.add(element[0][i])

    possible_options = [w for w in words if allLettersInWord(w, present_letters)]
    possible_options = [w for w in possible_options if forbiddenLettersNotInWord(w, not_present_letters)]
    possible_options = [w for w in possible_options if correctLetterPosition(w, correct_letter_position)]
    possible_options = [w for w in possible_options if presentLetterPosition(w, present_letter_position)]

    """print(possible_options)

    rem_option = possible_options

    for w in possible_options:
        remove_p = False
        remove_np = False
        for let in present_letters:
            if len(present_letters) == WORD_LENGTH:
                if w.count(let) != 1 and remove_p is False:
                    rem_option.remove(w)
                    remove_p = True
            if let not in w and remove_p is False:
                rem_option.remove(w)
                remove_p = True
        for let in not_present_letters:
            if let in w and remove_np is False:
                rem_option.remove(w)
                remove_np = True"""

    return possible_options


def remaining_options(words, guess_history, games):
    possible_options = [[] for _ in range(games)]
    present_letters = [set() for _ in range(games)]  # list of present letters
    not_present_letters = [set() for _ in range(games)]  # list of not present letters
    present_letter_position = [set() for _ in
                               range(games)]  # list of list with present letter with already tried position
    correct_letter_position = [set() for _ in range(games)]  # list of correct letters with correct position

    finish_game = {i: False for i in range(games)}

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

    for g in range(games):
        if not finish_game[g]:
            possible_options[g] = [w for w in words if allLettersInWord(w, present_letters[g])]
            possible_options[g] = [w for w in possible_options[g] if forbiddenLettersNotInWord(w, not_present_letters[g])]
            possible_options[g] = [w for w in possible_options[g] if correctLetterPosition(w, correct_letter_position[g])]
            possible_options[g] = [w for w in possible_options[g] if presentLetterPosition(w, present_letter_position[g])]

    # print(possible_options)
    """rem_option = possible_options

    for gm in range(GAMES):
        for w in possible_options[gm]:
            remove_p = False
            remove_np = False
            for let in present_letters[gm]:
                if len(present_letters[gm]) == WORD_LENGTH:
                    if w.count(let) >= 2 and remove_p is False:
                        rem_option[gm].remove(w)
                        remove_p = True
                if let not in w and remove_p is False:
                    rem_option[gm].remove(w)
                    remove_p = True
            for let in not_present_letters[gm]:
                if let in w and remove_np is False:
                    rem_option[gm].remove(w)
                    remove_np = True

    print(rem_option)"""
    return possible_options


def allLettersInWord(word, letters):
    for l in letters:
        if l in word:
            continue
        else:
            return False

    return True


def forbiddenLettersNotInWord(word, letters):
    for l in letters:
        if l in word:
            return False

    return True


def correctLetterPosition(word, correct_letter_position):
    for l in correct_letter_position:
        if word[l[1]] == l[0]:
            continue
        else:
            return False
    return True


def presentLetterPosition(word, present_letter_position):
    for l in present_letter_position:
        if word[l[1]] == l[0]:
            return False

    return True
