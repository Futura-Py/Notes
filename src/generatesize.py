from win32api import GetMonitorInfo, MonitorFromPoint

def get():
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area = monitor_info.get("Work")
    return "{}x{}".format(work_area[2] - 40, work_area[3] - 80)