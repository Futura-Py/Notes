import tkinter, sv_ttk, ntkutils
from tkinter import filedialog, ttk
from pynput.keyboard import HotKey, Key, KeyCode, Listener

try: import generatesize as size 
except: import src.generatesize as size

root = tkinter.Tk()
sv_ttk.set_theme("dark")
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon="assets/logo.png")
ntkutils.dark_title_bar(root)
ntkutils.placeappincenter(root)
root.update()

def save():
    if filename.get() == "unsaved":
        file = filedialog.asksaveasfile()
    else:
        file = open(filename.get(), "w")
    
    try:
        file.write(textwidget.get("1.0", "end"))
        filename.set(file.name)
        file.close()
        root.title("txt2 - {}".format(filename.get().split("/")[-1]))
    except AttributeError:
        pass

def openfile():
    file = filedialog.askopenfile()
    
    try:
        content = file.read()
        filename.set(file.name)
        file.close()
        textwidget.delete("1.0", "end")
        textwidget.insert("1.0", content)
        root.title("txt2 - {}".format(filename.get().split("/")[-1]))
    except AttributeError:
        pass

filename = tkinter.StringVar(value="unsaved")
keyhandlerstatus = True
fileboxstate = tkinter.StringVar(value="File")

header = tkinter.Frame(root, height="50")
header.pack(fill="both")
header.pack_propagate(False)

textwidget = tkinter.Text(root, height=int((root.winfo_height() - 50) / 17.5))

scrollbar = ttk.Scrollbar(root, command=textwidget.yview)
textwidget.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y", expand=False, pady=(0, 25))

textwidget.pack(fill="x")

footer = tkinter.Frame(root)
footer.pack(fill="both", expand=True)
footer.pack_propagate(False)

filemenu = ttk.Combobox(
    header, textvariable=fileboxstate, state="readonly", width=3, 
    values=[
        "Save",
        "Save As",
        "Open",
        "New"
    ]
)
filemenu.pack(side=tkinter.LEFT, padx=10)

filedir = tkinter.Label(footer, textvariable=filename).pack(side=tkinter.LEFT)

hotkeys = [
    HotKey(
        [Key.ctrl, KeyCode(char="s")], save
    ),
    HotKey(
        [Key.ctrl, KeyCode(char="o")], openfile
    ),
]

def signal_press_to_hotkeys(key): 
    for hotkey in hotkeys: hotkey.press(l.canonical(key))
def signal_release_to_hotkeys(key):
    for hotkey in hotkeys: hotkey.release(l.canonical(key))

l = Listener(on_press=signal_press_to_hotkeys, on_release=signal_release_to_hotkeys)
l.start()

def refreshtitle(e):
    if not root.wm_title().endswith("*"):
        root.title(root.wm_title() + "*")

def fileboxaction(*args):
    action = fileboxstate.get()
    filemenu.set("File")

    if action == "Save": save()
    elif action == "Open": openfile()
    
fileboxstate.trace("w", fileboxaction)

textwidget.bind("<KeyPress>", refreshtitle)
root.mainloop()