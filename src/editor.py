import tkinter
from pathlib import Path
from tkinter import ttk
from tkinter.font import Font

import chlorophyll
import darkdetect
import ntkutils
import pygments
import pyperclip
from tkinterdnd2 import *
from tklinenums import TkLineNumbers

import mdpreview as md
import pages.about as about
import pages.wanttosave as w
import settings.UI as settingsui
import tabmanager
import vars as v
from settings.images import setimages


def build(theme, root, ver):
    closeimg = tkinter.PhotoImage(file=Path(theme["closeimg"]))

    def closepreview():
        md.close()
        textwidget.bind("<KeyPress>", refreshtitle)
        if v.cfg["linenumbers"]:
            textwidget.bind(
                f"<BackSpace>", lambda event: root.after_idle(linenums.redraw), add=True
            )

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    footer = tkinter.Frame(root, width=root.winfo_width(), height=25)
    footer.update_idletasks()
    footer.pack(side="bottom", fill="x")
    footer.pack_propagate(False)

    scrollbar = ttk.Scrollbar(root)
    scrollbar.pack(side="right", fill="y")

    if v.cfg["syntax-highlighting"]:
        textwidget = chlorophyll.CodeView(
            root,
            height=800,
            bg=theme["primary"],
            lexer=pygments.lexers.TextLexer,
            font=(v.cfg["font"], int(v.cfg["font-size"])),
        )
        textwidget._set_color_scheme(theme["color_scheme"])
        textwidget.pack(side="right", fill="both", expand=True)
        textwidget._hs.grid_remove()
        textwidget._vs.grid_remove()
    else:       
        textwidget = tkinter.Text(
            root,
            width=100,
            borderwidth=0,
            height=root.winfo_height() - 125,
            font=(v.cfg["font"], int(v.cfg["font-size"])),
        )
        textwidget.pack(side="right", fill="both", expand=True)

    textwidget.update()

    scrollbar.configure(command=textwidget.yview)
    textwidget["yscrollcommand"] = scrollbar.set

    if v.cfg["linenumbers"]:
        style = ttk.Style()
        style.configure(
            "TLineNumbers",
            background=theme["primary"],
            foreground=theme["opposite_secondary"],
        )

        font = Font(
            family="Courier New bold", size=v.cfg["font-size"], name="TkLineNumsFont"
        )

        linenums = TkLineNumbers(root, textwidget, font, "right")
        linenums.pack(side="left", fill="y")
        linenums.configure(borderwidth=0)
        linenums.reload(font)

        textwidget.bind(
            "<Return>", lambda event: root.after_idle(linenums.redraw), add=True
        )
        textwidget.bind(
            f"<BackSpace>", lambda event: root.after_idle(linenums.redraw), add=True
        )
        textwidget.bind(
            f"<Control-v>", lambda event: root.after_idle(linenums.redraw), add=True
        )

        def onscroll(first, last):
            scrollbar.set(first, last)
            linenums.redraw()

        textwidget["yscrollcommand"] = onscroll

        textwidget.linenums = linenums

    filedir = tkinter.Label(footer, text="unsaved")
    filedir.pack(side="left")

    menubar = tkinter.Menu(root)
    root.config(menu=menubar)

    filemenu = tkinter.Menu(menubar, tearoff=False, bg="white")
    settingsmenu = tkinter.Menu(menubar, tearoff=False, bg="white")

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Settings", menu=settingsmenu)

    filemenu.add_command(label="Save ({})".format(v.cfg["hkey-save"]), command=tabmanager.save, foreground="black" )
    filemenu.add_command(label="Save As", command=lambda: tabmanager.save(saveas=True), foreground="black")
    filemenu.add_command(label="Open ({})".format(v.cfg["hkey-open"]), command=tabmanager.openfile, foreground="black")
    filemenu.add_command(label="New", command=tabmanager.new, foreground="black")
    filemenu.add_separator()
    filemenu.add_command(label="Change file extension", command=tabmanager.changetype, foreground="black")
    filemenu.add_separator()
    filemenu.add_command(label="Preview Markdown", command=md.build, foreground="black")
    filemenu.add_command(label="Close Preview", command=closepreview, foreground="black")

    settingsmenu.add_command(label="Open Settings", command=settingsui.build, foreground="black")
    settingsmenu.add_command(label="About", command=about.build, foreground="black")

    if v.cfg["mica"]:
        if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
            notebook.configure(bg="#1c1c1c")
            ntkutils.blur_window_background(root, dark=True)
            textwidget.text.configure(bg="#1b1c1b")
            try:
                textwidget.numberLines.configure(bg="#1b1c1b")
            except:
                pass
        else:
            ntkutils.blur_window_background(root)
            textwidget.text.configure(bg="#fafbfa")

    def refreshtitle(e):
        if not root.wm_title().endswith("*"):
            root.title(root.wm_title() + "*")
        tabmanager.tabs[v.tabselected][3] = "*"

    textwidget.bind("<KeyPress>", refreshtitle)

    root.event_add("<<Open>>", "<{}>".format(v.cfg["hkey-open"]))
    root.event_add("<<Save>>", "<{}>".format(v.cfg["hkey-save"]))

    root.bind("<<Open>>", tabmanager.openfile)
    root.bind("<<Save>>", tabmanager.save)

    def filedrop(event):
        tabmanager.openfile(path=event.data)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", filedrop)

    def cut():
        pyperclip.copy(textwidget.selection_get())
        textwidget.delete("sel.first", "sel.last")

    def copy(): 
        pyperclip.copy(textwidget.selection_get())

    def paste():
        textwidget.insert("insert", pyperclip.paste())

    def popup(event):
        try:
            context.tk_popup(event.x_root, event.y_root, 0)
        finally:
            context.grab_release()

    context = tkinter.Menu(root, tearoff=False, bg="white")
    context.add_command(label="Cut", command=cut, foreground="black")
    context.add_command(label="Copy", command=copy, foreground="black")
    context.add_command(label="Paste", command=paste, foreground="black")
    root.bind("<Button-3>", popup)

    def on_closing():
        if v.cfg["onclose"] == "Do Nothing":
            root.destroy()
        elif v.cfg["onclose"] == "Save":
            tabmanager.save()
            root.destroy()
        else:
            w.build()


    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Set global variables
    v.root = root
    v.textwidget = textwidget
    v.filedir = filedir
    v.tabbar = notebook
    v.footer = footer
    v.closeimg = closeimg
    v.theme = theme
    v.ver = ver

    setimages()

    notebook.add(tkinter.Frame(), text=tabmanager.tabs[0][0], image=closeimg, compound="right")
    # Bind Left mouse button to write content of selected tab into the text widget
    notebook.bind("<ButtonRelease-1>", tabmanager.click, add="+")  
