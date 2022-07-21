ver = "0.4.1"

import tkinter, sv_ttk, ntkutils, darkdetect
from tkinter import ttk

import generatesize as size 
import settings
import config
import textwidget as t
import tabmanager
import vars as v
import applysettings as a
import mdpreview as md

cfg = config.get()

root = tkinter.Tk()
root.geometry(size.get())
root.withdraw()
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon="assets/logo.png")
root.update_idletasks()
ntkutils.placeappincenter(root)

root.update()

closeimg = tkinter.PhotoImage(file="assets/close_light.png")
closeimg2 = tkinter.PhotoImage(file="assets/close_dark.png")

def settings_():
    settings.build()
    root.wait_window(settings.settings)
    
    if settings.save == True:
        oldcfg = cfg
        v.cfg = settings.cfg
        if oldcfg["linenumbers"] or cfg["linenumbers"]: a.applysettings(True)
        else: a.applysettings()

def closepreview():
    md.close()
    textwidget.text.bind("<KeyPress>", refreshtitle)

header = tkinter.Frame(root, height="50", bg="#202020")
header.pack(fill="both")
header.pack_propagate(False)

tabbar = tkinter.Frame(root, height="50", bg="#202020")
tabbar.pack(fill="both")
tabbar.pack_propagate(False) 

if cfg["linenumbers"]:
    if cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
    else: sv_ttk.set_theme(cfg["theme"].lower()) 

    textwidget = t.ScrollText(root, width=100, borderwidth=0, height=root.winfo_height() - 125)
    textwidget.pack(fill="both")
    textwidget.redraw()
else:
    textwidget = tkinter.Text(root, width=100, borderwidth=0, height=root.winfo_height() - 125)
    textwidget.text = textwidget
    textwidget.pack(fill="both")

footer = tkinter.Frame(root, width=root.winfo_width(), height=25)
footer.update()
footer.place(y=root.winfo_height() - 25)
footer.pack_propagate(False)

filedir = tkinter.Label(footer, text="unsaved")
filedir.pack(side="left")

fileboxstate = tkinter.StringVar(value="File")

filemenu = ttk.Combobox(
    header, textvariable=fileboxstate, state="readonly", width=3, 
    values=[
        "Save",
        "Save As",
        "Open",
        "New",
        "File Type"
    ]
)
filemenu.pack(side="left", padx=10)

def fileboxaction(*args):
    action = fileboxstate.get()
    filemenu.set("File")

    if action == "Save": tabmanager.save()
    elif action == "Open": tabmanager.openfile("e")
    elif action == "Save As": tabmanager.save(saveas=True)
    elif action == "New": tabmanager.new()
    elif action == "File Type": tabmanager.changetype()
    
fileboxstate.trace("w", fileboxaction)

btnsettings = ttk.Button(header, text="Settings", command=settings_).pack(side="left")
btnpreview = ttk.Button(header, text="Preview Markdown", command=md.build).pack(side="left", padx=10)
btnclosepreview = ttk.Button(header, text="Close Preview", command=closepreview).pack(side="left")

def refreshtitle(e):
    if not root.wm_title().endswith("*"): root.title(root.wm_title() + "*")
    tabmanager.tabs[v.tabselected][3] = "*"

textwidget.text.bind("<KeyPress>", refreshtitle)

root.event_add("<<Open>>", "<{}>".format(cfg["hkey-open"]))
root.event_add("<<Save>>", "<{}>".format(cfg["hkey-save"]))

root.bind("<<Open>>", tabmanager.openfile)
root.bind("<<Save>>", tabmanager.save)

# Set global variables
v.cfg = cfg
v.root = root
v.textwidget = textwidget
v.filedir = filedir
v.header = header
v.tabbar = tabbar
v.footer = footer
v.closeimg = closeimg
v.closeimg2 = closeimg2

if cfg["linenumbers"]: a.applysettings(True, True)
else: a.applysettings(first=True)

tabmanager.cbuttons[0].place(x=71) # The first cbutton has to be placed like that because it seems like the winfo functions return wrong values the first time
tabmanager.buildtabs()

root.update_idletasks()
root.deiconify()

root.mainloop()
