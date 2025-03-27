@echo off
setlocal

:: === CONFIGURATION ===
set PROJECT_NAME=ModParameter
for %%i in ("%cd%") do set PARENT_DIR=%%~dpi
set OUTPUT_DIR=%PARENT_DIR%
set ARCHIVE_NAME=%PROJECT_NAME%.zip
set ZIP_EXE="C:\Program Files\7-Zip\7z.exe"

:: === Vérifie que 7-Zip existe ===
if not exist %ZIP_EXE% (
    echo ❌ 7z.exe introuvable. Modifie le chemin ZIP_EXE dans le script.
    pause
    exit /b
)

:: === Créer dossier dist si besoin ===
if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

:: === Supprimer ancienne archive ===
if exist "%OUTPUT_DIR%\%ARCHIVE_NAME%" (
    del "%OUTPUT_DIR%\%ARCHIVE_NAME%"
)

:: === Créer l’archive proprement ===
%ZIP_EXE% a "%OUTPUT_DIR%\%ARCHIVE_NAME%" "package.json" "README.md" "tsconfig.json" "src\Entity\*" "src\ListIdItem\*" "src\Service\*" "src\Utils\*" "src\config.ts" "src\mod.ts" "src\README.md" "py\Images\*" "py\JsonFiles\*" "py\README.MD"

echo.
echo ✅ Archive créée avec succès : %OUTPUT_DIR%\%ARCHIVE_NAME%
pause
