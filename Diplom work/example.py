import json
import winreg
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

def get_registry_data():
    """Функция для извлечения данных из реестра"""
    data = {
        "USB Devices": get_usb_devices(),
        "Recently Executed Programs": get_recently_executed(),
        "Network Connections": get_network_connections(),
        "Autorun Programs": get_autorun_programs(),
        "Installed Programs": get_installed_programs()
    }
    return data

def get_usb_devices():
    """Извлекает список подключенных USB-устройств"""
    usb_devices = []
    registry_path = r"SYSTEM\CurrentControlSet\Enum\USB"
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, registry_path)
        i = 0
        while True:
            try:
                device_name = winreg.EnumKey(key, i)
                usb_devices.append(device_name)
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
    except Exception as e:
        log_error(f"Ошибка при доступе к реестру USB-устройств: {e}")
    return usb_devices

def get_recently_executed():
    """Извлекает список недавно выполненных программ"""
    recent_programs = []
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(reg, registry_path)
        i = 0
        while True:
            try:
                value_name, value_data, _ = winreg.EnumValue(key, i)
                recent_programs.append(value_name)
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
    except Exception as e:
        log_error(f"Ошибка при доступе к реестру недавно выполненных программ: {e}")
    return recent_programs

def get_network_connections():
    """Извлекает информацию о сетевых подключениях"""
    network_connections = []
    registry_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles"
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, registry_path)
        i = 0
        while True:
            try:
                profile_name = winreg.EnumKey(key, i)
                network_connections.append(profile_name)
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
    except Exception as e:
        log_error(f"Ошибка при доступе к реестру сетевых подключений: {e}")
    return network_connections

def get_autorun_programs():
    """Извлекает список программ, запускаемых при старте системы"""
    autorun_programs = []
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, registry_path)
        i = 0
        while True:
            try:
                value_name, value_data, _ = winreg.EnumValue(key, i)
                autorun_programs.append(f"{value_name}: {value_data}")
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
    except Exception as e:
        log_error(f"Ошибка при доступе к реестру автозапуска: {e}")
    return autorun_programs

def get_installed_programs():
    """Извлекает список установленных программ"""
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    programs = []
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, registry_path)
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = f"{registry_path}\\{subkey_name}"
                subkey = winreg.OpenKey(reg, subkey_path)
                try:
                    display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    programs.append(display_name)
                except FileNotFoundError:
                    pass
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
    except Exception as e:
        log_error(f"Ошибка при доступе к реестру: {e}")
    return programs

def log_error(message):
    """Записывает ошибки в файл"""
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def save_to_json(data):
    """Сохраняет извлеченные данные в JSON"""
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[["JSON files", "*.json"]])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Сохранение", "Данные успешно сохранены!")

def extract_data():
    """Функция для извлечения данных и их отображения"""
    progress.start()
    threading.Thread(target=extract_and_display, daemon=True).start()

def extract_and_display():
    data = get_registry_data()
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, json.dumps(data, indent=4, ensure_ascii=False))
    text_output.config(state=tk.DISABLED)
    progress.stop()

def create_gui():
    """Создание GUI приложения"""
    global text_output, progress
    root = tk.Tk()
    root.title("Forensics Extractor")
    root.geometry("700x500")
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    extract_button = ttk.Button(frame, text="Извлечь данные", command=extract_data)
    extract_button.pack(pady=5)
    save_button = ttk.Button(frame, text="Сохранить JSON", command=lambda: save_to_json(get_registry_data()))
    save_button.pack(pady=5)
    progress = ttk.Progressbar(frame, mode='indeterminate')
    progress.pack(pady=5, fill=tk.X)
    text_output = tk.Text(frame, height=20, width=80, state=tk.DISABLED)
    scrollbar = ttk.Scrollbar(frame, command=text_output.yview)
    text_output.config(yscrollcommand=scrollbar.set)
    text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
