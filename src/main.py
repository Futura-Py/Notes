ver = "0.8 beta"

import os
import tkinter
from pathlib import Path
from tkinter import ttk

import darkdetect
import ntkutils
import sv_ttk
from tkinterdnd2 import *

import config
import editor
import generatesize as size
import tabmanager
import vars as v
from themes import dark, light

cfg = config.get()

if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()):
    theme = dark.get()
else:
    theme = light.get()

root = TkinterDnD.Tk()
root.geometry("200x350")
root.withdraw()
ntkutils.windowsetup(
    root, title="Onyx - Untitled *", icon=Path("assets/logo.png"), resizeable=False
)
sv_ttk.set_theme(cfg["theme"].lower())
root.update_idletasks()
ntkutils.placeappincenter(root)
root.update_idletasks()


def preparewindow():
    ntkutils.clearwin(root)
    root.geometry(size.get())
    root.update()
    ntkutils.placeappincenter(root)
    root.resizable(True, True)
    editor.build(cfg, theme, root, ver)


def openfile(path):
    preparewindow()
    tabmanager.openfile(path=path)


title = tkinter.Label(root, text="Onyx Editor", font=("Segoe UI", 20, "bold")).pack(
    anchor="nw", padx=20, pady=20
)
btncreatenew = ttk.Button(root, text="Create New File", command=preparewindow).pack(
    anchor="nw", padx=20
)
btnopenfile = ttk.Button(
    root, text="Open File", command=lambda: openfile(path="")
).pack(anchor="nw", pady=10, padx=20)
btnopendir = ttk.Button(root, text="Open Directory", state="disabled").pack(
    anchor="nw", padx=20
)
btnopenlast = ttk.Button(
    root, text="Open last file", command=lambda: openfile(path=content)
)
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
