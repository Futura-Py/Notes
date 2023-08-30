from tkinter.ttk import Notebook
from tkinter import Frame

class Manager(Notebook):
    def __init__(self, *args):
        super().__init__(*args)

    def newtab(self, name):
        self.add(Editor, text=name)

class Editor(Frame):
    def __init__(self, *args):
        super().__init__(*args)