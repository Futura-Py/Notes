rmdir /Q /S dist
pyinstaller txt2.py --onefile --windowed --collect-data sv_ttk --icon "./assets/logo.ico"
rmdir /Q /S build
rmdir /Q /S __pycache__
del /Q /S txt2.spec