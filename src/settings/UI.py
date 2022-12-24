import tkinter
from tkinter import font, ttk

import darkdetect
import ntkutils
import sv_ttk

import config
import vars as v
from generatesize import system
import utils as u

options = [
    "Theme",
    "Font",
    "Font Size",
    "Display Line Numbers",
    "Syntax Highlighting",
    "Hotkeys",
    "Mica Blur",
]

options2 = {
    "Theme": "appearance",
    "Font": "appearance",
    "Font Size": "appearance",
    "Display Line Numbers": "general",
    "Syntax Highlighting": "general",
    "Hotkeys": "hotkeys",
    "Mica Blur": "experimental",
    "On Close": "general",
}

def general():
    global page, btnnumbers, btnhighlight, boxonclose

    savechanges()
    clearstates()

    btngeneral.configure(style="Accent.TButton")
    if u.dark(): btngeneral.configure(image=v.settings_dark)
    else: btngeneral.configure(image=v.settings_light)

    ntkutils.clearwin(frameright)

    page = "general"

    lblonclose = tkinter.Label(frameright, text="On Close:").place(x=10, y=15)
    boxonclose = ttk.Combobox(frameright, values=["Do Nothing", "Save", "Ask"], state="readonly", width=25)
    boxonclose.set(cfg["onclose"])
    boxonclose.pack(padx=10, pady=10, anchor="e")

    lblnumbers = tkinter.Label(frameright, text="Display line numbers:").place(x=10, y=60)
    btnnumbers = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnnumbers.pack(padx=10, pady=10, anchor="e")
    btnnumbers.state(["!alternate"])
    if cfg["linenumbers"]: btnnumbers.state(["!alternate", "selected"])

    lblhighlight = tkinter.Label(frameright, text="Syntax Highlighting:").place(x=10, y=115)
    btnhighlight = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnhighlight.pack(padx=10, pady=15, anchor="e")
    btnhighlight.state(["!alternate"])
    if cfg["syntax-highlighting"]: btnhighlight.state(["!alternate", "selected"])

def appearance():
    global boxtheme, boxfont, boxsize, page

    savechanges()
    clearstates()

    btnappearence.configure(style="Accent.TButton", image=eval("v.brush_" + sv_ttk.get_theme()))

    ntkutils.clearwin(frameright)

    page = "appearance"

    lbltheme = tkinter.Label(frameright, text="Theme:").place(x=10, y=15)
    boxtheme = ttk.Combobox(frameright, values=["Dark", "Light", "System"], state="readonly", width=25)
    boxtheme.set(cfg["theme"])
    boxtheme.pack(padx=10, pady=10, anchor="e")

    lblfont = tkinter.Label(frameright, text="Font:").place(x=10, y=60)
    boxfont = ttk.Combobox(frameright, state="readonly", values=fonts, width=15)
    boxfont.set(cfg["font"])
    boxfont.pack(padx=70, pady=10, anchor="e")
    boxsize = ttk.Entry(frameright, width=5)
    boxsize.insert(0, cfg["font-size"])
    boxsize.place(x=265, y=58)


def experimental():
    global page, btnmica, btnhotkeys

    savechanges()
    clearstates()

    btnexperimental.configure(style="Accent.TButton", image=eval("v.warn_" + sv_ttk.get_theme()))

    ntkutils.clearwin(frameright)

    page = "experimental"

    lblmica = tkinter.Label(frameright, text="Mica Blur:").place(x=10, y=12)
    btnmica = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnmica.pack(padx=10, pady=10, anchor="e")
    btnmica.state(["!alternate"])
    if cfg["mica"]: btnmica.state(["!alternate", "selected"])


def hotkeys():
    global page, entryopen, entrysave

    savechanges()
    clearstates()

    btnhotkeys.configure(style="Accent.TButton", image=eval("v.keyboard_" + sv_ttk.get_theme()))

    ntkutils.clearwin(frameright)

    page = "hotkeys"

    lblopen = tkinter.Label(frameright, text="Open:").place(x=10, y=12)
    entryopen = ttk.Entry(frameright, width=25)
    entryopen.insert(0, cfg["hkey-open"])
    entryopen.pack(padx=10, pady=10, anchor="e")

    lblsave = tkinter.Label(frameright, text="Save:").place(x=10, y=67)
    entrysave = ttk.Entry(frameright, width=25)
    entrysave.insert(0, cfg["hkey-save"])
    entrysave.pack(padx=10, pady=10, anchor="e")


def savechanges():
    if page == "general":
        cfg["linenumbers"] = btnnumbers.instate(["selected"])
        cfg["syntax-highlighting"] = btnhighlight.instate(["selected"])
        cfg["onclose"] = boxonclose.get()

        if u.dark(): btngeneral.configure(image=v.settings_light)
        else: btngeneral.configure(image=v.settings_dark)
    elif page == "appearance":
        cfg["theme"] = boxtheme.get()
        cfg["font"] = boxfont.get()
        cfg["font-size"] = boxsize.get()

        if u.dark(): btnappearence.configure(image=v.brush_light)
        else: btnappearence.configure(image=v.brush_dark)
    elif page == "experimental":
        cfg["mica"] = btnmica.instate(["selected"])

        if u.dark(): btnexperimental.configure(image=v.warn_light)
        else: btnexperimental.configure(image=v.warn_dark)
    elif page == "hotkeys":
        cfg["hkey-open"] = entryopen.get()
        cfg["hkey-save"] = entrysave.get()

        if u.dark(): btnhotkeys.configure(image=v.keyboard_light)
        else: btnhotkeys.configure(image=v.keyboard_dark)


def apply():
    global page, save

    savechanges()

    ntkutils.cfgtools.SaveCFG(cfg)
    settings.destroy()


def build():
    global frameright, frameleft, btnappearence, btnexperimental, btnhotkeys, settings, page, cfg, btngeneral

    cfg = config.get()
    page = ""

    settings = tkinter.Toplevel()
    ntkutils.windowsetup(settings, "Futura Notes - Settings", "assets/logo.png", False, "500x400")
    if system != "Darwin" and u.dark():
        ntkutils.dark_title_bar(settings)

    frameleft = tkinter.Frame(settings, width=175, bg=v.theme["secondary"])
    frameleft.pack(side=tkinter.LEFT, fill="y")
    frameleft.pack_propagate(False)

    frameright = tkinter.Frame(settings, width=325)
    frameright.pack(side=tkinter.LEFT, fill="both")
    frameright.pack_propagate(False)

    def update(data):
        menu.delete(0, "end")
        for value in data:
            menu.insert("end", value)
        menu.configure(height=len(data))

    def check(e):
        v = search.get()
        if v == "":
            data = options
        else:
            data = []
            for item in options:
                if v.lower() in item.lower():
                    data.append(item)
        update(data)

    def showlist(e):
        search.delete(0, "end")
        menu.bind("<<ListboxSelect>>", onselect)
        menu.place(x=search.winfo_x(), y=search.winfo_y() + search.winfo_height())
        check("")

    def removelist(e):
        menu.unbind("<<ListboxSelect>>")
        menu.place(x=1000, y=1000)

    search = ttk.Entry(frameleft, width=23)
    search.pack(pady=10)
    search.bind("<KeyRelease>", check)
    search.update()
    search.bind("<FocusIn>", showlist)
    search.bind("<FocusOut>", removelist)
    search.insert(0, "Search for a setting...")

    def onselect(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        func = eval(options2[value])
        func()

    btngeneral = ttk.Button(frameleft, text="General", width=14, command=general, image=v.settings_dark, compound="left")
    btngeneral.pack(pady=10)

    btnappearence = ttk.Button(frameleft, text="Appearence", width=14, command=appearance, image=v.brush_dark, compound="left")
    btnappearence.pack()

    btnhotkeys = ttk.Button(frameleft, text="Hotkeys", width=14, command=hotkeys, image=v.keyboard_dark, compound="left")
    btnhotkeys.pack(pady=10)

    btnexperimental = ttk.Button(frameleft, text="Unstable Features", width=14, command=experimental, image=v.warn_dark, compound="left")
    btnexperimental.pack()

    btnapply = ttk.Button(frameleft, text="Apply", style="Accent.TButton", width=18, command=apply)
    btnapply.pack(side="bottom", pady=10)

    lblrestart = tkinter.Label(frameleft, text="Restart required!", wraplength=170, fg="grey", bg=v.theme["secondary"]).pack(side="bottom")

    menu = tkinter.Listbox(frameleft, width=23)
    menu.bind("<<ListboxSelect>>", onselect)

    if u.dark():
        btngeneral.configure(image=v.settings_light)
        btnappearence.configure(image=v.brush_light)
        btnhotkeys.configure(image=v.keyboard_light)
        btnexperimental.configure(image=v.warn_light)

    getfonts()
    general()


def clearstates():
    for i in frameleft.pack_slaves():
        try:
            i.configure(style="TButton")
        except:
            pass


def getfonts():
    global fonts
    fonts = list(font.families())
    fonts.sort()
