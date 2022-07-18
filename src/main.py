ver = "0.4"

import tkinter, sv_ttk, ntkutils, darkdetect
from tkinter import filedialog, ttk

import generatesize as size 
import filetype as f
import settings
import config
import textwidget as t

cfg = config.get()

root = tkinter.Tk()
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon="assets/logo.png")
ntkutils.placeappincenter(root)
root.update()

closeimg = tkinter.PhotoImage(file="assets/close_light.png")
closeimg2 = tkinter.PhotoImage(file="assets/close_dark.png")

#region funcs
def applysettings(ignoretheme=False, first=False):
    global normal, normal_hover, selected, selected_hover

    if not ignoretheme:
        if cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
        else: sv_ttk.set_theme(cfg["theme"].lower()) 

        if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()): 
            if size.system != "Darwin":
                ntkutils.dark_title_bar(root)

            header.configure(bg="#202020")
            tabbar.configure(bg="#202020")
            footer.configure(bg="#202020")

            closeimg.configure(file="assets/close_light.png")
            closeimg2.configure(file="assets/close_dark.png")

            selected_hover = "#51b7eb"
            selected = "#57c8ff"
            normal = "#2a2a2a"
            normal_hover = "#2f2f2f"
        else: 
            header.configure(bg="#f3f3f3")
            tabbar.configure(bg="#f3f3f3")
            footer.configure(bg="#f3f3f3")

            closeimg.configure(file="assets/close_dark.png")
            closeimg2.configure(file="assets/close_light.png")

            normal = "#fdfdfd"
            normal_hover = "#f9f9f9"
            selected = "#0560b6"
            selected_hover = "#1e6fbc"

    if first:
        if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()):
            if size.system != "Darwin":
                ntkutils.dark_title_bar(root)
            
            selected_hover = "#51b7eb"
            selected = "#57c8ff"
            normal = "#2a2a2a"
            normal_hover = "#2f2f2f"
        else:
            header.configure(bg="#f3f3f3")
            tabbar.configure(bg="#f3f3f3")
            footer.configure(bg="#f3f3f3")
            
            normal = "#fdfdfd"
            normal_hover = "#f9f9f9"
            selected = "#0560b6"
            selected_hover = "#1e6fbc"

            closeimg.configure(file="assets/close_dark.png")
            closeimg2.configure(file="assets/close_light.png")

    textwidget.text.configure(font=(cfg["font"], int(cfg["font-size"])))

    if cfg["mica"]: 
        if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()):
            ntkutils.blur_window_background(root, dark=True)
            textwidget.text.configure(bg="#1b1c1b")
        else:
            ntkutils.blur_window_background(root)
            textwidget.text.configure(bg="#fafbfa")

    buildtabs()

def changetype():
    if tabs[tabselected][2] == "unsaved": save()
    else:
        result = f.get(tabs[tabselected][2])
        tabs[tabselected][2] = result
        tabs[tabselected][0] = result.split("/")[-1]
        filedir.configure(text=result)

        buildtabs()
        updatetitle()

def settings_():
    global cfg

    settings.build()
    root.wait_window(settings.settings)
    
    if settings.save == True:
        oldcfg = cfg
        cfg = settings.cfg
        if oldcfg["linenumbers"] or cfg["linenumbers"]: applysettings(True)
        else: applysettings()

def updatetitle(): root.title("txt2 - {} {}".format(tabs[tabselected][0], tabs[tabselected][3]))

def updatetab(file):
    tabs[tabselected][0] = file.name.split("/")[-1]
    tabs[tabselected][2] = file.name
    tabs[tabselected][3] = ""   

def save(e="", saveas=False):
    if tabs[tabselected][2] == "unsaved" or saveas:
        file = filedialog.asksaveasfile()
        if file == None: return
    else: file = open(tabs[tabselected][2], "w")
    
    if file != None:
        file.write(textwidget.text.get("1.0", "end"))

        updatetab(file)
        filedir.configure(text=file.name)

        file.close()

        buildtabs()
        updatetitle()

def openfile(e):
    if not len(tabs) == 10: 
        file = filedialog.askopenfile()
        content = file.read()

        if not textwidget.text.get("1.0", "end").replace("\n", "") == "": new()

        updatetab(file)

        file.close()

        textwidget.text.insert("1.0", content)
        filedir.configure(text=tabs[tabselected][2])

        buildtabs()
        updatetitle()
    else:
        print("Tab limit reached")

def new():
    if not len(tabs) == 10:
        global tabselected

        tabs[tabselected][1] = textwidget.text.get("1.0", "end")
        textwidget.text.delete("1.0", "end")
        tabs.append(["Untitled", "", "unsaved", "*"])
        filedir.configure(text="unsaved")
        tabselected = len(tabbuttons)

        buildtabs()
        updatetitle()
    else: print("Tab limit reached")

def opentab(x):
    global tabselected

    tabs[tabselected][1] = textwidget.text.get("1.0", "end")
    tabselected = tabbuttons.index(x)

    textwidget.text.delete("1.0", "end")
    textwidget.text.insert("1.0", tabs[tabselected][1])
    textwidget.text.delete("end-1c", "end")

    filedir.configure(text=tabs[tabselected][2])

    buildtabs()
    updatetitle()

def closetab(e, x):
    global tabselected
    if not tabselected == cbuttons.index(x):
        tabs.pop(cbuttons.index(x))
        if cbuttons.index(x) < tabselected: tabselected = tabselected - 1
            
        buildtabs()
    else:
        if len(cbuttons) > 1:
            tabs.pop(tabselected)
            tabselected = tabselected - 1

            buildtabs()

            textwidget.text.delete("1.0", "end")
            textwidget.text.insert("1.0", tabs[tabselected][1])
            updatetitle()
            filedir.configure(text=tabs[tabselected][2])
        else:
            root.destroy()

#endregion

tabs = [["Untitled", "", "unsaved", "*"]]

tabbuttons = []
cbuttons = []
tabselected = 0

header = tkinter.Frame(root, height="50", bg="#202020")
header.pack(fill="both")
header.pack_propagate(False)

tabbar = tkinter.Frame(root, height="50", bg="#202020")
tabbar.pack(fill="both")
tabbar.pack_propagate(False)
tabbar.update()

def on_enters(e, x): x.configure(bg=selected_hover)
def on_leaves(e, x): x.configure(bg=selected)
def on_enter(e, x): x.configure(bg=normal_hover)
def on_leave(e, x): x.configure(bg=normal)

def buildtabs():
    ntkutils.clearwin(tabbar)
    tabbuttons.clear()
    cbuttons.clear()

    for i in tabs:
        button = ttk.Button(tabbar, text=i[0] + "       ", image=closeimg, compound="right")
        button.pack(side="left", padx=10)
        button.configure(command=lambda x=button: opentab(x))
        button.update()

        cbutton = tkinter.Label(tabbar, font=("", 15), image=closeimg, bg=normal)
        cbutton.place(x=button.winfo_x() + button.winfo_width() - 37, y=10)
        cbutton.bind("<1>", lambda event, x=cbutton:closetab(event, x)) # Execute closetab on click

        tabbuttons.append(button)
        cbuttons.append(cbutton)

    tabbuttons[tabselected].configure(style="Accent.TButton")

    # This makes the background change to the hover color when hovering over the button
    for i in tabbuttons:
        if tabbuttons.index(i) == tabselected:
            i.bind("<Enter>", lambda event, x=cbuttons[tabselected]: on_enters(event, x))
            i.bind("<Leave>", lambda event, x=cbuttons[tabselected]: on_leaves(event, x))
        else:
            i.bind("<Enter>", lambda event, x=cbuttons[tabbuttons.index(i)]: on_enter(event, x))
            i.bind("<Leave>", lambda event, x=cbuttons[tabbuttons.index(i)]: on_leave(event, x))

    cbuttons[tabselected].configure(bg=selected, image=closeimg2)

footer = tkinter.Frame(root, width=root.winfo_width(), height=25)
footer.update()
footer.place(y=root.winfo_height() - 25)
footer.pack_propagate(False)

filedir = tkinter.Label(footer, text="unsaved")
filedir.pack(side="left")

if cfg["linenumbers"]:
    if cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
    else: sv_ttk.set_theme(cfg["theme"].lower()) 

    textwidget = t.TextWithLineNumbers(root, height=int((root.winfo_height() - 100) / 17.5), borderwidth=0)
    textwidget.pack(fill="both")
else:
    textwidget = tkinter.Text(root, height=int((root.winfo_height() - 100) / 17.5), borderwidth=0)
    textwidget.text = textwidget
    textwidget.pack(fill="both")

"""
scrollbar = ttk.Scrollbar(root, command=textwidget.text.yview)
textwidget.text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y", expand=False, pady=(0, 25))
"""

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

    if action == "Save": save()
    elif action == "Open": openfile("e")
    elif action == "Save As": save(saveas=True)
    elif action == "New": new()
    elif action == "File Type": changetype()
    
fileboxstate.trace("w", fileboxaction)

btnsettings = ttk.Button(header, text="Settings", command=settings_).pack(side="left")

def refreshtitle(e):
    if not root.wm_title().endswith("*"): root.title(root.wm_title() + "*")
    tabs[tabselected][3] = "*"

textwidget.text.bind("<KeyPress>", refreshtitle)

root.event_add("<<Open>>", "<{}>".format(cfg["hkey-open"]))
root.event_add("<<Save>>", "<{}>".format(cfg["hkey-save"]))

root.bind("<<Open>>", openfile)
root.bind("<<Save>>", save)

if cfg["linenumbers"]: applysettings(True, True)
else: applysettings(first=True)

cbuttons[0].place(x=71) # The first cbutton has to be placed like that because it seems like the winfo functions return wrong values the first time
buildtabs()

root.mainloop()
