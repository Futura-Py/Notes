ver = "0.4.1"

import tkinter, ntkutils
from pathlib import Path

import settings, config, tabmanager
import generatesize as size 
import textwidget as t
import vars as v
import applysettings as a
import mdpreview as md

cfg = config.get()

root = tkinter.Tk()
root.geometry(size.get())
root.withdraw()
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon=Path("assets/logo.png"))
root.update_idletasks()
ntkutils.placeappincenter(root)

root.update()

closeimg = tkinter.PhotoImage(file=Path("assets/close_light.png"))
closeimg2 = tkinter.PhotoImage(file=Path("assets/close_dark.png"))

def settings_():
    settings.build()
    root.wait_window(settings.settings)
    
    if settings.save == True:
        oldcfg = cfg
        v.cfg = settings.cfg
        a.applysettings()

def closepreview():
    md.close()
    textwidget.text.bind("<KeyPress>", refreshtitle)

tabbar = tkinter.Frame(root, height="75", bg="#202020")
tabbar.pack(fill="both")
tabbar.pack_propagate(False) 

if cfg["linenumbers"]:
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

menubar = tkinter.Menu(root)
root.config(menu=menubar)

filemenu = tkinter.Menu(menubar, tearoff=False, bg="white")
settingsmenu = tkinter.Menu(menubar, tearoff=False, bg="white")

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Settings", menu=settingsmenu)

filemenu.add_command(label="Save", command=tabmanager.save, foreground="black")
filemenu.add_command(label="Save As", command=lambda:tabmanager.save(saveas=True), foreground="black")
filemenu.add_command(label="Open", command=tabmanager.openfile, foreground="black")
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

# Set global variables
v.cfg = cfg
v.root = root
v.textwidget = textwidget
v.filedir = filedir
v.tabbar = tabbar
v.footer = footer
v.closeimg = closeimg
v.closeimg2 = closeimg2

a.applysettings()

tabmanager.cbuttons[0].place(x=71) # The first cbutton has to be placed like that because it seems like the winfo functions return wrong values the first time
tabmanager.buildtabs()

root.update_idletasks()
root.deiconify()

root.mainloop()
