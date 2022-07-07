import tkinter, ntkutils
from tkinter import E, N, W, ttk, font

import config

def appearance():
    global boxtheme, boxfont, boxsize, page

    savechanges()
    clearstates()

    btnappearence.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    page = "appearance"

    lbltheme = tkinter.Label(frameright, text="Theme:").place(x=10, y=12)
    boxtheme = ttk.Combobox(frameright, values=["Dark", "Light", "System"], state="readonly", width=25)
    boxtheme.set(cfg["theme"])
    boxtheme.pack(padx=10, pady=10, anchor=E)

    lblfont = tkinter.Label(frameright, text="Font:").place(x=10, y=67)
    boxfont = ttk.Combobox(frameright, state="readonly", values=fonts, width=15)
    boxfont.set(cfg["font"])
    boxfont.pack(padx=80, pady=10, anchor=E)
    boxsize = ttk.Entry(frameright, width=5)
    boxsize.insert(0, cfg["font-size"])
    boxsize.place(x=260, y=63)

def experimental():
    global page, btnmica, btnhotkeys

    savechanges()

    clearstates()
    btnexperimental.configure(style="Accent.TButton")
    ntkutils.clearwin(frameright)

    page = "experimental"

    lblmica = tkinter.Label(frameright, text="Mica Blur:").place(x=10, y=12)
    btnmica = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnmica.pack(padx=10, pady=10, anchor=E)
    btnmica.state(["!alternate"])
    if cfg["mica"]: btnmica.state(["!alternate", "selected"])
    micainfo = tkinter.Label(frameright, text="When switching from dark to light theme with this\noption enabled, you have to perform a restart!", justify="left", fg="grey").place(x=10, y=42)

    lblhotkeys = tkinter.Label(frameright, text="Enable Hotkeys: (Buggy) [needs restart]").place(x=10, y=112)
    btnhotkeys = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnhotkeys.pack(padx=10, pady=65, anchor="e")
    btnhotkeys.state(["!alternate"])
    if cfg["hotkeys"]: btnhotkeys.state(["!alternate", "selected"])

def savechanges():
    if page == "appearance":
        cfg["theme"] = boxtheme.get()
        cfg["font"] = boxfont.get()
        cfg["font-size"] = boxsize.get()
    elif page == "experimental":
        cfg["mica"] = btnmica.instate(["selected"])
        cfg["hotkeys"] = btnhotkeys.instate(["selected"])

def apply():
    global page, save

    savechanges()

    ntkutils.cfgtools.SaveCFG(cfg)
    save = True
    settings.destroy()


def build():
    global frameright, frameleft, btnappearence, btnexperimental, settings, page, cfg, save

    cfg = config.get()
    page = ""
    save = False

    settings = tkinter.Toplevel()
    ntkutils.windowsetup(settings, "txt2 - Settings", "assets/logo.png", False, "500x400")
    ntkutils.dark_title_bar(settings)

    frameleft = tkinter.Frame(settings, width=175, bg="#202020")
    frameleft.pack(side=tkinter.LEFT, fill="y")
    frameleft.pack_propagate(False)

    if not cfg["theme"] == "Dark":
        frameleft.configure(bg="#f3f3f3")

    frameright = tkinter.Frame(settings, width=325)
    frameright.pack(side=tkinter.LEFT, fill="both")
    frameright.pack_propagate(False)

    btnappearence = ttk.Button(frameleft, text="Appearence", style="Accent.TButton", width=20, command=appearance)
    btnappearence.pack(pady=10)
    btnexperimental = ttk.Button(frameleft, text="Experimental Features", width=20, command=experimental)
    btnexperimental.pack()

    btnapply = ttk.Button(frameleft, text="Apply", style="Accent.TButton", width=20, command=apply)
    btnapply.pack(side=tkinter.BOTTOM, pady=10)

    getfonts()
    appearance()

def clearstates():
    for i in frameleft.pack_slaves():
        i.configure(style="TButton")

def getfonts():
    global fonts
    fonts=list(font.families())
    fonts.sort()
