@echo off
title Anti-Cheat Requirements Installer par SH4FS0c13ty
chcp 65001
SET dir=%~dp0
cls
echo.
echo  █████╗ ███╗   ██╗████████╗██╗       ██████╗██╗  ██╗███████╗ █████╗ ████████╗
echo ██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
echo ███████║██╔██╗ ██║   ██║   ██║█████╗██║     ███████║█████╗  ███████║   ██║   
echo ██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║     ██╔══██║██╔══╝  ██╔══██║   ██║   
echo ██║  ██║██║ ╚████║   ██║   ██║      ╚██████╗██║  ██║███████╗██║  ██║   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝       ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
echo.
echo Anti-Cheat Requirements Installer par SH4FS0c13ty
echo.
goto admin_check

:startmsg
echo 1 - Installation complète (Python 3.7.4 + Dépendances Python + Tesseract + Données formées pour Tesseract)
echo 2 - Installation basique (Dépendances Python + Tesseract + Données formées pour Tesseract)
echo.
echo 0 - Quitter Anti-Cheat Requirements Installer

:prompt
echo.
set /p start=Entrez un chiffre [0~2]:~$ 
echo.
if /i "%start%" EQU "0" exit
if /i "%start%" EQU "1" goto full_install
if /i "%start%" EQU "2" goto basic_install

echo Unknown number.

goto prompt

:admin_check
call :isAdmin
if %errorlevel% == 0 (
	goto startmsg
) else (
	echo Erreurr: Anti-Cheat Requirements Installer n'a pas les permissions adminitrateur.
	echo Redémarrage avec les droits administrateur ...
	powershell.exe Start-Process '%dir%\Anti-Cheat Requirements Installer.bat' -Verb runAs
)

:isAdmin
fsutil dirty query %systemdrive% >nul
exit /b

:full_install
echo Téléchargement de Python 3.7.4 x86 ...
"%dir%\setup\curl.exe" -# -k -o "%dir%\setup\python_3.7.4_x86.exe" https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe
echo Installation de Python 3.7.4 x86 ...
"%dir%\setup\python_3.7.4_x86.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
setx path "%path%"
del "%dir%\setup\python_3.7.4_x86.exe"
echo Installation des dépendances Python ...
IF EXIST "C:\Program Files (x86)\Python37-32" (
	"C:\Program Files (x86)\Python37-32\python.exe" -m pip install -r "%dir%\setup\requirements.txt"
) ELSE (
	"C:\Program Files\Python37-32\python.exe" -m pip install -r "%dir%\setup\requirements.txt"
)
echo Téléchargement de Tesseract 5 x86 ...
"%dir%\setup\curl.exe" -# -k -o "%dir%\setup\tesseract_v5_x86.exe" https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20190708.exe
echo Installation de Tesseract ...
"%dir%\setup\tesseract_v5_x86.exe" /S
IF EXIST "C:\Program Files (x86)\Tesseract-OCR" (
	setx path "%path%;C:\Program Files (x86)\Tesseract-OCR"
	copy "%dir%\setup\ita.traineddata" "C:\Program Files (x86)\Tesseract-OCR\tessdata\ita.traineddata"
) ELSE (
	setx path "%path%;C:\Program Files\Tesseract-OCR"
	copy "%dir%\setup\ita.traineddata" "C:\Program Files\Tesseract-OCR\tessdata\ita.traineddata"
)
echo.
goto end

:basic_install
echo Installation des dépendances Python ...
IF EXIST "C:\Program Files (x86)\Python37-32" (
	"C:\Program Files (x86)\Python37-32\python.exe" -m pip install -r "%dir%\setup\requirements.txt"
) ELSE (
	"C:\Program Files\Python37-32\python.exe" -m pip install -r "%dir%\setup\requirements.txt"
)
echo Téléchargement de Tesseract 5 x86 ...
"%dir%\setup\curl.exe" -# -k -o "%dir%\setup\tesseract_v5_x86.exe" https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20190708.exe
echo Installation de Tesseract ...
"%dir%\setup\tesseract_v5_x86.exe" /S
IF EXIST "C:\Program Files (x86)\Tesseract-OCR" (
	setx path "%path%;C:\Program Files (x86)\Tesseract-OCR"
	copy "%dir%\setup\ita.traineddata" "C:\Program Files (x86)\Tesseract-OCR\tessdata\ita.traineddata"
) ELSE (
	setx path "%path%;C:\Program Files\Tesseract-OCR"
	copy "%dir%\setup\ita.traineddata" "C:\Program Files\Tesseract-OCR\tessdata\ita.traineddata"
)
echo.
goto end

:end
echo Dépendances d'Anti-Cheat installées.
pause