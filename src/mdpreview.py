import markdown
from tkinterweb.htmlwidgets import HtmlFrame

import vars as v

def update():
    html = markdown.markdown(v.textwidget.text.get("1.0", "end"))
    display.load_html(html)

def reload(e):
    v.root.after(2, update)

def build():
    global display, binding

    display = HtmlFrame(v.root, messages_enabled=False)
    display.place(x=v.root.winfo_width() / 2, y=75, width=v.root.winfo_width() / 2, height=v.root.winfo_height() - 100)
    display.on_link_click(reload) # This line blocks clicking on links

    v.textwidget.text.bind("<KeyPress>", reload, add="+")
    reload("")

def close():
    v.textwidget.text.unbind("<KeyPress>")
    display.destroy()