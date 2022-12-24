import tkinter

import vars as v


def setimages():
    v.brush_light = tkinter.PhotoImage(master=v.root, file="./assets/brush_light.png")
    v.brush_dark = tkinter.PhotoImage(master=v.root, file="./assets/brush_dark.png")
    v.keyboard_light = tkinter.PhotoImage(master=v.root, file="./assets/keyboard_light.png")
    v.keyboard_dark = tkinter.PhotoImage(master=v.root, file="./assets/keyboard_dark.png")
    v.warn_light = tkinter.PhotoImage(master=v.root, file="./assets/warn_light.png")
    v.warn_dark = tkinter.PhotoImage(master=v.root, file="./assets/warn_dark.png")
    v.logo = tkinter.PhotoImage(master=v.root, file="./assets/logo.png")
    v.github_dark = tkinter.PhotoImage(master=v.root, file="./assets/github_dark.png")
    v.github_light = tkinter.PhotoImage(master=v.root, file="./assets/github_light.png")
    v.update_dark = tkinter.PhotoImage(master=v.root, file="./assets/update_dark.png")
    v.update_light = tkinter.PhotoImage(master=v.root, file="./assets/update_light.png")
    v.settings_light = tkinter.PhotoImage(master=v.root, file="./assets/settings_light.png")
    v.settings_dark = tkinter.PhotoImage(master=v.root, file="./assets/settings_dark.png")
