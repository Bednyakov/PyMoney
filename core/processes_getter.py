import ctypes
import ctypes.wintypes as wintypes

# Определение необходимых структур и констант
TH32CS_SNAPPROCESS = 0x00000002
INVALID_HANDLE_VALUE = -1

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * wintypes.MAX_PATH),
    ]

def get_process_names():
    process_names = []

    # Создание снимка всех запущенных процессов в системе
    snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == INVALID_HANDLE_VALUE:
        raise Exception("Failed to create snapshot")

    process_entry = PROCESSENTRY32()
    process_entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

    # Получение информации о первом процессе
    success = ctypes.windll.kernel32.Process32First(snapshot, ctypes.byref(process_entry))
    while success:
        process_name = process_entry.szExeFile.decode('utf-8')
        process_names.append(process_name)
        # Переход к следующему процессу
        success = ctypes.windll.kernel32.Process32Next(snapshot, ctypes.byref(process_entry))

    # Закрытие дескриптора снимка
    ctypes.windll.kernel32.CloseHandle(snapshot)

    return list(set(process_names))


if __name__ == "__main__":
    processes = get_process_names()
    for process_name in processes:
        print(process_name)