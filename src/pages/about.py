import tkinter
from tkinter import messagebox
import webbrowser
from tkinter import ttk

import darkdetect

import update
import vars as v


def dark():
    if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
        return True
    else:
        return False


def checkforupdates():
    response = update.check()

    if response == True:
        webbrowser.open("https://github.com/not-nef/onyx/releases")
    elif response == False:
        messagebox.showinfo(
            title="Update", message="You are on the newest version of onyx!"
        )
    else:
        messagebox.showinfo(
            title="Rate Limit",
            message="""You have managed to exceed the github api rate limit of 60 requests per hour. idk how that can be achieved by accident. try again in an hour i guess.
        """,
        )


def build():
    root = tkinter.Toplevel()
    root.title("About Onyx")
    root.geometry("650x200")
    root.resizable(False, False)

    logolabel = tkinter.Label(root, image=v.logo).place(x=10, y=20)

    name = tkinter.Label(root, text="Onyx", font=("Segoe UI", 40, "bold")).place(
        x=210, y=30
    )
    version = tkinter.Label(
        root, text="Version {}".format(v.ver.split(" ")[0]), font=("Segoe UI", 20, "")
    ).place(x=370, y=57)

    versiontype = tkinter.Label(
        root,
        text="Beta" if v.ver.endswith("beta") else "Stable",
        font=("Segoe UI", 20, ""),
        fg="orange" if v.ver.endswith("beta") else "green",
    ).place(x=510, y=57)

    github = ttk.Button(
        root,
        text="  Github Repo",
        image=v.github_light if dark() else v.github_dark,
        compound="left",
        command=lambda: webbrowser.open("https://github.com/not-nef/onyx"),
    ).place(x=210, y=120)

    updatebtn = ttk.Button(
        root,
        text="  Check for Updates",
        image=v.update_light if dark() else v.update_dark,
        compound="left",
        command=checkforupdates,
    ).place(x=350, y=120)
