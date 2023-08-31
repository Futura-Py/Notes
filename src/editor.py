from tkinter import Frame, Label, PhotoImage
from tkinter.font import Font
from tkinter.ttk import Notebook, Style

from chlorophyll import CodeView
from pygments.lexers import TextLexer
from tklinenums import TkLineNumbers


class Manager(Notebook):
    def __init__(self, *args):
        super().__init__(*args)

        # Remove dotted line :O
        self.style = Style()
        self.style.configure("TNotebook.Tab", focuscolor=self.style.configure(".")["background"])

        self.closeimg = PhotoImage(file="assets/close_light.png")

        self.bind("<Button-1>", self.on_click, add=True)

    def newtab(self, name):
        self.add(Editor(), text=name, image=self.closeimg, compound="right")

    def closetab(self, event):
        print("close tab")

    def on_click(self, event) -> None:
        if event.widget.identify(event.x, event.y) == "label":
            # find the right edge of the top label (including close button)
            right = event.x
            while event.widget.identify(right, event.y) == "label":
                right += 1

            # hopefully the image is on the right edge of the label and there's no padding :O
            if event.x >= right - self.closeimg.width():
                self.closetab(event)


class Editor(Frame):
    def __init__(self, *args):
        super().__init__(*args)

        self.footer = Frame(self, width=self.winfo_width(), height=25)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.filedir = Label(self.footer, text="unsaved")
        self.filedir.pack(side="left")

        self.text = CodeView(self, bg="#1c1c1c", lexer=TextLexer)
        self.text._set_color_scheme("ayu-dark")
        self.text.pack(side="right", fill="both", expand=True)
        self.text._hs.grid_remove()

        self.style = Style()
        self.style.configure("TLineNumbers", background="#1c1c1c", foreground="white")
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
