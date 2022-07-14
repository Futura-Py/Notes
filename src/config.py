import ntkutils.cfgtools as cfgtools

def get():
    return cfgtools.init({
    "theme": "Dark",
    "font": "Helvetica",
    "font-size": 11,
    "mica": False,
    "hkey-open": "Control-o",
    "hkey-save": "Control-s",
    })