import tkinter
from tkinter import ttk

import tabmanager as t
import vars as v


def save(e=""):
    t.save()
    v.root.destroy()


def build():
    w = tkinter.Toplevel()
    w.geometry("300x100")
    w.title("Save before exiting?")
    w.focus_set()

    lbl = tkinter.Label(w, font=("Segoe UI", 10, "bold"), text="Do you want to save before exiting?").pack(pady=10)

    btnno = ttk.Button(w, text="No", command=v.root.destroy, width=10).place(x=25, y=50)
    btnyes = ttk.Button(w, text="Yes", command=save, width=10, style="Accent.TButton").place(x=170, y=50)

    w.bind("<Return>", save)