rmdir /Q /S dist
pyinstaller ./src/main.py --onefile --windowed --collect-data sv_ttk --collect-all tkinterweb --icon "./assets/logo.ico"
rmdir /Q /S build
rmdir /Q /S __pycache__
del /Q /S main.spec