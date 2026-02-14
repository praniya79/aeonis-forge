@echo off
REM Uninstall Seventh River FIRE autostart (Task Scheduler)
powershell -ExecutionPolicy Bypass -File "%~dp0uninstall-fire-autostart.ps1"
