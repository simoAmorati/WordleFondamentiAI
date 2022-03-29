from tkinter import Tk, Button, Entry, Label, messagebox, PhotoImage
from tkinter import StringVar, Frame
# import random


class GUIWordle(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.frame_title = Frame(self.master, bg='black', width=400, height=100)
        self.frame_squares = Frame(self.master, bg='black', width=400, height=350)
        self.row = 0
        self.green = '#538d4e'
        self.yellow = '#c9b458'
        self.grey = '#86888a'
        self.text = StringVar()
        self.text.trace("w", lambda *args: self.limit(self.text))
        self.create_widgets()

    def create_widgets(self):
        self.frame_title.grid_propagate(0)
        self.frame_title.grid(column=0, row=0, sticky='snew')
        self.frame_squares.grid_propagate(0)
        self.frame_squares.grid(column=0, row=1, sticky='snew')

        Label(self.frame_title, bg='black', fg='white', text='Wordle', font=('Arial', 25, 'bold')).pack(side='top')

    @staticmethod
    def limit(text):
        if len(text.get()) > 0:
            text.set(text.get()[:5])


if __name__ == "__main__":
    window = Tk()
    window.config(bg='black')
    # window.call('wm', 'iconphoto', window._w, PhotoImage(file='logo.png'))
    window.geometry('410x440+500+50')
    window.resizable(0, 0)
    window.title('Wordle')
    app = GUIWordle(window)
    app.mainloop()
