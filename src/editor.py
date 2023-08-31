from tkinter.ttk import Notebook, Style
from tkinter import Frame
from tkinter.font import Font
from chlorophyll import CodeView
from tklinenums import TkLineNumbers
from pygments.lexers import TextLexer

class Manager(Notebook):
    def __init__(self, *args):
        super().__init__(*args)

    def newtab(self, name):
        self.add(Editor(), text=name)

class Editor(Frame):
    def __init__(self, *args):
        super().__init__(*args)

        self.footer = Frame(self, width=self.winfo_width(), height=25)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.text = CodeView(self, bg="#1c1c1c", lexer=TextLexer)
        self.text._set_color_scheme("ayu-dark")
        self.text.pack(side="right", fill="both", expand=True)
        self.text._hs.grid_remove()

        self.linenumbersstyle = Style()
        self.linenumbersstyle.configure("TLineNumbers", background="#1c1c1c", foreground="white")
        self.linenumbersfont = Font(family="Courier New bold", name="TkLineNumsFont")

        self.linenumbers = TkLineNumbers(self, self.text, "right")
        self.linenumbers.pack(side="left", fill="y")
        self.linenumbers.configure(borderwidth=0)

        self.text.bind("<Return>", lambda event: self.after_idle(self.linenumbers.redraw), add=True)
        self.text.bind("<BackSpace>", lambda event: self.after_idle(self.linenumbers.redraw), add=True)
        self.text.bind("<Control-v>", lambda event: self.after_idle(self.linenumbers.redraw), add=True)

        self.text["yscrollcommand"] = self.linenumbers.redraw
        self.text._line_numbers.destroy()
        self.text._line_numbers = self.linenumbers
