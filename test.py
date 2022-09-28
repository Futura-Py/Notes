import tkinter
from tkinter import ttk
from tkinter.font import Font
from tklinenums import TkLineNumbers

root = tkinter.Tk()

textwidget = tkinter.Text(root, width=100, borderwidth=0, height=root.winfo_height() - 125)
textwidget.text = textwidget
textwidget.pack(side="right", fill="both", expand=True)

style = ttk.Style()
style.configure("TLineNumbers", background="#ffffff", foreground="#2197db")

font = Font(family="Courier New bold", size=15, name="TkLineNumsFont")

linenums = TkLineNumbers(root, textwidget, font)
linenums.pack(fill="y", side="left", expand=True)
linenums.reload(font)

textwidget.bind("<<ContentChanged>>", lambda event: root.after_idle(linenums.redraw()))
textwidget["yscrollcommand"] = linenums.redraw()

root.mainloop()