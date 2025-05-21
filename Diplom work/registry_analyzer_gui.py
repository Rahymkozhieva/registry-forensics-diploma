import tkinter as tk
from tkinter import filedialog, messagebox
import Registry
import json
import os

report_data = {}

def extract_usb_devices(file_path):
    try:
        registry = Registry.Registry(file_path)
        key = registry.open("ControlSet001\\Enum\\USBSTOR")
        devices = [subkey.name() for subkey in key.subkeys()]
        report_data["USB Devices"] = devices
        return devices
    except Exception as e:
        return ["USBSTOR не найден или файл не является SYSTEM"]

def extract_autorun(file_path):
    try:
        registry = Registry.Registry(file_path)
        run_key = registry.open("Software\\Microsoft\\Windows\\CurrentVersion\\Run")
        autorun = {v.name(): v.value() for v in run_key.values()}
        report_data["Autorun Programs"] = autorun
        return autorun
    except Exception as e:
        return {"Ошибка": "Run не найден или файл не является NTUSER.DAT"}

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Выберите .DAT файл", 
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )
    if not file_path:
        return

    filename = os.path.basename(file_path).lower()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Анализ файла: {filename}\n\n")

    if "system" in filename:
        usb_devices = extract_usb_devices(file_path)
        result_text.insert(tk.END, "🔌 USB-устройства:\n")
        for dev in usb_devices:
            result_text.insert(tk.END, f" - {dev}\n")
        result_text.insert(tk.END, "\n")

    if "ntuser" in filename:
        autorun = extract_autorun(file_path)
        result_text.insert(tk.END, "🚀 Программы автозагрузки:\n")
        for name, val in autorun.items():
            result_text.insert(tk.END, f" - {name}: {val}\n")
        result_text.insert(tk.END, "\n")

    save_report()

def save_report():
    try:
        with open("registry_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Успех", "Отчёт сохранён в registry_report.json")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", str(e))

# GUI
root = tk.Tk()
root.title("Извлечение данных из .DAT файлов")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Выберите .DAT файл для анализа", font=("Arial", 12))
label.pack(pady=5)

btn = tk.Button(frame, text="Выбрать файл", command=choose_file, font=("Arial", 12))
btn.pack(pady=10)

result_text = tk.Text(frame, width=80, height=25)
result_text.pack(pady=10)

root.mainloop()