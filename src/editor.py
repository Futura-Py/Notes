from tkinter.ttk import Notebook
from tkinter import _Cursor, _Relief, _ScreenUnits, _TakeFocusValue, Frame, Misc
from typing import Any
from typing_extensions import Literal

class Manager(Notebook):
    def __init__(self, *args):
        super().__init__(*args)

    def newtab(self, name):
        self.add(Editor, text=name)

class Editor(Frame):
    def __init__(self, *args):
        super().__init__(*args)