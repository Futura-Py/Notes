import markdown
from tkinterweb.htmlwidgets import HtmlFrame
from tkinter import ttk

import vars as v

def update():
    html = markdown.markdown(v.textwidget.text.get("1.0", "end"))
    display.load_html(html)

def reload(e):
    v.root.after(2, update)

def build():
    global display

    display = HtmlFrame(v.root, width=200, messages_enabled=False)
    display.place(x=v.root.winfo_width() / 2, y=100, width=v.root.winfo_width() / 2)
    display.on_link_click(reload) # This line blocks clicking on links

    v.textwidget.text.bind("<KeyPress>", reload)
    reload("")

def close():
    display.destroy()