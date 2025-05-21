from Registry import Registry

def extract_usb_devices_from_system(system_dat_path):
    registry = Registry(system_dat_path)
    
    try:
        usb_key = registry.open("ControlSet001\\Enum\\USBSTOR")
        devices = [subkey.name() for subkey in usb_key.subkeys()]
        return devices
    except Registry.RegistryKeyNotFoundException:
        print("Ключ USBSTOR не найден.")
        return []

if name == "__main__":
    path = "C:\\Users\\erk\\Desktop\\samples\\SYSTEM"  # путь к файлу
    result = extract_usb_devices_from_system(path)
    
    for device in result:
        print(f"Найдено устройство: {device}")