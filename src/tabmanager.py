import ntkutils, tkinter
from tkinter import ttk, filedialog
from pygments.lexers import get_lexer_for_filename
import pygments.lexers

import vars as v
import filetype as f

tabs = [["Untitled", "", "unsaved", "*"]]

def updatetabcontent(file):
    tabs[v.tabselected][0] = file.name.split("/")[-1]
    tabs[v.tabselected][2] = file.name
    tabs[v.tabselected][3] = ""   

def updatetitle(): v.root.title("txt2 - {} {}".format(tabs[v.tabselected][0], tabs[v.tabselected][3]))

def new():
    if not len(tabs) == 10:
        tabs[v.tabselected][1] = v.textwidget.text.get("1.0", "end")
        v.textwidget.text.delete("1.0", "end")
        tabs.append(["Untitled", "", "unsaved", "*"])
        v.filedir.configure(text="unsaved")
        v.tabselected = v.tabselected + 1

        try: v.textwidget.redraw()
        except: pass

        buildtabs()
        updatetitle()
        if v.cfg["syntax-highlighting"]: v.textwidget.text._set_lexer(pygments.lexers.TextLexer)
    else: print("Tab limit reached")

def save(e="", saveas=False):
    if tabs[v.tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
        if file == None: return
    else: file = open(tabs[v.tabselected][2], "w")
    
    if file != None:
        file.write(v.textwidget.text.get("1.0", "end"))

        updatetabcontent(file)
        v.filedir.configure(text=file.name)

        file.close()

        buildtabs()
        updatetitle()
        setlexer()

def openfile(e=""):
    if not len(tabs) == 10: 
        file = filedialog.askopenfile()
        content = file.read()

        if not v.textwidget.text.get("1.0", "end").replace("\n", "") == "": new()

        updatetabcontent(file)

        file.close()

        v.textwidget.text.insert("1.0", content)
        v.filedir.configure(text=tabs[v.tabselected][2])

        buildtabs()
        updatetitle()
        setlexer()
    else:
        print("Tab limit reached")

def opentab(e):
    v.tabselected = v.tabbar.index(v.tabbar.select())

    v.textwidget.text.delete("1.0", "end")
    v.textwidget.text.insert("1.0", tabs[v.tabselected][1])
    v.textwidget.text.delete("end-1c", "end")

    v.filedir.configure(text=tabs[v.tabselected][2])

    try: v.textwidget.redraw()
    except: pass

    buildtabs()
    updatetitle()
    setlexer()

def buildtabs():
    while True:
        try:
            v.tabbar.forget(0)
        except:
            break

    for i in tabs:
        f = tkinter.Frame(v.root)
        v.tabbar.add(f, text=i[0])
    
    v.tabbar.select(v.tabselected)

def setlexer():
    if v.cfg["syntax-highlighting"]:
        try: lexer = get_lexer_for_filename(tabs[v.tabselected][0])
        except pygments.util.ClassNotFound: lexer = pygments.lexers.TextLexer
        lexer = "pygments.lexers." + str(lexer).split(".")[-1].removesuffix(">")
        v.textwidget.text._set_lexer(eval(lexer))
        try: v.textwidget.redraw()
        except: pass

def changetype():
    if tabs[v.tabselected][2] == "unsaved": save()
    else:
        result = f.get(tabs[v.tabselected][2])
        tabs[v.tabselected][2] = result
        tabs[v.tabselected][0] = result.split("/")[-1]
        v.filedir.configure(text=result)

        buildtabs()
        updatetitle()
        setlexer()