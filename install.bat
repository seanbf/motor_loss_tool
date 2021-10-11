@ECHO off
cls
:start
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%ps_script.ps1
ECHO.
ECHO ################################
ECHO [ Motor Loss Tool Install ]
ECHO ################################
ECHO. 
ECHO    [1] Install Python 3.9.5, Paths, Dependancies and Launch motor_loss_tool [Powershell]
ECHO. 
ECHO    [2] Install Dependancies and Launch motor_loss_tool
ECHO. 

set choice=
set /p choice=Type the [number] of the option you want to use.
ECHO. 

if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto install_full
if '%choice%'=='2' goto install_dep

ECHO "%choice%" is not valid, try again
ECHO.
goto start

:install_full
ECHO Installing Python 3.9.5, Paths, Dependancies and Launching motor_loss_tool
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}"
goto end

:install_dep
ECHO Installing Dependancies and Launching motor_loss_tool
py -3.9 -m pip install -r requirements.txt
py -3.9 -m streamlit run motor_loss_tool.py
goto end

:end
pause