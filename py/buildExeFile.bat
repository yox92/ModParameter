@echo off

echo 🚀 Compilation avec PyInstaller...

pyinstaller --onefile --clean --name ModParameters --icon=Images/ModParameters.ico --distpath . --add-data "JsonFiles;JsonFiles" --add-data "Images;Images" main/main.py

echo  Compilation terminée !
pause
