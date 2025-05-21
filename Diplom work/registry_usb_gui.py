import tkinter as tk
from tkinter import filedialog, messagebox
from Registry import Registry
import json
import os

def extract_usb_devices(file_path):
    try:
        registry = Registry(file_path)
        key = registry.open("ControlSet001\\Enum\\USBSTOR")
        devices = [subkey.name() for subkey in key.subkeys()]
        return devices
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при анализе файла: {str(e)}")
        return []

def choose_file():
    file_path = filedialog.askopenfilename(title="Выберите файл SYSTEM", filetypes=[("DAT files", "*.dat"), ("All files", "*.*")])
    if file_path:
        usb_devices = extract_usb_devices(file_path)
        if usb_devices:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Найденные USB-устройства:\n\n")
            for dev in usb_devices:
                result_text.insert(tk.END, f"- {dev}\n")
            save_result(usb_devices)
        else:
            result_text.insert(tk.END, "Устройства не найдены или файл некорректен.")

def save_result(data):
    try:
        with open("usb_devices.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Успех", "Результат сохранён в usb_devices.json")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", str(e))

# GUI
root = tk.Tk()
root.title("Извлечение USB из SYSTEM")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Выберите файл SYSTEM для анализа:", font=("Arial", 12))
label.pack(pady=5)

btn = tk.Button(frame, text="Выбрать файл", command=choose_file, font=("Arial", 12))
btn.pack(pady=10)

result_text = tk.Text(frame, width=60, height=20)
result_text.pack(pady=10)

root.mainloop()