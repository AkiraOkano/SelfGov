echo off
cd /d %~dp0

SET result=0
SET count=0

:loop

if %count% neq 0 powershell sleep 3

\pleiades\python\3\python Counter.py 
SET result=%ERRORLEVEL%

SET /a count=%count%+1
echo %count% >> SelfGov.log

if %result% equ 1 if %count% lss 3 goto :loop

