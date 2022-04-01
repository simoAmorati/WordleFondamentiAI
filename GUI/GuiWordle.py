import random
import time

from tkinter import Tk, Button, Entry, Label, messagebox, PhotoImage
from tkinter import StringVar, Frame
# import random
from LetterPositionInformation import LetterInformation
from WordList import WordList
from WordleAISofia import WordleAISofia

MAX_GUESSES = 6
WORD_LENGTH = 5
BACKGROUND = '#fafafa'

class GUIWordle(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.wordlist_filename = "\\data\\combined_wordlist.txt"
        self.wordlist = WordList(self.wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = WordleAISofia(self.words)
        self.word = random.choice(self.words)
        """self.guess_history = []"""
        self.num_guesses = 0

        self.frame_control = Frame(self.master, bg=BACKGROUND, width=400, height=100)
        self.frame_title = Frame(self.master, bg=BACKGROUND, width=400, height=100)
        self.frame_squares = Frame(self.master, bg=BACKGROUND, width=400, height=350)
        self.row = 0
        self.green = '#538d4e'
        self.yellow = '#c9b458'
        self.grey = '#86888a'
        self.text = StringVar()
        self.create_widgets()
        self.squares = Label()


    def create_widgets(self):
        self.frame_title.grid_propagate(0)
        self.frame_title.grid(column=0, row=0, sticky='snew')
        self.frame_squares.grid_propagate(0)
        self.frame_squares.grid(column=0, row=1, sticky='snew')

        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='snew')

        Label(self.frame_title, fg='black', text='Wordle', font=('Arial', 25, 'bold')).pack(side='top')
        self.play_game()


    def play_game(self):

        guess_history = []
        for g in range(MAX_GUESSES):  # Up to 6 guesses
            guess = self.competitor.guess(guess_history)
            if self.guess_is_legal(guess):
                guess_result = []

                for letter in range(WORD_LENGTH):
                    squares = Label(self.frame_squares, width=3, fg='white',
                                         bg=self.grey, text=guess[letter].upper(), font=('Geometr706 BlkCn BT', 25, 'bold'))
                    squares.grid(column=letter, row=g, padx=5, pady=5)

                    if guess[letter] not in self.word:
                        squares['bg'] = self.grey
                        guess_result.append(LetterInformation.NOT_PRESENT)
                    elif self.word[letter] == guess[letter]:
                        squares['bg'] = self.green
                        guess_result.append(LetterInformation.CORRECT)
                    else:
                        squares['bg'] = self.yellow
                        guess_result.append(LetterInformation.PRESENT)

                guess_history.append((guess, guess_result))

                #self.num_guesses += 1
                if g <= MAX_GUESSES and self.word == guess:
                    messagebox.showinfo('YOU WIN', 'Congratulations')
                    self.master.destroy()
                    self.master.quit()
                if g == MAX_GUESSES and self.word != guess:
                    messagebox.showinfo('YOU LOSE', 'Try again')
                    self.master.destroy()
                    self.master.quit()

    def guess_is_legal(self, guess):
        if len(guess) == 5 and guess.lower() == guess and guess in self.words:
            return True
        else:
            return False




if __name__ == "__main__":
    window = Tk()
    window.config(bg=BACKGROUND)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file='C:\\Users\\sofia\\IdeaProjects\\WordleFondamentiAI\\images\\Wordle_NYT_logo.svg.png'))
    window.geometry('410x440+500+50')
    window.resizable(0, 0)
    window.title('Wordle')
    app = GUIWordle(window)
    app.mainloop()
