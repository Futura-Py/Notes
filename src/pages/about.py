import tkinter
import webbrowser
from tkinter import messagebox, ttk

import update
import utils as u
import vars as v


def checkforupdates():
    response = update.check()

    if response == True: webbrowser.open("https://github.com/futura-py/notes/releases")
    elif response == False: messagebox.showinfo(title="Update", message="You are on the newest version of Futura Notes!")
    else: messagebox.showinfo(title="Rate Limit", message="You have managed to exceed the github api rate limit of 60 requests per hour. idk how that can be achieved by accident. try again in an hour i guess.",)


def build():
    root = tkinter.Toplevel()
    root.title("About Futura Notes")
    root.geometry("650x200")
    root.resizable(False, False)

    name = tkinter.Label(root, text="Futura Notes", font=("Segoe UI", 40, "bold")).place(x=30, y=15)
    version = tkinter.Label(root, text="Version {}".format(v.ver.split(" ")[0]), font=("Segoe UI", 20, "")).place(x=370, y=42)
    versiontype = tkinter.Label(root, text="Beta" if v.ver.endswith("beta") else "Stable", font=("Segoe UI", 20, ""), fg="orange" if v.ver.endswith("beta") else "green").place(x=510, y=42)
    github = ttk.Button(root, text="  Github Repo", image=v.github_light if u.dark() else v.github_dark, compound="left", command=lambda: webbrowser.open("https://github.com/futura-py/notes")).place(x=30, y=105)
    updatebtn = ttk.Button(root, text="  Check for Updates", image=v.update_light if u.dark() else v.update_dark, compound="left", command=checkforupdates).place(x=170, y=105)
