@echo off

echo 🚀 Compilation avec PyInstaller...

echo pyinstaller --onefile --clean --name ModParameters --icon=Images/ModParameters.ico --distpath . main/main.py

echo pyinstaller --noupx --clean --name ModParameters --icon=Images/ModParameters.ico --distpath . main/main.py

py -3.12 -m nuitka --standalone --assume-yes-for-downloads \
  --nofollow-import-to=tkinter --nofollow-import-to=PIL \
  main.py
echo  Compilation terminée !
pause
