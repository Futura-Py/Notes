ver = "0.7 beta"

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
from themes import dark, light

cfg = config.get()

if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()): theme = dark.get()
else: theme = light.get()

root = TkinterDnD.Tk()
root.geometry("200x300")
root.withdraw()
ntkutils.windowsetup(root, title="Onyx - Untitled *", icon=Path("assets/logo.png"), resizeable=False)
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
    editor.build(cfg, theme, root)

def openfile():
    preparewindow()
    tabmanager.openfile()

title = tkinter.Label(root, text="Onyx Editor", font=("Segoe UI", 20, "bold")).pack(anchor="nw", padx=20, pady=20)
btncreatenew = ttk.Button(root, text="Create New File", command=preparewindow).pack(anchor="nw", padx=20)
btnopenfile = ttk.Button(root, text="Open File", command=openfile).pack(anchor="nw", pady=10, padx=20)
btnopendir = ttk.Button(root, text="Open Directory", state="disabled").pack(anchor="nw", padx=20)

root.update_idletasks()
root.deiconify()
root.mainloop()