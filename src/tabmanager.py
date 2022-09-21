from __future__ import annotations

import ntkutils, tkinter
from tkinter import PhotoImage, ttk, filedialog, Event
from pygments.lexers import get_lexer_for_filename
import pygments.lexers
import pyautogui

import vars as v
import filetype as f

tabs = [["Untitled", "", "unsaved", "*"]]

def updatetab(file):
    tabs[v.tabselected][0] = file.name.split("/")[-1]
    tabs[v.tabselected][2] = file.name
    tabs[v.tabselected][3] = ""

def updatetitle(): v.root.title("txt2 - {} {}".format(tabs[v.tabselected][0], tabs[v.tabselected][3]))

def new():
    tabs[v.tabselected][1] = v.textwidget.text.get("1.0", "end")
    v.textwidget.text.delete("1.0", "end")
    tabs.append(["Untitled", "", "unsaved", "*"])
    v.filedir.configure(text="unsaved")
    v.tabselected = v.tabselected + 1

    try: v.textwidget.redraw()
    except: pass

    v.tabbar.add(tkinter.Frame(), text=tabs[v.tabselected][0], image=v.closeimg, compound="right")
    v.tabbar.select(v.tabselected)

    updatetitle()
    if v.cfg["syntax-highlighting"]: v.textwidget.text._set_lexer(pygments.lexers.TextLexer)

def save(e="", saveas=False):
    if tabs[v.tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
        if file == None: return
    else: file = open(tabs[v.tabselected][2], "w")

    if file != None:
        file.write(v.textwidget.text.get("1.0", "end"))

        updatetab(file)
        v.filedir.configure(text=file.name)

        file.close()

        updatetitle()
        setlexer()

def openfile(e=""):
    file = filedialog.askopenfile()
    content = file.read()

    if v.textwidget.text.get("1.0", "end").replace("\n", "") != "": 
        new()

    updatetab(file)

    file.close()

    v.tabbar.tab(v.tabselected, text=tabs[v.tabselected][0], image=v.closeimg, compound="right")
    v.textwidget.text.insert("1.0", content)
    v.filedir.configure(text=tabs[v.tabselected][2])

    updatetitle()
    setlexer()

def opentab(event, tabdeleted=False):
    if not tabdeleted: tabs[v.tabselected][1] = v.textwidget.text.get("1.0", "end")

    v.tabselected = v.tabbar.index(v.tabbar.select())

    v.textwidget.text.delete("1.0", "end")
    v.textwidget.text.insert("1.0", tabs[v.tabselected][1])
    v.textwidget.text.delete("end-1c", "end")

    v.filedir.configure(text=tabs[v.tabselected][2])

    try: v.textwidget.redraw()
    except: pass

    updatetitle()
    setlexer()

def setlexer():
    if v.cfg["syntax-highlighting"]:
        try: lexer = get_lexer_for_filename(tabs[v.tabselected][0])
        except pygments.util.ClassNotFound: lexer = pygments.lexers.TextLexer
        lexer = "pygments.lexers." + str(lexer).split(".")[-1].removesuffix(">").removesuffix("'")
        v.textwidget.text._set_lexer(eval(lexer))
        try: v.textwidget.redraw()
        except: pass

# The following two functions are property of Akuli

def closetab(event):
    before = v.tabbar.index(f"@{event.x},{event.y}")
    after = before + 1

    if v.tabbar.index(v.tabbar.tabs()[before:after][0]) < v.tabselected:
        v.tabselected = v.tabselected - 1

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
    if tabs[v.tabselected][2] == "unsaved": save()
    else:
        result = f.get(tabs[v.tabselected][2])
        tabs[v.tabselected][2] = result
        tabs[v.tabselected][0] = result.split("/")[-1]
        v.filedir.configure(text=result)

        updatetitle()
        setlexer()
