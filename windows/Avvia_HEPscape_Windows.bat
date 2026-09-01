@echo off
title HEPscape! - Cassetto 125
cd /d "%~dp0\.."
python windows\relay_server_windows.py
echo.
echo Il server si e fermato. Controlla eventuali errori qui sopra.
pause
