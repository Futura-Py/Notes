from os.path import isfile
from tkinter import Menu, PhotoImage, Toplevel, Label
from tkinter.ttk import Entry
from tkinterdnd2 import Tk, DND_FILES

from sv_ttk import set_theme

from editor import Manager
from platform import system

if system() == "Linux": LINUX = True
else: LINUX = False

theme = "dark"

class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Futura Notes")
        set_theme(theme)

        self.checkimg = PhotoImage(file="assets/check_{}.png".format(theme))

        self.h = self.winfo_screenheight() - 200
        self.w = self.winfo_screenwidth() - 100
        self.x = int((self.winfo_screenwidth() - self.w) / 2)
        self.y = int((self.winfo_screenheight() - self.h - 75) / 2)

        self.geometry("{}x{}+{}+{}".format(self.w, self.h, self.x, self.y))

        self.manager = Manager(theme, self)
        self.manager.pack(fill="both", expand=True)
        self.menubar = Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, tearoff=False)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="New", command=self.manager.newtab, foreground="white" if LINUX and theme == "dark" else "black")
        self.filemenu.add_command(label="Open", command=self.manager.openfile, foreground="white" if LINUX and theme == "dark" else "black")
        self.filemenu.add_command(label="Save", command=self.manager.save, foreground="white" if LINUX and theme == "dark" else "black")
        self.filemenu.add_command(label="Save As", command=self.manager.saveas, foreground="white" if LINUX and theme == "dark" else "black")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Preview", command=self.openpreview, foreground="white" if LINUX and theme == "dark" else "black", compound="right")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Properties", command=self.openproperties, foreground="white" if LINUX and theme == "dark" else "black")

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.filedrop)

    def openpreview(self):
        self.manager.openpreview()
        if self.manager.getcurrentchild().ispreviewed: self.filemenu.entryconfigure(6, image=self.checkimg)
        else: self.filemenu.entryconfigure(6, image="")

    def filedrop(self, event):
        self.file = open(event.data.replace("{", "").replace("}", ""), "r")
        self.manager.newtab(self.file)
        self.file.close()

    def openproperties(self):
        self.filetoopen = self.manager.getcurrentchild().filedir.cget("text")
        if isfile(self.filetoopen): 
            self.properties = Properties(self.filetoopen, self)

class Properties(Toplevel):
    def __init__(self, file, *args):
        super().__init__(*args)

        self.title("File Properties")
        self.geometry("350x400")
        self.resizable(False, False)

        self.imagefile = "assets/filetypes/{}_{}.png".format(file.split(".")[-1], theme)
        if isfile(self.imagefile): self.image = PhotoImage(file=self.imagefile)
        else: self.image = PhotoImage(file="assets/filetypes/other_{}.png".format(theme))
        self.imagelabel = Label(self, image=self.image).place(x=5, y=5)

        self.filename = Entry(self, width=25)
        self.filename.insert(0, file.split("/")[-1])
        self.filename.pack(anchor="ne", padx=15, pady=20)

        self.filepath = Label(self, text="/".join(file.split("/")[:-1]), font=("Segoe UI", 10), width=27, anchor="w")
        self.filepath.pack(anchor="ne", padx=15)


if __name__ == "__main__":
    main = App()
    main.mainloop()
