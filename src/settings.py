import tkinter, ntkutils
from tkinter import E, ttk, font
import config

cfg = config.cfg
page = ""

def appearance():
    global box1, box2, page

    if not page == "":
        savechanges()

    clearstates()
    btnappearence.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    page = "appearance"

    lbl1 = tkinter.Label(frameright, text="Theme:").place(x=10, y=12)
    box1 = ttk.Combobox(frameright, values=["Dark", "Light", "System"], state="readonly")
    box1.set(cfg["theme"])
    box1.pack(padx=10, pady=10, anchor=E)

    lbl2 = tkinter.Label(frameright, text="Font:").place(x=10, y=67)
    box2 = ttk.Combobox(frameright, textvariable=font, state="readonly", values=fonts)
    box2.set(cfg["font"])
    box2.pack(padx=10, pady=10, anchor=E)

def experimental():
    global page

    savechanges()

    clearstates()
    btnexperimental.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    page = "experimental"

    lbl1 = tkinter.Label(frameright, text="Experimental features go here").pack(pady=10)

def savechanges():
    if page == "appearance":
        cfg["theme"] = box1.get()
        cfg["font"] = box2.get()
    elif page == "experimental":
        pass

def exit_():
    global page
    
    ntkutils.cfgtools.SaveCFG(cfg)
    page = ""
    settings.destroy()

def build():
    global frameright, frameleft, btnappearence, btnexperimental, settings

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

    btnapply = ttk.Button(frameleft, text="Apply", style="Accent.TButton", width=20, command=exit_).pack(side=tkinter.BOTTOM, pady=10)

    getfonts()
    appearance()

def clearstates():
    for i in frameleft.pack_slaves():
        i.configure(style="TButton")

def getfonts():
    global fonts
    fonts=list(font.families())
    fonts.sort()
