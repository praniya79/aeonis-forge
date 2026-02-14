@echo off
REM Seventh River launcher: ensure theme patch is applied, then start TUI.
CALL "%~dp0apply-seventh-river-theme.cmd"
openclaw tui
