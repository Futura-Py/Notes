import tkinter, sv_ttk, ntkutils
from tkinter import filedialog, ttk
from pynput import keyboard

try: 
    import generatesize as size 
    import filetype as f
    import settings
except: 
    import src.generatesize as size
    import src.filetype as f
    import src.settings as settings

root = tkinter.Tk()
sv_ttk.set_theme("dark")
ntkutils.windowsetup(root, title="txt2 - Untitled *", resizeable=False, size=size.get(), icon="assets/logo.png")
ntkutils.dark_title_bar(root)
ntkutils.placeappincenter(root)
root.update()

def save(saveas=False):
    if filename.get() == "unsaved" or saveas:
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

def new():
    filename.set(value="unsaved")
    root.title("txt2 - Untitled *")
    textwidget.delete("1.0", "end")

def changetype():
    if filename.get() == "unsaved":
        save()
    else:
        f.changetype(filename, root)

filename = tkinter.StringVar(value="unsaved")

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

filedir = tkinter.Label(footer, textvariable=filename).pack(side=tkinter.LEFT)

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
filemenu.pack(side=tkinter.LEFT, padx=10)

def fileboxaction(*args):
    action = fileboxstate.get()
    filemenu.set("File")

    if action == "Save": save()
    elif action == "Open": openfile()
    elif action == "Save As": save(True)
    elif action == "New": new()
    elif action == "File Type": changetype()
    
fileboxstate.trace("w", fileboxaction)

btnsettings = ttk.Button(header, text="Settings", command=lambda:settings.build()).pack(side=tkinter.LEFT)

def refreshtitle(e):
    if not root.wm_title().endswith("*"):
        root.title(root.wm_title() + "*")

textwidget.bind("<KeyPress>", refreshtitle)

hotkeys = [
    keyboard.HotKey(
        [keyboard.Key.ctrl, keyboard.KeyCode(char="s")], save
    ),
    keyboard.HotKey(
        [keyboard.Key.ctrl, keyboard.KeyCode(char="o")], openfile
    ),
]

def signal_press_to_hotkeys(key): 
    for hotkey in hotkeys: hotkey.press(l.canonical(key))
def signal_release_to_hotkeys(key):
    for hotkey in hotkeys: hotkey.release(l.canonical(key))

l = keyboard.Listener(on_press=signal_press_to_hotkeys, on_release=signal_release_to_hotkeys)
#l.start()

root.mainloop()