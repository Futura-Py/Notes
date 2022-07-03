import os, tkinter, ntkutils
from tkinter import ttk

def changetype(filename, root):
    def change():
        if entry.get().startswith("."):
            new_path = filename.get().removesuffix("." + filename.get().split(".")[-1]) + entry.get()
            os.rename(filename.get(), new_path)
            filetype.destroy()
            filename.set(new_path)
            root.title("txt2 - {}".format(new_path.split("/")[-1]))
        else:
            print("not an extension")
    filetype = tkinter.Toplevel()
    ntkutils.dark_title_bar(filetype)
    filetype.title("txt2 - Change file type")
    lbl = tkinter.Label(filetype, text="Change file extension:", font=("", 20)).pack(pady=5)
    entry = ttk.Entry(filetype)
    entry.pack(pady=5)
    btn = ttk.Button(filetype, text="Apply", command=change).pack(pady=5)