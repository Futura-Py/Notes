ver = "0.9 beta"

import os
import tkinter
from tkinter import ttk

import ntkutils
import sv_ttk
from tkinterdnd2 import *

import config
import editor
import generatesize as size
import settings.UI as settings
import tabmanager
import utils as u
import vars as v
from themes import dark, light

v.cfg = config.get()

if u.dark():
    theme = dark.get()
else:
    theme = light.get()

root = TkinterDnD.Tk()
root.geometry("200x350")
root.withdraw()
ntkutils.windowsetup(root, title="Futura Notes", resizeable=False)
sv_ttk.set_theme(v.cfg["theme"].lower())
root.update_idletasks()
ntkutils.placeappincenter(root)
root.update_idletasks()


def preparewindow():
    root.title("Futura Notes - Untitled *")
    ntkutils.clearwin(root)
    root.geometry(size.get())
    root.update()
    ntkutils.placeappincenter(root)
    root.resizable(True, True)
    editor.build(theme, root, ver)


def openfile(path):
    preparewindow()
    tabmanager.openfile(path=path)

def settingss():
    preparewindow()
    settings.build()


title = tkinter.Label(root, text="Futura Notes", font=("Segoe UI", 20, "bold")).pack(anchor="nw", padx=20, pady=20)
btncreatenew = ttk.Button(root, text="Create New File", command=preparewindow).pack(anchor="nw", padx=20)
btnopenfile = ttk.Button(root, text="Open File", command=lambda: openfile(path="")).pack(anchor="nw", pady=10, padx=20)
btnopendir = ttk.Button(root, text="Open Directory", state="disabled").pack(anchor="nw", padx=20)
btnopenlast = ttk.Button(root, text="Open last file", command=lambda: openfile(path=content))
btnopenlast.pack(anchor="nw", padx=20, pady=20)

if os.path.isfile("lastfile.txt"):
    file = open("lastfile.txt", "r")
    content = file.read()
    file.close()

    if not os.path.isfile(content):
        btnopenlast.configure(state="disabled")
else:
    btnopenlast.configure(state="disabled")

root.update_idletasks()
root.deiconify()
root.mainloop()

# Save path of last opened file
content = tabmanager.tabs[v.tabselected][2]

if content != "unsaved":
    file = open("lastfile.txt", "w+")
    file.write(content)
    file.close()
