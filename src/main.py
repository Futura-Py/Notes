from tkinter import Label, Menu, Tk
from tkinter.font import Font
from tkinter.ttk import Button

from sv_ttk import SunValleyTtkTheme

from editor import Manager


class StartupWindow(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("250x300")
        self.withdraw()
        self.title("Futura Notes")
        self.resizable(False, False)
        SunValleyTtkTheme.set_theme("dark")
        self.update_idletasks()

        self.title = Label(self, text="Futura Notes", font=("Segoe UI", 20, "bold")).pack(anchor="nw", padx=20, pady=20)
        self.btncreatenew = Button(self, text="Create New File", command=self.openmainwindow).pack(anchor="nw", padx=20)

        self.deiconify()

    def openmainwindow(self):
        self.destroy()

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
        self.manager.newtab("Test")

        self.menubar = Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, tearoff=False, bg="white")

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="New", command=lambda:self.manager.newtab("Test"), foreground="black")



if __name__ == "__main__":
    start = StartupWindow()
    start.mainloop()
    main = App()
    main.mainloop()
