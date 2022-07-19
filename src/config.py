import ntkutils.cfgtools as cfgtools
from generatesize import system

def get():
    if system != "Darwin":
        return cfgtools.init({
        "theme": "Dark",
        "font": "Helvetica",
        "font-size": 11,
        "mica": False,
        "hkey-open": "Control-o",
        "hkey-save": "Control-s",
        "linenumbers": True,
        })
    else:
        return cfgtools.init({
        "theme": "Dark",
        "font": "Helvetica",
        "font-size": 11,
        "mica": False,
        "hkey-open": "Command-o",
        "hkey-save": "Command-s",
        "linenumbers": True,
        })