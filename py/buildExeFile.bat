@echo off
echo 🧹 Nettoyage des anciennes versions...
rmdir /s /q build dist

echo 🚀 Compilation avec PyInstaller...
pyinstaller --onefile --clean --name test --add-data "JsonFiles;JsonFiles" --add-data "Images;Images" main/main.py

echo ✅ Compilation terminée ! Le fichier final est dist\test.exe
pause
