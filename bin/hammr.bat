@echo off
:: %~dp0 == drive and path of this bat file (including trailing \)
:: %~n0 == filename of this bat file (without .xxx extension)
:: %* == all command line parameters
python.exe "%~dp0%~n0" %*