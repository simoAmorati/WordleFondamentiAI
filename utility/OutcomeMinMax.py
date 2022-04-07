WORD_LENGTH = 5

def calculate_outcome(guess, solution):
    outcome = 0
    for i in range(WORD_LENGTH):
        if guess[i] == solution[i]:
            outcome += 2 * 3 ** i
        elif guess[i] not in solution:
            outcome += 3 ** i
    return outcome  # outcome id (0-242)