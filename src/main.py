ver = "0.5"

import tkinter, ntkutils, pygments
from tkinter.font import Font
from pathlib import Path
from tkinter import ttk
from tkinterdnd2 import *
from tklinenums import TkLineNumbers

import config, tabmanager
import settings.applysettings as a
import settings.UI as settingsui
from settings.images import setimages
import generatesize as size
import vars as v
import mdpreview as md
from widgets.textwidget import ScrollText, ScrollCode
from widgets.codeview import CodeView

cfg = config.get()

root = TkinterDnD.Tk()
root.geometry(size.get())
root.withdraw()
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon=Path("assets/logo.png"))
root.update_idletasks()
ntkutils.placeappincenter(root)

root.update_idletasks()

closeimg = tkinter.PhotoImage(file=Path("assets/close_light.png"))
closeimg2 = tkinter.PhotoImage(file=Path("assets/close_dark.png"))

def settings_():
    settingsui.build()
    root.wait_window(settingsui.settings)

    if settingsui.save == True:
        v.cfg = settingsui.cfg
        a.applysettings()

def closepreview():
    md.close()
    textwidget.text.bind("<KeyPress>", refreshtitle)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

if cfg["linenumbers"] and not cfg["syntax-highlighting"]:
    textwidget = tkinter.Text(root, width=100, borderwidth=0, height=root.winfo_height() - 125)
    textwidget.text = textwidget
    textwidget.pack(side="right", fill="both", expand=True)

    style = ttk.Style()
    style.configure("TLineNumbers", background="#ffffff", foreground="#2197db")

    font = Font(family="Courier New bold", size=15, name="TkLineNumsFont")

    linenums = TkLineNumbers(root, textwidget, font)
    linenums.pack(fill="y", side="left", expand=True)
    linenums.reload(font)

    textwidget.bind("<Return>", lambda event: root.after_idle(linenums.redraw), add=True)
    textwidget.bind(f"<BackSpace>", lambda event: root.after_idle(linenums.redraw), add=True)
    textwidget.bind(f"<Control-v>", lambda event: root.after_idle(linenums.redraw), add=True)
    textwidget["yscrollcommand"] = linenums.redraw
elif cfg["syntax-highlighting"] and not cfg["linenumbers"]:
    textwidget = CodeView(root, height=800, bg="#1c1c1c", lexer=pygments.lexers.TextLexer)
    textwidget.pack(fill="both")
    textwidget.text = textwidget
elif cfg["syntax-highlighting"] and cfg["linenumbers"]:
    textwidget = ScrollCode(root, height=800, bg="#1c1c1c", lexer=pygments.lexers.TextLexer)
    textwidget.pack(fill="both")
    textwidget.redraw()
else:
    textwidget = tkinter.Text(root, width=100, borderwidth=0, height=root.winfo_height() - 125)
    textwidget.text = textwidget
    textwidget.pack(fill="both")


footer = tkinter.Frame(root, width=root.winfo_width(), height=25)
footer.update_idletasks()
footer.place(y=root.winfo_height() - 25)
footer.pack_propagate(False)

filedir = tkinter.Label(footer, text="unsaved")
filedir.pack(side="left")

menubar = tkinter.Menu(root)
root.config(menu=menubar)

filemenu = tkinter.Menu(menubar, tearoff=False, bg="white")
settingsmenu = tkinter.Menu(menubar, tearoff=False, bg="white")

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Settings", menu=settingsmenu)

filemenu.add_command(label="Save ({})".format(cfg["hkey-save"]), command=tabmanager.save, foreground="black")
filemenu.add_command(label="Save As", command=lambda:tabmanager.save(saveas=True), foreground="black")
filemenu.add_command(label="Open ({})".format(cfg["hkey-open"]), command=tabmanager.openfile, foreground="black")
filemenu.add_command(label="New", command=tabmanager.new, foreground="black")
filemenu.add_separator()
filemenu.add_command(label="Change file extension", command=tabmanager.changetype, foreground="black")
filemenu.add_separator()
filemenu.add_command(label="Preview Markdown", command=md.build, foreground="black")
filemenu.add_command(label="Close Preview", command=closepreview, foreground="black")

settingsmenu.add_command(label="Open Settings", command=settings_, foreground="black")
settingsmenu.add_command(label="About", state="disabled")

def refreshtitle(e):
    if not root.wm_title().endswith("*"): root.title(root.wm_title() + "*")
    tabmanager.tabs[v.tabselected][3] = "*"

textwidget.text.bind("<KeyPress>", refreshtitle)

root.event_add("<<Open>>", "<{}>".format(cfg["hkey-open"]))
root.event_add("<<Save>>", "<{}>".format(cfg["hkey-save"]))

root.bind("<<Open>>", tabmanager.openfile)
root.bind("<<Save>>", tabmanager.save)


def filedrop(event):
    tabmanager.openfile(path=event.data)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", filedrop)


# Set global variables
v.cfg = cfg
v.root = root
v.textwidget = textwidget
v.filedir = filedir
v.tabbar = notebook
v.footer = footer
v.closeimg = closeimg
v.closeimg2 = closeimg2

setimages()

a.applysettings()

notebook.add(tkinter.Frame(), text=tabmanager.tabs[0][0], image=closeimg, compound="right")
notebook.bind('<ButtonRelease-1>', tabmanager.click, add="+") # Bind Left mouse button to write content of selected tab into the text widget

root.update_idletasks()
root.deiconify()
root.mainloop()
