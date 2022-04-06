import random

from tkinter import Tk, Button, Label, messagebox, PhotoImage, Text
from tkinter import Frame

import numpy as np

from utility.LetterPositionInformation import LetterInformation
from octordle.OctordleAI import OctordleAI
from utility.WordList import WordList

BACKGROUND = '#fafafa'
TITANIC = '#fafafa' + "#mifafamifasollasol"

MAX_GUESSES = 13
WORD_LENGTH = 5
GAMES = 8
MAX = 40
Green = '#538d4e'
Yellow = '#c9b458'
Grey = '#86888a'


class GUIOctordle(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.wordlist_filename = "data/shuffled_real_wordles.txt"
        self.wordlist = WordList(self.wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = OctordleAI(self.words)

        self.word = [random.choice(self.words) for _ in range(GAMES)]

        self.frame_title = Frame(self.master, bg=BACKGROUND, width=1600, height=100)
        self.frame_squares = Frame(self.master, bg=BACKGROUND, width=1600, height=500)
        self.frame_control = Frame(self.master, bg=BACKGROUND, width=1600, height=100)

        self.squares = [[None] * MAX for _ in range(MAX_GUESSES)]
        # self.chose_words = [None for _ in range(GAMES)]
        self.create_widgets()

    def create_widgets(self):
        self.top_frame()
        self.centre_frame()
        self.bottom_frame()

    def top_frame(self):
        self.frame_title.grid_propagate(0)
        self.frame_title.grid(column=0, row=0, sticky='snew')
        Label(self.frame_title, bg=BACKGROUND, fg='black', text='Octordle', font=('Arial', 25, 'bold')).pack(side='top')
        """Label(self.frame_title, bg=BACKGROUND, fg='black',
              text=self.word[0] + "\t" + self.word[1] + "\t" + self.word[2] + "\t" + self.word[3],
              font=('Arial', 10, 'bold')).pack(side='left')"""

    def centre_frame(self):

        self.frame_squares.grid_propagate(0)
        self.frame_squares.grid(column=0, row=1, sticky='snew')

        for i in range(MAX_GUESSES):
            for j in range(MAX):
                self.squares[i][j] = Label(self.frame_squares, width=2, height=1, fg='white', bg=BACKGROUND, text="",
                                           font=('Arial', 12, 'bold'), borderwidth=2, relief="groove")
                if (j + 1) % WORD_LENGTH == 0:
                    self.squares[i][j].grid(row=i, column=j, padx=(5, 20), pady=5)
                else:
                    self.squares[i][j].grid(row=i, column=j, padx=5, pady=5)

    def bottom_frame(self):
        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='snew')

        play_octordle_button = Button(self.frame_control, bg=Green, fg='white', text="Play Octordle",
                                      font=('Arial', 10),
                                      command=lambda: self.play_octordle_game())
        play_octordle_button.pack(side='bottom')

        """for i in range(GAMES):
            self.chose_words[i] = Text(self.frame_control, height=1, width=10, bg=BACKGROUND, fg='black', font=('Arial', 10),
                                       borderwidth=2, relief="groove")
            self.chose_words[i].grid(row=i + 1, column=0, padx=5, pady=10)

        chose_word_button = Button(self.frame_control, text="Choose word to guess", font=('Arial', 10),
                                   command=lambda: self.choose_word())
        chose_word_button.grid(row=1, column=1, padx=5, pady=10)"""

    def play_octordle_game(self):
        guess_history = []
        check_success = [False, False, False, False, False, False, False, False]
        for gss in range(MAX_GUESSES):  # Up to 9 guesses
            guess = self.competitor.guess(guess_history)
            if self.guess_is_legal(guess):
                guess_result = []
                for g in range(GAMES):
                    game_result = [None] * WORD_LENGTH
                    for letter in range(WORD_LENGTH):

                        self.squares[gss][g * WORD_LENGTH + letter].config(text=guess[letter].upper())
                        if guess[letter] not in self.word[g]:
                            self.squares[gss][g * WORD_LENGTH + letter]['bg'] = Grey
                            game_result[letter] = LetterInformation.NOT_PRESENT

                        elif self.word[g][letter] == guess[letter]:
                            self.squares[gss][g * WORD_LENGTH + letter]['bg'] = Green
                            game_result[letter] = LetterInformation.CORRECT
                        else:
                            self.squares[gss][g * WORD_LENGTH + letter]['bg'] = Yellow
                            game_result[letter] = LetterInformation.PRESENT
                        if check_success[g] is True:
                            self.squares[gss][g * WORD_LENGTH + letter].config(bg=BACKGROUND, text="", borderwidth=2,
                                                                               relief="groove")
                    guess_result.insert(g, game_result)
                guess_history.append((guess, guess_result))

                for g in range(GAMES):
                    if guess == self.word[g]:
                        check_success[g] = True
                        guess_history.remove((guess, guess_result))
                        guess_result[g] = []
                        guess_history.append((guess, guess_result))

            if gss <= MAX_GUESSES - 1 and np.array_equal(check_success,
                                                         [True, True, True, True, True, True, True, True]):
                messagebox.showinfo('YOU WIN', 'Congratulations')
                self.update_labels()
                self.word = [random.choice(self.words) for _ in range(GAMES)]
                break
            if gss == MAX_GUESSES - 1 and not (
            np.array_equal(check_success, [True, True, True, True, True, True, True, True])):
                messagebox.showinfo('YOU LOSE',
                                    'Try again\nwords were:\n' + self.word[0] + " " + self.word[1] + " " + self.word[
                                        2] + " " + self.word[3] + " " + self.word[4] + " " + self.word[5] + " " +
                                    self.word[6] + " " + self.word[7] + " ")
                self.update_labels()
                self.word = [random.choice(self.words) for _ in range(GAMES)]
                break

    def guess_is_legal(self, guess):
        if len(guess) == 5 and guess.lower() == guess and guess in self.words:
            return True
        else:
            return False

    def update_labels(self):
        for i in range(MAX_GUESSES):
            for j in range(MAX):
                self.squares[i][j].config(text="", bg=BACKGROUND, fg='white', borderwidth=2, relief="groove")

    """ def choose_word(self):
        for g in range(GAMES):
            self.word[g] = self.chose_words[g].get("1.0", "end-1c")

        for i in range(GAMES):
            if len(self.word) != WORD_LENGTH:
                self.word[i] = random.choice(self.words)
    """


if __name__ == "__main__":
    window = Tk()
    window.config(bg=BACKGROUND)
    window.call('wm', 'iconphoto', window._w,
                PhotoImage(file="images/logo.png"))
    window.geometry('1600x600')
    window.resizable(0, 0)
    window.title('Octordle')
    app = GUIOctordle(window)
    app.mainloop()
