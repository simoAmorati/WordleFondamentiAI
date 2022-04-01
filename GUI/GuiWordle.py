import random
from tkinter import Tk, Button, Entry, Label, messagebox, PhotoImage
from tkinter import StringVar, Frame
# import random
from LetterPositionInformation import LetterInformation
from WordList import WordList
from WordleAISofia import WordleAISofia

MAX_GUESSES = 6
WORD_LENGTH = 5


class GUIWordle(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.wordlist_filename = "data/combined_wordlist.txt"
        self.wordlist = WordList(self.wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitor = WordleAISofia(self.words)
        self.word = random.choice(self.words)

        self.frame_control = Frame(self.master, bg='black', width=400, height=100)
        self.frame_title = Frame(self.master, bg='black', width=400, height=100)
        self.frame_squares = Frame(self.master, bg='black', width=400, height=350)
        self.row = 0
        self.green = '#538d4e'
        self.yellow = '#c9b458'
        self.grey = '#86888a'
        self.text = StringVar()
        self.create_widgets()
        self.num_guesses = 0

    def create_widgets(self):
        self.frame_title.grid_propagate(0)
        self.frame_title.grid(column=0, row=0, sticky='snew')
        self.frame_squares.grid_propagate(0)
        self.frame_squares.grid(column=0, row=1, sticky='snew')

        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='snew')

        Label(self.frame_title, bg='black', fg='white', text='Wordle', font=('Arial', 25, 'bold')).pack(side='top')

        self.next = Button(self.frame_control, text='Nxt', bg='gray50', activebackground='green2',
                           fg='white', font=('Arial', 12, 'bold'), command=self.play_game)
        self.next.pack(side='left', expand=True)

    def play_game(self):

        guess_history = []

        if self.num_guesses < MAX_GUESSES:  # Up to 6 guesses
            guess = self.competitor.guess(guess_history)
            if self.guess_is_legal(guess):
                guess_result = []

                for letter in range(WORD_LENGTH):
                    self.squares = Label(self.frame_squares, width=4, fg='white',
                                         bg=self.grey, text=guess[letter], font=('Geometr706 BlkCn BT', 25, 'bold'))
                    self.squares.grid(column=letter, row=self.num_guesses, padx=5, pady=5)

                    if guess[letter] not in word:
                        self.squares['bg'] = self.grey
                        guess_result.append(LetterInformation.NOT_PRESENT)
                    elif word[letter] == guess[letter]:
                        self.squares['bg'] = self.yellow
                        guess_result.append(LetterInformation.CORRECT)
                    else:
                        self.squares['bg'] = self.green
                        guess_result.append(LetterInformation.PRESENT)
                guess_history.append((guess, guess_result))

                self.num_guesses += 1
                if self.num_guesses <= MAX_GUESSES and self.word == guess:
                    messagebox.showinfo('YOU WIN', 'Congratulations')
                    self.master.destroy()
                    self.master.quit()
                if self.num_guesses == MAX_GUESSES and self.word != guess:
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
    window.config(bg='black')
    # window.call('wm', 'iconphoto', window._w, PhotoImage(file='logo.png'))
    window.geometry('410x440+500+50')
    window.resizable(0, 0)
    window.title('Wordle')
    app = GUIWordle(window)
    app.mainloop()
