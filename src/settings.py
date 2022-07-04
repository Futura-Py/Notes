import tkinter, ntkutils
from tkinter import E, RIDGE, ttk, font

def appearance():
    clearstates()
    btnappearence.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    lbl1 = tkinter.Label(frameright, text="Theme:").place(x=10, y=12)
    theme = tkinter.StringVar(value="Dark")
    box1 = ttk.Combobox(frameright, values=["Dark", "Light", "System"], textvariable=theme, state="readonly").pack(padx=10, pady=10, anchor=E)
    def resettheme(*args): theme.set("Dark")
    theme.trace("w", resettheme)

    lbl2 = tkinter.Label(frameright, text="Font:").place(x=10, y=67)
    font = tkinter.StringVar(value="Courier New")
    box2 = ttk.Combobox(frameright, textvariable=font, state="readonly", values=fonts).pack(padx=10, pady=10, anchor=E)
    def resetfont(*args): font.set("Courier New")
    font.trace("w", resetfont)

def experimental():
    clearstates()
    btnexperimental.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    btn1 = ttk.Button(frameright, text="I am another button").pack()

def build():
    global frameright, frameleft, btnappearence, btnexperimental

    settings = tkinter.Toplevel()
    ntkutils.windowsetup(settings, "txt2 - Settings", "assets/logo.png", False, "500x400")
    ntkutils.dark_title_bar(settings)

    frameleft = tkinter.Frame(settings, width=175, bg="#202020")
    frameleft.pack(side=tkinter.LEFT, fill="y")
    frameleft.pack_propagate(False)

    frameright = tkinter.Frame(settings, width=325)
    frameright.pack(side=tkinter.LEFT, fill="both")
    frameright.pack_propagate(False)

    btnappearence = ttk.Button(frameleft, text="Appearence", style="Accent.TButton", width=20, command=appearance)
    btnappearence.pack(pady=10)
    btnexperimental = ttk.Button(frameleft, text="Experimental Features", width=20, command=experimental)
    btnexperimental.pack()

    getfonts()
    appearance()

def clearstates():
    for i in frameleft.pack_slaves():
        i.configure(style="TButton")

def getfonts():
    global fonts
    fonts=list(font.families())
    fonts.sort()
