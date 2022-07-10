ver = "0.3"

import tkinter, sv_ttk, ntkutils
from tkinter import LEFT, filedialog, ttk
from pynput import keyboard
import darkdetect

import generatesize as size 
import filetype as f
import settings
import config

cfg = config.get()

root = tkinter.Tk()
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon="assets/logo.png")
ntkutils.placeappincenter(root)
root.update()

#region funcs
def applysettings():
    if cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
    else: sv_ttk.set_theme(cfg["theme"].lower())
    if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()): 
        ntkutils.dark_title_bar(root)
        tabbar.configure(bg="#202020")
    else: 
        tabbar.configure(bg="#f3f3f3")

    textwidget.configure(font=(cfg["font"], int(cfg["font-size"])))

    if cfg["mica"]: 
        if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()):
            ntkutils.blur_window_background(root, dark=True)
            textwidget.configure(bg="#1b1c1b")
        else:
            ntkutils.blur_window_background(root)
            textwidget.configure(bg="#fafbfa")

def changetype():
    if tabs[tabselected][2] == "unsaved":
        save()
    else:
        result = f.get(tabs[tabselected][2])
        tabs[tabselected][2] = result
        tabs[tabselected][0] = result.split("/")[-1]
        filedir.configure(text=result)

        buildtabs()
        updatetitle()

def settings_():
    global cfg

    settings.build()
    root.wait_window(settings.settings)
    
    if settings.save == True:
        cfg = settings.cfg
        applysettings()

def updatetitle():
    global tabselected

    root.title("txt2 - {} {}".format(tabs[tabselected][0], tabs[tabselected][3]))

def openfile():
    global tabselected

    file = filedialog.askopenfile()
    content = file.read()

    print(repr(textwidget.get("1.0", "end")))

    if not textwidget.get("1.0", "end").replace("\n", "") == "": 
        new()

    tabs[tabselected][0] = file.name.split("/")[-1]
    tabs[tabselected][2] = file.name
    tabs[tabselected][3] = ""

    file.close()

    textwidget.delete("1.0", "end")
    textwidget.insert("1.0", content)
    filedir.configure(text=tabs[tabselected][2])

    buildtabs()
    updatetitle()

def save(saveas=False):
    global tabselected

    if tabs[tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
    else:
        file = open(tabs[tabselected][2], "w")

    file.write(textwidget.get("1.0", "end"))
    tabs[tabselected][0] = file.name.split("/")[-1]
    tabs[tabselected][2] = file.name
    tabs[tabselected][3] = ""

    buildtabs()
    updatetitle()

def new():
    global tabselected

    tabs[tabselected][1] = textwidget.get("1.0", "end")
    textwidget.delete("1.0", "end")
    tabs.append(["Untitled", "", "unsaved", "*"])
    tabselected = len(tabbuttons)

    buildtabs()
    updatetitle

def opentab(x):
    global tabselected

    tabs[tabselected][1] = textwidget.get("1.0", "end")
    tabbuttons[tabselected].configure(style="TButton")
    cbuttons[tabselected].configure(bg="#2a2a2a")
    x.configure(style="Accent.TButton")
    tabselected = tabbuttons.index(x)
    cbuttons[tabselected].configure(bg="#57c8ff")

    textwidget.delete("1.0", "end")
    textwidget.insert("1.0", tabs[tabselected][1])
    textwidget.delete("end-1c", "end")

    filedir.configure(text=tabs[tabselected][2])

    updatetitle()

def closetab():
    global tabselected
    if not len(tabs) == 1:
        tabs.pop(tabselected)
        tabselected = tabselected - 1
    else:
        tabs[0] = ["Untitled", "", "unsaved", "*"]
        
    buildtabs()

    textwidget.delete("1.0", "end")
    textwidget.insert("1.0", tabs[tabselected][1])
    updatetitle()
    filedir.configure(text=tabs[tabselected][2])

def closetab2(e, x):
    global tabselected
    if not tabselected == cbuttons.index(x):
        tabs.pop(cbuttons.index(x))
            
        buildtabs()

        textwidget.delete("1.0", "end")
        textwidget.insert("1.0", tabs[tabselected][1])
        updatetitle()
        filedir.configure(text=tabs[tabselected][2])
    else:
        closetab()

#endregion

tabs = [
    ["Untitled", "", "unsaved", "*"]
]

tabbuttons = []
cbuttons = []
tabselected = 0

header = tkinter.Frame(root, height="50")
header.pack(fill="both")
header.pack_propagate(False)

tabbar = tkinter.Frame(root, height="50", bg="#202020")
tabbar.pack(fill="both")
tabbar.pack_propagate(False)
tabbar.update()

def buildtabs():

    ntkutils.clearwin(tabbar)
    tabbuttons.clear()
    cbuttons.clear()

    for i in tabs:
        button = ttk.Button(tabbar, text=i[0] + "      ")
        button.pack(side=LEFT, padx=10)
        button.configure(command=lambda x=button: opentab(x))
        button.update()

        cbutton = tkinter.Label(tabbar, text=" X ", fg="grey", font=("", 15), bg="#2a2a2a")
        cbutton.place(x=button.winfo_x() + button.winfo_width() - 32, y=10)
        cbutton.bind("<1>", lambda event, x=cbutton:closetab2(event, x))

        print(button.winfo_width())

        tabbuttons.append(button)
        cbuttons.append(cbutton)

    tabbuttons[tabselected].configure(style="Accent.TButton")
    cbuttons[tabselected].configure(bg="#57c8ff")

buildtabs()

cbuttons[0].place(x=71)

textwidget = tkinter.Text(root, height=int((root.winfo_height() - 100) / 17.5))

scrollbar = ttk.Scrollbar(root, command=textwidget.yview)
textwidget.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y", expand=False, pady=(0, 25))

textwidget.pack(fill="x")

footer = tkinter.Frame(root)
footer.pack(fill="both", expand=True)
footer.pack_propagate(False)

filedir = tkinter.Label(footer)
filedir.pack(side=tkinter.LEFT)
filedir.configure(text="unsaved")

fileboxstate = tkinter.StringVar(value="File")

filemenu = ttk.Combobox(
    header, textvariable=fileboxstate, state="readonly", width=3, 
    values=[
        "Save",
        "Save As",
        "Open",
        "New",
        "File Type"
    ]
)
filemenu.pack(side=tkinter.LEFT, padx=10)

def fileboxaction(*args):
    action = fileboxstate.get()
    filemenu.set("File")

    if action == "Save": save()
    elif action == "Open": openfile()
    elif action == "Save As": save(True)
    elif action == "New": new()
    elif action == "File Type": changetype()
    
fileboxstate.trace("w", fileboxaction)

btnctab = ttk.Button(header, text="Close Tab", command=closetab).pack(side="left")
btnsettings = ttk.Button(header, text="Settings", command=settings_).pack(side=tkinter.LEFT, padx=10)

def refreshtitle(e):
    if not root.wm_title().endswith("*"):
        root.title(root.wm_title() + "*")
    tabs[tabselected][3] = "*"

textwidget.bind("<KeyPress>", refreshtitle)

hotkeys = [
    keyboard.HotKey(
        [keyboard.Key.ctrl, keyboard.KeyCode(char="s")], save
    ),
    keyboard.HotKey(
        [keyboard.Key.ctrl, keyboard.KeyCode(char="o")], openfile
    ),
]

def signal_press_to_hotkeys(key): 
    for hotkey in hotkeys: hotkey.press(l.canonical(key))
def signal_release_to_hotkeys(key):
    for hotkey in hotkeys: hotkey.release(l.canonical(key))

l = keyboard.Listener(on_press=signal_press_to_hotkeys, on_release=signal_release_to_hotkeys)
if cfg["hotkeys"]: l.start()

try:
    applysettings()
except:
    config.get()

root.mainloop()