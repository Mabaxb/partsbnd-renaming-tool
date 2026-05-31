@echo off
setlocal enabledelayedexpansion

for %%F in (*.dcx) do (
    set "filename=%%F"
    set "newname=!filename:.partsbnd.dcx=_l.partsbnd.dcx!"
    copy "%%F" "!newname!"
)

endlocal
echo Done
pause >nul