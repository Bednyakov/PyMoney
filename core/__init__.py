import threading
import tkinter as tk
from tkinter import ttk, messagebox
from .memoryeditor import MemoryEditor
from .processes_getter import get_process_names

class MenuEditor:
    def __init__(self, root):
        self.root = root
        self.editor = None
        self.root.title("Memory Editor")
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.process_var = tk.StringVar()
        self.current_value_var = tk.IntVar()
        self.desired_value_var = tk.IntVar()

        processes = get_process_names()

        tk.Label(self.root, text="Выберите процесс").grid(row=0, column=0, pady=10)
        self.process_combobox = ttk.Combobox(self.root, textvariable=self.process_var, values=processes)
        self.process_combobox.grid(row=0, column=1, pady=10)

        tk.Label(self.root, text="Настоящее значение").grid(row=1, column=0, pady=10)
        self.current_value_entry = tk.Entry(self.root, textvariable=self.current_value_var)
        self.current_value_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.root, text="Желаемое значение").grid(row=2, column=0, pady=10)
        self.desired_value_entry = tk.Entry(self.root, textvariable=self.desired_value_var)
        self.desired_value_entry.grid(row=2, column=1, pady=10)

        tk.Button(self.root, text="Начать поиск", command=self.start_search).grid(row=3, column=0, columnspan=2, pady=20)

    def start_search(self):
        process_name = self.process_var.get()
        current_value = self.current_value_var.get()
        self.editor = MemoryEditor(process_name)
        

        if not process_name or not current_value:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return
        
        # Создаем новое окно загрузки
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Загрузка")
        tk.Label(self.loading_window, text="Идёт сканирование памяти, пожалуйста, подождите...").pack(padx=20, pady=20)

        # Запускаем поиск в новом потоке
        threading.Thread(target=self.perform_search, args=(int(current_value),)).start()

    def perform_search(self, current_value):
        self.search_results = self.editor.search_value(int(current_value))  # поиск значения в памяти

        if len(self.search_results) > 1:
            self.show_filter_window()
        else:
            messagebox.showinfo("Результат", "Значение найдено и изменено.")
            self.create_main_menu()

        # Закрываем окно загрузки после завершения поиска
        self.loading_window.destroy()

        if len(self.search_results) > 1:
            self.show_filter_window()
        else:
            messagebox.showinfo("Результат", "Значение найдено и изменено.")
            self.create_main_menu()

    def show_filter_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.new_value_var = tk.StringVar()

        tk.Label(self.root, text=f"Количество элементов соответствующих поиску: {len(self.search_results)}").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.root, text="Новое значение").grid(row=1, column=0, pady=10)
        self.new_value_entry = tk.Entry(self.root, textvariable=self.new_value_var)
        self.new_value_entry.grid(row=1, column=1, pady=10)

        tk.Button(self.root, text="Отфильтровать по новому значению", command=self.filter_values).grid(row=2, column=0, pady=20)
        tk.Button(self.root, text="Изменить во всех", command=self.replace_values).grid(row=2, column=1, pady=20)

    def filter_values(self):
        new_value = self.new_value_var.get()

        if not new_value:
            messagebox.showerror("Ошибка", "Пожалуйста, введите новое значение.")
            return

        self.search_results = self.editor.search_next_value(self.search_results, int(new_value)) #  Вызов функции фильтрации значений

        if len(self.search_results) > 1:
            self.show_filter_window()
        else:
            messagebox.showinfo("Результат", "Значение найдено и изменено.")
            self.replace_values()
            self.create_main_menu()

    def replace_values(self):
        desired_value = int(self.desired_value_var.get())
        self.editor.replace_value(self.search_results, desired_value)  # Вызов функции замены значений

        messagebox.showinfo("Успех", "Значение было изменено.")
        self.create_main_menu()