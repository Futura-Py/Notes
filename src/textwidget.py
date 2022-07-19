import tkinter as tk

class ScrollText(tk.Frame):
    def __init__(self, master=None, mode="dark", line_numbers_callbacks=None, **text_kwargs):
        tk.Frame.__init__(self, master)
        self.text = tk.Text(self, **text_kwargs)

        if line_numbers_callbacks is None:
            line_numbers_callbacks = []
        self.line_numbers_callbacks = line_numbers_callbacks
        self.numberLines = TextLineNumbers(self, width=30, callbacks=self.line_numbers_callbacks)
        self.numberLines.attach(self.text)

        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Return>", self.onPressDelay)
        self.text.bind("<BackSpace>", self.onPressDelay)
        self.text.bind("<Button-1>", self.redraw)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self, *args):
        self.numberLines.redraw()

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        self.callbacks = kwargs.get("callbacks", [])
        del kwargs["callbacks"]
        tk.Canvas.__init__(self, *args, **kwargs)
        self.text_widget = None

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self, mode="dark", *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            for callback in self.callbacks:
                callback(i)
            linenum = str(i).split(".")[0]
            if mode == "dark":
                self.create_text(2, y, anchor="nw", text=linenum, fill="white")
            else:
                self.create_text(2, y, anchor="nw", text=linenum)
            i = self.text_widget.index("%s+1line" % i)

'''THIS CODE IS CREDIT OF Bryan Oakley (With minor visual modifications on my side): 
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''


if __name__ == '__main__':
    root = tk.Tk()
    scroll = ScrollText(root, mode="light")
    scroll.insert(tk.END, "HEY" + 20*'\n')
    root.after(10, scroll.redraw())
    scroll.pack()
    root.mainloop()