@echo off
setlocal

:: === CONFIGURATION ===
set PROJECT_NAME=ModParameter
for %%i in ("%cd%") do set PARENT_DIR=%%~dpi
set TEMP_DIR=%cd%\%PROJECT_NAME%
set OUTPUT_DIR=%PARENT_DIR%
set ARCHIVE_NAME=%PROJECT_NAME%.zip
set ZIP_EXE="C:\Program Files\7-Zip\7z.exe"

:: === Vérifie que 7-Zip existe ===
if not exist %ZIP_EXE% (
    echo ❌ 7z.exe introuvable. Modifie le chemin ZIP_EXE dans le script.
    pause
    exit /b
)

:: === Supprimer l’ancien dossier temporaire s’il existe ===
if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%"
)

:: === Créer le dossier temporaire ===
mkdir "%TEMP_DIR%"
mkdir "%TEMP_DIR%\src"
mkdir "%TEMP_DIR%\src\Entity"
mkdir "%TEMP_DIR%\src\ListIdItem"
mkdir "%TEMP_DIR%\src\Service"
mkdir "%TEMP_DIR%\src\Utils"
mkdir "%TEMP_DIR%\py"
mkdir "%TEMP_DIR%\py\Images"
mkdir "%TEMP_DIR%\py\JsonFiles"

:: === Copier les fichiers racine ===
copy /y "package.json" "%TEMP_DIR%\"
copy /y "README.md" "%TEMP_DIR%\"
copy /y "tsconfig.json" "%TEMP_DIR%\"

:: === Copier les fichiers src ===
copy /y "src\config.ts" "%TEMP_DIR%\src\"
copy /y "src\mod.ts" "%TEMP_DIR%\src\"
copy /y "src\README.md" "%TEMP_DIR%\src\"

xcopy /s /y /i "src\Entity" "%TEMP_DIR%\src\Entity\"
xcopy /s /y /i "src\ListIdItem" "%TEMP_DIR%\src\ListIdItem\"
xcopy /s /y /i "src\Service" "%TEMP_DIR%\src\Service\"
xcopy /s /y /i "src\Utils" "%TEMP_DIR%\src\Utils\"

:: === Copier les fichiers Python ===
xcopy /s /y /i "py\Images" "%TEMP_DIR%\py\Images\"
xcopy /s /y /i "py\JsonFiles" "%TEMP_DIR%\py\JsonFiles\"
copy /y "py\ModParameters.exe" "%TEMP_DIR%\"
copy /y "py\README.md" "%TEMP_DIR%\py\"

:: === Supprimer ancienne archive ===
if exist "%OUTPUT_DIR%\%ARCHIVE_NAME%" (
    del "%OUTPUT_DIR%\%ARCHIVE_NAME%"
)

:: === Créer l’archive proprement ===
pushd "%cd%"
%ZIP_EXE% a "%OUTPUT_DIR%\%ARCHIVE_NAME%" ".\%PROJECT_NAME%\"
popd

:: === Nettoyage ===
rmdir /s /q "%TEMP_DIR%"

echo.
echo Archive créée avec succès : %OUTPUT_DIR%\%ARCHIVE_NAME%
pause
