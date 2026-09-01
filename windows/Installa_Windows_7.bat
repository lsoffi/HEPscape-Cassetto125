@echo off
title Installazione HEPscape! - Windows 7
cd /d "%~dp0"
echo.
echo HEPscape! - preparazione Windows 7
echo ==================================
echo.
python --version
if errorlevel 1 (
  echo ERRORE: Python non e stato trovato.
  echo Installa Python 3.8.10 a 64 bit e seleziona "Add Python to PATH".
  pause
  exit /b 1
)
echo.
echo Installazione del componente seriale...
python -m pip install --user pyserial==3.5
if errorlevel 1 (
  echo ERRORE: installazione non riuscita.
  pause
  exit /b 1
)
echo.
echo Installazione completata.
echo Ora puoi usare Avvia_HEPscape_Windows.bat
pause
