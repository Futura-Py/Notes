import tkinter
import webbrowser
from tkinter import ttk

import darkdetect

import vars as v


def dark():
    if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
        return True
    else:
        return False

def build():
    root = tkinter.Toplevel()
    root.title("About Onyx")
    root.geometry("550x200")
    root.resizable(False, False)

    logolabel = tkinter.Label(root, image=v.logo).place(x=10, y=20)
    name = tkinter.Label(root, text="Onyx", font=("Segoe UI", 40, "bold")).place(x=210, y=30)
    version = tkinter.Label(root, text="Version {}".format(v.ver.split(" ")[0]), font=("Segoe UI", 20, "")).place(x=370, y=57)
    versiontype = tkinter.Label(root, text="Beta" if v.ver.endswith("beta") else "Stable", font=("Segoe UI", 20, "bold"), fg="orange" if v.ver.endswith("beta") else "green").place(x=210, y=105)
    github = ttk.Button(root, text="  Github Repo", image=v.github_light if dark() else v.github_dark, compound="left", command=lambda:webbrowser.open("https://github.com/not-nef/onyx")).place(x=330, y=105)