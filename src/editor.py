from os.path import basename, isfile
from tkinter import Frame, Label, PhotoImage
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.ttk import Button, Notebook, Scrollbar, Style
from toml import load

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

        self.home = Frame(self)
        self.title = Label(self.home, text="Futura Notes", font=("Segoe UI", 20, "bold")).pack(anchor="nw", padx=20, pady=20)
        self.btncreatenew = Button(self.home, text="Create New File", command=self.newtab).pack(anchor="nw", padx=20)
        self.btnopen = Button(self.home, text="Open File", command=self.openfile).pack(anchor="nw", padx=20, pady=20)
        self.add(self.home, text="Home", image=self.closeimg, compound="right")

        self.bind("<Button-1>", self.on_click, add=True)

    def newtab(self, file=None):
        self.add(Editor(file), text="Untitled" if file==None else basename(file.name), image=self.closeimg, compound="right")
        self.select(self.tabs()[-1]) # Select newly opened tab

    def openfile(self):
        self.file = askopenfile()
        self.newtab(self.file)
        self.file.close()

    def save(self):
        self.editor = self.nametowidget(self.select()) # Retrieves Editor Object of currently opened Tab
        self.filetosave = self.editor.filedir.cget("text")
        if isfile(self.filetosave):
            self.file2 = open(self.filetosave, "w")
            self.file2.write(self.editor.text.get("1.0", "end"))
            self.file2.close()
        else:
            self.saveas()

    def saveas(self):
        self.editor = self.nametowidget(self.select())
        self.file3 = asksaveasfile()
        if self.file3 != None:
            self.file3.write(self.editor.text.get("1.0", "end"))
            self.editor.filedir.configure(text=self.file3.name)
            self.tab(self.select(), text=basename(self.file3.name))
            self.file3.close()
    

    # The next two functions are heavily inspired by Akuli:
    # https://github.com/Akuli/porcupine/blob/main/porcupine/plugins/tab_closing.py
    def closetab(self, event):
        self.before = self.index(f"@{event.x},{event.y}")
        self.after = self.before + 1
        self.forget(self.tabs()[self.before:self.after][0])
        if len(self.tabs()) == 0: self.master.destroy()

    def on_click(self, event) -> None:
        self.update_idletasks()
        if event.widget.identify(event.x, event.y) == "label":
            # find the right edge of the top label (including close button)
            right = event.x
            while event.widget.identify(right, event.y) == "label":
                right += 1

            # hopefully the image is on the right edge of the label and there's no padding :O
            if event.x >= right - self.closeimg.width():
                self.closetab(event)


class Editor(Frame):
    def __init__(self, file, *args):
        super().__init__(*args)

        self.footer = Frame(self, width=self.winfo_width(), height=25)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.filedir = Label(self.footer, text="unsaved")
        self.filedir.pack(side="left")

        self.text = CodeView(self, lexer=TextLexer)
        self.text.pack(side="right", fill="both", expand=True)
        self.text._hs.grid_remove()

        self.color_scheme = load("src/dark.toml")
        self.text._set_color_scheme(self.color_scheme)

        self.text._line_numbers.configure(borderwidth=0)

        if file != None:
            self.text.insert("1.0", file.read())
            self.filedir.configure(text=file.name)
            file.close()


