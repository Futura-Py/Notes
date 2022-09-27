import vars as v
import tkinter

def setimages():
    v.brush_light = tkinter.PhotoImage(master=v.root, file="./assets/brush_light.png")
    v.brush_dark = tkinter.PhotoImage(master=v.root, file="./assets/brush_dark.png")
    v.keyboard_light = tkinter.PhotoImage(master=v.root, file="./assets/keyboard_light.png")
    v.keyboard_dark = tkinter.PhotoImage(master=v.root, file="./assets/keyboard_dark.png")
    v.warn_light = tkinter.PhotoImage(master=v.root, file="./assets/warn_light.png")
    v.warn_dark = tkinter.PhotoImage(master=v.root, file="./assets/warn_dark.png")