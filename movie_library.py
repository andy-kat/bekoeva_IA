import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

movies = []
displayed_movies = []

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
    return []

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

def update_treeview():
    """Обновляет таблицу фильмов на экране."""
    for i in tree.get_children():
        tree.delete(i)
    for movie in displayed_movies:
        tree.insert("", tk.END, values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            movie["rating"]
        ))

def add_movie():
    """Добавляет новый фильм в базу данных."""
    title = title_entry.get().strip()
    genre = genre_var.get()
    year_str = year_entry.get().strip()
    rating_str = rating_entry.get().strip()

    try:
        if not title:
            raise ValueError("Название фильма не может быть пустым.")
        if not year_str:
            raise ValueError("Год выпуска не может быть пустым.")
        if not rating_str:
            raise ValueError("Рейтинг не может быть пустым.")

        year = int(year_str)
        rating = float(rating_str)

        if rating < 1 or rating > 10:
            raise ValueError("Рейтинг должен быть от 1 до 10.")
        
        movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })
        displayed_movies.clear()
        displayed_movies.extend(movies)
        update_treeview()

        title_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        rating_entry.delete(0, tk.END)
        
        save_data()
        messagebox.showinfo("Успех", "Фильм добавлен!")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def apply_filter():
    """Применяет фильтр по жанру и году выпуска."""
    filter_genre = filter_genre_var.get()
    filter_year = filter_year_entry.get().strip()

    filtered = [m for m in movies if (filter_genre == "Все" or m["genre"] == filter_genre)]

    if filter_year:
        try:
            year_val = int(filter_year)
            filtered = [m for m in filtered if m["year"] == year_val]
        except ValueError:
            messagebox.showerror("Ошибка", "Год для фильтра должен быть числом.")
            return

    displayed_movies.clear()
    displayed_movies.extend(filtered)
    update_treeview()

def reset_filter():
    """Сбрасывает фильтр и показывает все фильмы."""
    filter_genre_var.set("Все")
    filter_year_entry.delete(0, tk.END)
    displayed_movies.clear()
    displayed_movies.extend(movies)
    update_treeview()

movies = load_data()
displayed_movies = movies.copy()

#окна фильмотека
root = tk.Tk()
root.title("Movie Library")
root.geometry("900x600")

filter_frame = ttk.LabelFrame(root, text="Фильтр", padding="5")
filter_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(filter_frame, text="Жанр:").pack(side="left", padx=5)
filter_genre_var = tk.StringVar(value="Все")
genre_options = ["Боевик", "Комедия", "Драма", "Фантастика", "Триллер", "Все"]
ttk.Combobox(filter_frame, textvariable=filter_genre_var, values=genre_options,
             state="readonly", width=12).pack(side="left", padx=5)

ttk.Label(filter_frame, text="Год выпуска:").pack(side="left", padx=5)
filter_year_entry = ttk.Entry(filter_frame, width=12)
filter_year_entry.pack(side="left", padx=5)

ttk.Button(filter_frame, text="Применить фильтр", command=apply_filter).pack(side="left", padx=5)
ttk.Button(filter_frame, text="Сбросить фильтр", command=reset_filter).pack(side="left", padx=5)

input_frame = ttk.LabelFrame(root, text="Добавить фильм", padding="10")
input_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(input_frame, text="Название фильма").grid(row=0, column=0, sticky="w", pady=2)
title_entry = ttk.Entry(input_frame, width=35)
title_entry.grid(row=0, column=1, sticky="we", pady=2)

ttk.Label(input_frame, text="Жанр").grid(row=1, column=0, sticky="w", pady=2)
genre_var = tk.StringVar()
genre_values = ["Боевик", "Комедия", "Драма", "Фантастика", "Триллер"]
ttk.Combobox(input_frame, textvariable=genre_var, values=genre_values,
             state="readonly", width=32).grid(row=1, column=1, sticky="we", pady=2)
genre_var.set(genre_values[0])

ttk.Label(input_frame, text="Год выпуска").grid(row=2, column=0, sticky="w", pady=2)
year_entry = ttk.Entry(input_frame, width=35)
year_entry.grid(row=2, column=1, sticky="we", pady=2)

ttk.Label(input_frame, text="Рейтинг (от 1 до 10)").grid(row=3, column=0, sticky="w", pady=2)
rating_entry = ttk.Entry(input_frame, width=35)
rating_entry.grid(row=3, column=1, sticky="we", pady=2)

ttk.Button(input_frame, text="Добавить фильм", command=add_movie).grid(row=4, column=0, columnspan=2, pady=15)


table_container = ttk.Frame(root)
table_container.pack(fill='both', expand=True, padx=10, pady=5)

yscrollbar = ttk.Scrollbar(table_container, orient="vertical")
xscrollbar = ttk.Scrollbar(table_container, orient="horizontal")
tree = ttk.Treeview(table_container,
                    columns=("title", "genre", "year", "rating"),
                    show='headings',
                    yscrollcommand=yscrollbar.set,
                    xscrollcommand=xscrollbar.set,
                    height=15) 

yscrollbar.config(command=tree.yview)
xscrollbar.config(command=tree.xview)
tree.heading("title", text="Название")
tree.heading("genre", text="Жанр")
tree.heading("year", text="Год")
tree.heading("rating", text="Рейтинг")
tree.column("rating", width=80) #ширина на рейтинг фильмв

tree.grid(row=0, column=0, sticky='nsew')
yscrollbar.grid(row=0, column=1, sticky='ns')
xscrollbar.grid(row=1, column=0, sticky='ew')
table_container.grid_rowconfigure(0, weight=1)
table_container.grid_columnconfigure(0, weight=1)

update_treeview()
root.mainloop()
