from tkinter import Tk, Label
from tkinter.ttk import Button
from sv_ttk import set_theme
from editor import Manager

class StartupWindow(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("250x300")
        self.withdraw()
        self.title("Futura Notes")
        self.resizable(False, False)
        set_theme("dark")
        self.update_idletasks()

        self.title = Label(self, text="Futura Notes", font=("Segoe UI", 20, "bold")).pack(anchor="nw", padx=20, pady=20)
        self.btncreatenew = Button(self, text="Create New File", command=self.openmainwindow).pack(anchor="nw", padx=20)

        self.deiconify()

    def openmainwindow(self):
        self.destroy()

class App(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.h = self.winfo_screenheight() - 200
        self.w = self.winfo_screenwidth() - 100
        self.x = int((self.winfo_screenwidth() - self.w) / 2)
        self.y = int((self.winfo_screenheight() - self.h - 75) / 2)

        self.geometry("{}x{}+{}+{}".format(self.w, self.h, self.x, self.y))
        self.deiconify()

        self.manager = Manager(self)
        self.manager.pack(fill="both", expand=True)



if __name__ == "__main__":
    start = StartupWindow()
    start.mainloop()
    main = App()
    main.mainloop()
