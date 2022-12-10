import tkinter
from tkinter import filedialog

import pygments.lexers
from pygments.lexers import get_lexer_for_filename

import pages.filetype as f
import vars as v

tabs = [["Untitled", "", "unsaved", "*"]]

# Item 0: Name
# Item 1: Content
# Item 2: Storage Path
# Item 3: Save Status ("*" or "")


def updatetab(file):
    tabs[v.tabselected][0] = file.name.split("/")[-1]
    tabs[v.tabselected][2] = file.name
    tabs[v.tabselected][3] = ""


def updatetitle():
    v.root.title("Futura Notes - {} {}".format(tabs[v.tabselected][0], tabs[v.tabselected][3]))


def redrawlinenums():
    if v.cfg["linenumbers"]:
        v.textwidget.linenums.redraw()


def new():
    tabs[v.tabselected][1] = v.textwidget.get("1.0", "end")  # Save edits
    v.textwidget.delete("1.0", "end")
    tabs.append(["Untitled", "", "unsaved", "*"])
    v.filedir.configure(text="unsaved")
    v.tabselected += 1

    v.tabbar.add(
        tkinter.Frame(), text=tabs[v.tabselected][0], image=v.closeimg, compound="right"
    )
    v.tabbar.select(v.tabselected)

    updatetitle()
    if v.cfg["syntax-highlighting"]:
        v.textwidget._set_lexer(pygments.lexers.TextLexer)


def save(e="", saveas=False):
    if tabs[v.tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
        if file == None:
            return
    else:
        file = open(tabs[v.tabselected][2], "w")

    if file != None:
        file.write(v.textwidget.get("1.0", "end"))

        updatetab(file)
        v.filedir.configure(text=file.name)

        file.close()

        updatetitle()
        setlexer()


def openfile(e="", path=""):
    if path == "":
        file = filedialog.askopenfile()
        content = file.read()
    else:
        file = open(path, "r")
        content = file.read()

    if v.textwidget.get("1.0", "end").replace("\n", "") != "":
        new()

    updatetab(file)

    file.close()

    v.tabbar.tab(
        v.tabselected, text=tabs[v.tabselected][0], image=v.closeimg, compound="right"
    )
    v.textwidget.insert("1.0", content)
    v.filedir.configure(text=tabs[v.tabselected][2])

    updatetitle()
    setlexer()
    redrawlinenums()


def opentab(event, tabdeleted=False):
    if not tabdeleted:
        tabs[v.tabselected][1] = v.textwidget.get("1.0", "end")

    v.tabselected = v.tabbar.index(v.tabbar.select())

    v.textwidget.delete("1.0", "end")
    v.textwidget.insert("1.0", tabs[v.tabselected][1])
    v.textwidget.delete("end-1c", "end")

    v.filedir.configure(text=tabs[v.tabselected][2])

    updatetitle()
    setlexer()
    redrawlinenums()


def setlexer():
    if v.cfg["syntax-highlighting"]:
        try:
            lexer = get_lexer_for_filename(tabs[v.tabselected][0])
        except pygments.util.ClassNotFound:
            lexer = pygments.lexers.TextLexer
        lexer = "pygments.lexers." + str(lexer).split(".")[-1].removesuffix(
            ">"
        ).removesuffix("'")
        v.textwidget._set_lexer(eval(lexer))


# The following two functions contain code copied from https://github.com/Akuli/porcupine


def closetab(event):
    before = v.tabbar.index(f"@{event.x},{event.y}")
    after = before + 1

    if v.tabbar.index(v.tabbar.tabs()[before:after][0]) < v.tabselected:
        v.tabselected -= 1

    tabs.pop(v.tabbar.index(v.tabbar.tabs()[before:after][0]))
    v.tabbar.forget(v.tabbar.tabs()[before:after][0])
    opentab(event, True)


def click(event) -> None:
    if event.widget.identify(event.x, event.y) == "label":
        # find the right edge of the top label (including close button)
        right = event.x
        while event.widget.identify(right, event.y) == "label":
            right += 1

        if event.x >= right - v.closeimg.width():
            if event.widget.index("end") != 1:
                closetab(event)
            else:
                v.root.destroy()
        else:
            opentab(event)
    else:
        opentab(event)


def changetype():
    if tabs[v.tabselected][2] == "unsaved":
        save()
    else:
        result = f.get(tabs[v.tabselected][2])
        tabs[v.tabselected][2] = result
        tabs[v.tabselected][0] = result.split("/")[-1]
        v.filedir.configure(text=result)

        updatetitle()
        setlexer()
