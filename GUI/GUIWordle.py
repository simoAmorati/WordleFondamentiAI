import random

from tkinter import Tk, Button, Label, messagebox, PhotoImage, Text
from tkinter import Frame

from utility.LetterPositionInformation import LetterInformation
from wordle.WordleAI import WordleAI
from utility.WordList import WordList

BACKGROUND = '#fafafa'
TITANIC = '#fafafa' + "#mifafamifasollasol"

MAX_GUESSES = 6
WORD_LENGTH = 5
Green = '#538d4e'
Yellow = '#c9b458'
Grey = '#86888a'


class GUIWordle(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.wordlist_filename = "data/shuffled_real_wordles.txt"
        self.wordlist = WordList(self.wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = WordleAI(self.words)

        self.word = random.choice(self.words)

        self.frame_title = Frame(self.master, bg=BACKGROUND, width=300, height=100)
        self.frame_squares = Frame(self.master, bg=BACKGROUND, width=300, height=350)
        self.frame_control = Frame(self.master, bg=BACKGROUND, width=300, height=150)

        self.squares = [[None] * WORD_LENGTH for _ in range(MAX_GUESSES)]
        self.chose_word = None

        self.create_widgets()

    def create_widgets(self):
        self.top_frame()
        self.centre_frame()
        self.bottom_frame()

    def top_frame(self):
        self.frame_title.grid_propagate(0)
        self.frame_title.grid(column=0, row=0, sticky='snew')
        Label(self.frame_title, bg=BACKGROUND, fg='black', text='Wordle', font=('Cooper Black', 25, 'bold')).pack(side='top')
        # Label(self.frame_title, bg=BACKGROUND, fg='black', text=self.word, font=('Arial', 10, 'bold')).pack(side='left')

    def centre_frame(self):
        self.frame_squares.grid_propagate(0)
        self.frame_squares.grid(column=0, row=1, sticky='snew')

        for i in range(MAX_GUESSES):
            for j in range(WORD_LENGTH):
                self.squares[i][j] = Label(self.frame_squares, width=2, height=1, fg='white', bg=BACKGROUND, text="",
                                           font=('Arial', 25, 'bold'), borderwidth=2, relief="groove")
                self.squares[i][j].grid(row=i, column=j, padx=5, pady=5)

    def bottom_frame(self):
        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='snew')
        play_wordle_button = Button(self.frame_control, bg=Green, fg='white', text="Play Wordle", font=('Arial', 10), command=lambda: self.play_wordle_game())
        play_wordle_button.grid(row=0, column=0, padx=5, pady=5)
        self.chose_word = Text(self.frame_control, height=1, width=10, bg=BACKGROUND, fg='black', font=('Arial', 10),
                               borderwidth=2, relief="groove")
        self.chose_word.grid(row=1, column=0, padx=5, pady=10)
        chose_word_button = Button(self.frame_control, text="Choose word to guess", font=('Arial', 10), command=lambda: self.choose_word())
        chose_word_button.grid(row=1, column=1, padx=5, pady=10)

    def play_wordle_game(self):
        guess_history = []
        for g in range(MAX_GUESSES):  # Up to 6 guesses
            guess = self.competitor.guess(guess_history)
            if self.guess_is_legal(guess):
                guess_result = []

                for letter in range(WORD_LENGTH):

                    self.squares[g][letter].config(text=guess[letter].upper())

                    if guess[letter] not in self.word:
                        self.squares[g][letter]['bg'] = Grey
                        guess_result.append(LetterInformation.NOT_PRESENT)
                    elif self.word[letter] == guess[letter]:
                        self.squares[g][letter]['bg'] = Green
                        guess_result.append(LetterInformation.CORRECT)
                    else:
                        self.squares[g][letter]['bg'] = Yellow
                        guess_result.append(LetterInformation.PRESENT)

                guess_history.append((guess, guess_result))

                # self.num_guesses += 1
                if g <= MAX_GUESSES-1 and self.word == guess:
                    messagebox.showinfo('YOU WIN', 'Congratulations')
                    self.update_labels()
                    self.word = random.choice(self.words)
                    break
                if g == MAX_GUESSES-1 and self.word != guess:
                    messagebox.showinfo('YOU LOSE', 'Try again')
                    self.update_labels()
                    self.word = random.choice(self.words)
                    break

    def guess_is_legal(self, guess):
        if len(guess) == 5 and guess.lower() == guess and guess in self.words:
            return True
        else:
            return False

    def update_labels(self):
        for i in range(MAX_GUESSES):
            for j in range(WORD_LENGTH):
                self.squares[i][j].config(text="", bg=BACKGROUND, fg='white', borderwidth=2, relief="groove")

    def choose_word(self):
        self.word = self.chose_word.get("1.0", "end-1c")
        if len(self.word) != WORD_LENGTH:
            self.word = random.choice(self.words)


if __name__ == "__main__":
    window = Tk()
    window.config(bg=BACKGROUND)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file="images/logo.png"))
    window.geometry('300x500')
    window.resizable(0, 0)
    window.title('Wordle')
    app = GUIWordle(window)
    app.mainloop()
