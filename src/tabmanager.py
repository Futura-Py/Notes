import ntkutils, tkinter
from tkinter import ttk, filedialog
from pygments.lexers import get_lexer_for_filename
import pygments.lexers

import vars as v
import filetype as f

tabbuttons = []
cbuttons = []
tabs = [["Untitled", "", "unsaved", "*"]]


def update(file):
    tabs[v.tabselected][0] = file.name.split("/")[-1]
    tabs[v.tabselected][2] = file.name
    tabs[v.tabselected][3] = ""   

def updatetitle(): v.root.title("txt2 - {} {}".format(tabs[v.tabselected][0], tabs[v.tabselected][3]))

def _open(x):
    tabs[v.tabselected][1] = v.textwidget.text.get("1.0", "end")
    v.tabselected = tabbuttons.index(x)

    v.textwidget.text.delete("1.0", "end")
    v.textwidget.text.insert("1.0", tabs[v.tabselected][1])
    v.textwidget.text.delete("end-1c", "end")

    v.filedir.configure(text=tabs[v.tabselected][2])

    buildtabs()
    updatetitle()
    setlexer()

def close(e, x):
    if not v.tabselected == cbuttons.index(x):
        tabs.pop(cbuttons.index(x))
        if cbuttons.index(x) < v.tabselected: v.tabselected = v.tabselected - 1
            
        buildtabs()
    else:
        if len(cbuttons) > 1:
            tabs.pop(v.tabselected)
            v.tabselected = v.tabselected - 1

            buildtabs()

            v.textwidget.text.delete("1.0", "end")
            v.textwidget.text.insert("1.0", tabs[v.tabselected][1])
            updatetitle()
            v.filedir.configure(text=tabs[v.tabselected][2])
        else:
            v.root.destroy()

def new():
    if not len(tabs) == 10:
        tabs[v.tabselected][1] = v.textwidget.text.get("1.0", "end")
        v.textwidget.text.delete("1.0", "end")
        tabs.append(["Untitled", "", "unsaved", "*"])
        v.filedir.configure(text="unsaved")
        v.tabselected = len(tabbuttons)

        buildtabs()
        updatetitle()
        if v.cfg["syntax-highlighting"]: v.textwidget._set_lexer(pygments.lexers.TextLexer)
    else: print("Tab limit reached")

def save(e="", saveas=False):
    if tabs[v.tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
        if file == None: return
    else: file = open(tabs[v.tabselected][2], "w")
    
    if file != None:
        file.write(v.textwidget.text.get("1.0", "end"))

        update(file)
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

        update(file)

        file.close()

        v.textwidget.text.insert("1.0", content)
        v.filedir.configure(text=tabs[v.tabselected][2])

        buildtabs()
        updatetitle()
        setlexer()
    else:
        print("Tab limit reached")

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

def on_enters(e, x): x.configure(bg=v.selected_hover)
def on_leaves(e, x): x.configure(bg=v.selected)
def on_enter(e, x): x.configure(bg=v.normal_hover)
def on_leave(e, x): x.configure(bg=v.normal)

def buildtabs():
    ntkutils.clearwin(v.tabbar)
    tabbuttons.clear()
    cbuttons.clear()

    for i in tabs:
        button = ttk.Button(v.tabbar, text=i[0] + "       ", image=v.closeimg, compound="right")
        button.pack(side="left", padx=10)
        button.configure(command=lambda x=button: _open(x))
        button.update()

        cbutton = tkinter.Label(v.tabbar, font=("", 15), image=v.closeimg, bg=v.normal)
        cbutton.place(x=button.winfo_x() + button.winfo_width() - 37, y=23)
        cbutton.bind("<1>", lambda event, x=cbutton:close(event, x)) # Execute closetab on click

        tabbuttons.append(button)
        cbuttons.append(cbutton)

    tabbuttons[v.tabselected].configure(style="Accent.TButton")

    # This makes the background change to the hover color when hovering over the button
    for i in tabbuttons:
        if tabbuttons.index(i) == v.tabselected:
            i.bind("<Enter>", lambda event, x=cbuttons[v.tabselected]: on_enters(event, x))
            i.bind("<Leave>", lambda event, x=cbuttons[v.tabselected]: on_leaves(event, x))
        else:
            i.bind("<Enter>", lambda event, x=cbuttons[tabbuttons.index(i)]: on_enter(event, x))
            i.bind("<Leave>", lambda event, x=cbuttons[tabbuttons.index(i)]: on_leave(event, x))

    cbuttons[v.tabselected].configure(bg=v.selected, image=v.closeimg2)

def setlexer():
    if v.cfg["syntax-highlighting"]:
        lexer = get_lexer_for_filename(tabs[v.tabselected][0])
        lexer = "pygments.lexers." + str(lexer).split(".")[-1].removesuffix(">")
        v.textwidget._set_lexer(eval(lexer))