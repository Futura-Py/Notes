import ntkutils.cfgtools as cfgtools
from generatesize import system
import json

default_win = {
    "theme": "Dark",
    "font": "Helvetica",
    "font-size": 11,
    "mica": False,
    "hkey-open": "Control-o",
    "hkey-save": "Control-s",
    "linenumbers": True,
    "syntax-highlighting": False,
}

default_mac = {
    "theme": "Dark",
    "font": "Helvetica",
    "font-size": 11,
    "mica": False,
    "hkey-open": "Command-o",
    "hkey-save": "Command-s",
    "linenumbers": True,
    "syntax-highlighting": False, 
}

# Update Config if settings are missing
try:
    config_file = open("cfg.json")
    cfg = json.load(config_file)
    config_file.close()

    if len(cfg) != len(default_win):
        temp_cfg = default_win.copy()
        for i in cfg:
            temp_cfg.pop(i)
        for i in temp_cfg:
            cfg[i] = temp_cfg[i]
        cfgtools.SaveCFG(cfg)
except FileNotFoundError:
    pass

def get():
    if system != "Darwin":
        return cfgtools.init(default_win)
    else:
        return cfgtools.init(default_mac)