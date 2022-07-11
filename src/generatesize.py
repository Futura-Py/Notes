import platform
system = platform.system()
if system == "Windows":
    from win32api import GetMonitorInfo, MonitorFromPoint

    def get():
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get("Work")
        return "{}x{}".format(work_area[2] - 40, work_area[3] - 80)
else:
    import tkinter
    root = tkinter.Tk()
    root.withdraw()
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    def get():
        return "{}x{}".format(WIDTH, HEIGHT-100)