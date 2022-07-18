import sv_ttk, darkdetect, ntkutils

import vars as v
import generatesize as size
import tabmanager

def applysettings(ignoretheme=False, first=False):
    if not ignoretheme:
        if v.cfg["theme"] == "System": sv_ttk.set_theme(darkdetect.theme().lower())
        else: sv_ttk.set_theme(v.cfg["theme"].lower()) 

        if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()): 
            if size.system != "Darwin":
                ntkutils.dark_title_bar(v.root)

            v.header.configure(bg="#202020")
            v.tabbar.configure(bg="#202020")
            v.footer.configure(bg="#202020")

            v.closeimg.configure(file="assets/close_light.png")
            v.closeimg2.configure(file="assets/close_dark.png")

            selected_hover = "#51b7eb"
            selected = "#57c8ff"
            normal = "#2a2a2a"
            normal_hover = "#2f2f2f"
        else: 
            v.header.configure(bg="#f3f3f3")
            v.tabbar.configure(bg="#f3f3f3")
            v.footer.configure(bg="#f3f3f3")

            v.closeimg.configure(file="assets/close_dark.png")
            v.closeimg2.configure(file="assets/close_light.png")

            normal = "#fdfdfd"
            normal_hover = "#f9f9f9"
            selected = "#0560b6"
            selected_hover = "#1e6fbc"

    if first:
        if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
            if size.system != "Darwin":
                ntkutils.dark_title_bar(v.root)
            
            selected_hover = "#51b7eb"
            selected = "#57c8ff"
            normal = "#2a2a2a"
            normal_hover = "#2f2f2f"
        else:
            v.header.configure(bg="#f3f3f3")
            v.tabbar.configure(bg="#f3f3f3")
            v.footer.configure(bg="#f3f3f3")
            
            normal = "#fdfdfd"
            normal_hover = "#f9f9f9"
            selected = "#0560b6"
            selected_hover = "#1e6fbc"

            v.closeimg.configure(file="assets/close_dark.png")
            v.closeimg2.configure(file="assets/close_light.png")

    v.textwidget.text.configure(font=(v.cfg["font"], int(v.cfg["font-size"])))

    if v.cfg["mica"]: 
        if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
            ntkutils.blur_window_background(v.root, dark=True)
            v.textwidget.text.configure(bg="#1b1c1b")
        else:
            ntkutils.blur_window_background(v.root)
            v.textwidget.text.configure(bg="#fafbfa")

    v.normal = normal
    v.selected = selected
    v.normal_hover = normal_hover
    v.selected_hover = selected_hover

    tabmanager.buildtabs()