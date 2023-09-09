from tkinter import Menu, Tk, PhotoImage

from sv_ttk import set_theme

from editor import Manager
from platform import system

if system() == "Linux": LINUX = True
else: LINUX = False

theme = "dark"

class App(Tk):
    def __init__(self):
        super().__init__()

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

    def openpreview(self):
        self.manager.openpreview()
        if self.manager.getcurrentchild().ispreviewed: self.filemenu.entryconfigure(6, image=self.checkimg)
        else: self.filemenu.entryconfigure(6, image="")



if __name__ == "__main__":
    main = App()
    main.mainloop()
