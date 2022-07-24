import sv_ttk, darkdetect, ntkutils

import vars as v
import generatesize as size
import tabmanager

def applysettings():
    if v.cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
    else: sv_ttk.set_theme(v.cfg["theme"].lower()) 

    if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()): 
        v.footer.configure(bg="#202020")
        v.closeimg.configure(file="assets/close_light.png")
        v.closeimg2.configure(file="assets/close_dark.png")

        selected_hover = "#51b7eb"
        selected = "#57c8ff"
        normal = "#2a2a2a"
        normal_hover = "#2f2f2f"

        try: v.textwidget.numberLines.mode = "dark"
        except AttributeError: pass
    else: 
        v.footer.configure(bg="#f3f3f3")
        v.closeimg.configure(file="assets/close_dark.png")
        v.closeimg2.configure(file="assets/close_light.png")

        normal = "#fdfdfd"
        normal_hover = "#f9f9f9"
        selected = "#0560b6"
        selected_hover = "#1e6fbc"

        try: v.textwidget.numberLines.mode = "light"
        except AttributeError: pass

    v.textwidget.text.configure(font=(v.cfg["font"], int(v.cfg["font-size"])))

    if v.cfg["mica"]: 
        if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
            v.tabbar.configure(bg="#1c1c1c")
            ntkutils.blur_window_background(v.root, dark=True)
            v.textwidget.text.configure(bg="#1b1c1b")
            try: v.textwidget.numberLines.configure(bg="#1b1c1b") 
            except: pass
        else:
            ntkutils.blur_window_background(v.root)
            v.textwidget.text.configure(bg="#fafbfa")

    v.normal = normal
    v.selected = selected
    v.normal_hover = normal_hover
    v.selected_hover = selected_hover

    try: v.textwidget.numberLines.redraw()
    except AttributeError: pass
    tabmanager.buildtabs()