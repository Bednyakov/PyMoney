from .memoryeditor import MemoryEditor
    

def main():

    try:
        process_name = str(input("\nВведите имя процесса (например TQ.exe): "))
        
        search_value = int(input('\nВведите искомое целочисленное значение: '))
        
        replace_value = int(input('\nНовое значение: '))

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
                print(f"Значение изменено.")
                exit()

            else:
                print(f"Найдено {len(found_addresses)} адресов с искомым значением.")
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
                    action = 0
                if action == 2:
                    next_value = int(input('Измените значение в игре и введите новое: '))
                    found_addresses = editor.search_next_value(found_addresses, next_value)
                if action == 0:
                    print("Программа завершила работу.")
                    exit()
    else:
        print("Значение не найдено в памяти процесса.")