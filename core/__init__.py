from .memoryeditor import MemoryEditor
    

def main():

    try:
        # Имя процесса игры (например, notepad.exe для тестирования)
        process_name = str(input("\nВведите имя процесса (например TQ.exe): "))
        
        # Значение, которое нужно найти
        search_value = int(input('\nВведите искомое целочисленное значение: '))  # Например, количество здоровья
        
        # Значение, на которое нужно заменить найденное
        replace_value = int(input('\nНовое значение: '))  # Новое значение здоровья

    except Exception as e:
        print('\nYOU DIED\n')
        exit()
    
    editor = MemoryEditor(process_name)
    
    # Поиск значений
    print(f"Поиск адресов со значением: {search_value}\n")
    found_addresses = editor.search_value(search_value)

    
    if found_addresses:
         while True:

            if len(found_addresses) == 1:
                editor.replace_value(found_addresses, replace_value)

            else:
                print(f"Найдено {len(found_addresses)} адресов со значением {search_value}.")
                print("""
Ввеедите:
    1 - Чтобы изменить значение во всех ячейках.
    2 - Чтобы отфильтровать адреса.
    0 - Чтобы выйти.\n                                                            
""")
                action = int(input(">>> "))

                if action == 1:
                    print("Изменяем значения...")
                    editor.replace_value(found_addresses, replace_value)
                if action == 2:
                    next_value = int(input('Измените значение в игре и введите новое: '))
                    found_addresses = editor.search_next_value(found_addresses, next_value)
                if action == 0:
                    print("Программа завершила работу.")
                    break
    else:
        print("Значение не найдено в памяти процесса.")