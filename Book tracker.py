import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

# Имя файла для хранения данных
DATA_FILE = 'book_data.json'


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        
        self.books = []
        self.load_data()

        # Поля для ввода
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(padx=10, pady=10)

        tk.Label(self.entry_frame, text="Название книги").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.entry_frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.entry_frame, text="Автор").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.entry_frame)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.entry_frame, text="Жанр").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.entry_frame)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.entry_frame, text="Количество страниц").grid(row=3, column=0)
        self.pages_entry = tk.Entry(self.entry_frame)
        self.pages_entry.grid(row=3, column=1)

        self.btn_add = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.btn_add.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(padx=10, pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0)
        self.genre_filter_var = tk.StringVar()
        self.genre_filter = ttk.Combobox(filter_frame, textvariable=self.genre_filter_var)
        self.genre_filter['values'] = ['Все']
        self.genre_filter.current(0)
        self.genre_filter.grid(row=0, column=1)
        self.genre_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр страниц >").grid(row=0, column=2, padx=5)
        self.pages_filter_var = tk.StringVar()
        self.pages_filter_entry = tk.Entry(filter_frame, textvariable=self.pages_filter_var, width=5)
        self.pages_filter_entry.grid(row=0, column=3)
        self.pages_filter_entry.bind("<KeyRelease>", self.apply_filters)

        self.btn_reset = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filters)
        self.btn_reset.grid(row=0, column=4, padx=5)

        # Таблица отображения
        self.tree = ttk.Treeview(root, columns=("Автор", "Жанр", "Страниц"), show='headings', height=10)
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страниц", text="Страниц")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.update_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
        else:
            self.books = []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        # Проверка
        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return
        pages = int(pages_str)

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        self.save_data()
        self.update_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

        # Обновление фильтров
        if genre not in self.genre_filter['values']:
            self.genre_filter['values'] = list(self.genre_filter['values']) + [genre]

    def update_table(self, filtered_books=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if filtered_books is None:
            filtered_books = self.books

        for book in filtered_books:
            self.tree.insert('', tk.END, values=(book['author'], book['genre'], book['pages']))

    def apply_filters(self, event=None):
        genre_filter = self.genre_filter_var.get()
        pages_filter_str = self.pages_filter_var.get()

        filtered = self.books
        if genre_filter != 'Все' and genre_filter != '':
            filtered = [b for b in filtered if b['genre'] == genre_filter]

        if pages_filter_str.isdigit():
            pages_threshold = int(pages_filter_str)
            filtered = [b for b in filtered if b['pages'] > pages_threshold]

        self.update_table(filtered)

    def reset_filters(self):
        self.genre_filter_var.set('Все')
        self.pages_filter_var.set('')
        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
