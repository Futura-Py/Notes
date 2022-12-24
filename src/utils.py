import darkdetect

import vars as v


def dark():
    if v.cfg["theme"] == "Dark" or (v.cfg["theme"] == "System" and darkdetect.isDark()):
        return True
    else:
        return False