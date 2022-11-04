import markdown
from tkinterweb.htmlwidgets import HtmlFrame

import vars as v


def update():
    html = markdown.markdown(v.textwidget.get("1.0", "end"))
    display.load_html(html)

def reload(e):
    v.root.after(2, update)

def build():
    global display, binding

    display = HtmlFrame(v.root, messages_enabled=False)
    display.place(x=v.root.winfo_width() / 2, y=50, width=v.root.winfo_width() / 2, height=v.root.winfo_height() - 75)
    display.on_link_click(reload) # This line blocks clicking on links

    v.textwidget.bind("<KeyPress>", reload, add="+")
    v.textwidget.bind("<BackSpace>", reload, add="+")
    reload("")

def close():
    v.textwidget.unbind("<KeyPress>")
    v.textwidget.unbind("<BackSpace>")
    display.destroy()