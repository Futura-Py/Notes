import os, tkinter, ntkutils
from tkinter import ttk

def changetype(filename):
    global filetype
    def change():
        global new_path
        if entry.get().startswith("."):
            new_path = filename.removesuffix("." + filename.split(".")[-1]) + entry.get()
            os.rename(filename, new_path)
            filetype.destroy()
        else:
            print("not an extension")
    filetype = tkinter.Toplevel()
    ntkutils.dark_title_bar(filetype)
    filetype.title("txt2 - Change file type")
    lbl = tkinter.Label(filetype, text="Change file extension:", font=("", 20)).pack(pady=5)
    entry = ttk.Entry(filetype)
    entry.pack(pady=5)
    btn = ttk.Button(filetype, text="Apply", command=change).pack(pady=5)

def get(path):
    changetype(path)
    filetype.wait_window()
    return new_path