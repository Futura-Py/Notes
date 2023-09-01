from tkinter import Menu, Tk

from sv_ttk import SunValleyTtkTheme

from editor import Manager


class App(Tk):
    def __init__(self):
        super().__init__()

        SunValleyTtkTheme.initialized = False
        SunValleyTtkTheme.set_theme("dark")

        self.h = self.winfo_screenheight() - 200
        self.w = self.winfo_screenwidth() - 100
        self.x = int((self.winfo_screenwidth() - self.w) / 2)
        self.y = int((self.winfo_screenheight() - self.h - 75) / 2)

        self.geometry("{}x{}+{}+{}".format(self.w, self.h, self.x, self.y))

        self.manager = Manager(self)
        self.manager.pack(fill="both", expand=True)
        self.menubar = Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, tearoff=False, bg="white")

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="New", command=lambda:self.manager.newtab(), foreground="black")
        self.filemenu.add_command(label="Open", command=self.manager.openfile, foreground="black")



if __name__ == "__main__":
    main = App()
    main.mainloop()
