@echo off
set "PYW=C:\Users\DELL\AppData\Local\Programs\Python\Python314\pythonw.exe"
if not exist "%PYW%" set "PYW=pyw"
start "" "%PYW%" "%~dp0bsod_prank.py"
