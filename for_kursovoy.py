import sqlite3 as sq
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class App(tk.Tk):
    def __init__(self, base):
        # Инициализация окна
        self.df = base
        super().__init__()
        self.title('Курсовой')
        self.geometry(f'1920x520+0+0')
        self.resizable(False, False)
        self['bg'] = '#00FFB3'
        for i in range(1, 4):
            self.rowconfigure(i, minsize=50)

        # Инициализация дерева
        self.tree = ttk.Treeview(self, selectmode=tk.EXTENDED, show='headings',
                                 columns=(', '.join([f'#{str(i)}' for i in range(1, len(self.df.columns) + 1)])))
        for i in range(1, len(self.df.columns) + 1):
            self.tree.heading('#' + str(i), text=self.df.columns[i - 1])

        # Инициализация виджетов
        self.scroll1 = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scroll1.set)
        self.but1 = tk.Button(self, bg='#00FFEF', activebackground='#00FFEF', text='Удалить игрока',
                              font='TimesNewRoman 16', command=self.delete_element)
        self.but2 = tk.Button(self, bg='#00FFEF', activebackground='#00FFEF', text='Отсортировать',
                              font='TimesNewRoman 16', command=self.sorting)
        self.combo1 = ttk.Combobox(self, width=13, font='TimeNewRoman 16',
                                   values=['index', 'Age', 'Value', 'Wage', 'Crossing', 'Finishing'])
        self.combo1.current(0)  # Задаем по умолчанию 0 индекс из списка value значений combo1
        self.more_many_var = tk.BooleanVar()
        self.rad1 = tk.Radiobutton(self, bg='#00FFB3', activebackground='#00FFB3', text='По возрастанию',
                                   font='TimesNewRoman 14',
                                   variable=self.more_many_var,
                                   value=True)
        self.rad1.select()
        self.rad2 = tk.Radiobutton(self, bg='#00FFB3', activebackground='#00FFB3', text='По убыванию',
                                   font='TimesNewRoman 14',
                                   variable=self.more_many_var,
                                   value=False)
        self.but3 = tk.Button(self, bg='#00FFEF', activebackground='#00FFEF', font='TimeNewRoman 16',
                              text='Добавить игрока', command=self.add_member)
        self.ent1 = tk.Entry(self, font='TimesNewRoman 16')
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Сохранить в базу данных', command=self.save_sql)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выйти', command=self.destroy_quit)
        self.menu.add_cascade(label='Меню', menu=self.file_menu)
        self.ent2 = tk.Entry(self)
        self.text1 = tk.Text(self, width=20, height=7)
        self.lab2 = tk.Label(text='Введите sql запрос', bg='#00FFB3', font='TimesNewRoman 14')
        self.but4 = tk.Button(text='Выполнить sql запрос', activebackground='#00FFEF', bg='#00FFEF',
                              font='TimeNewRoman 16', command=self.enter_sql, height=2)
        self.ent3 = tk.Entry(self)
        self.but5 = tk.Button(text='Найти', activebackground='#00FFEF', bg='#00FFEF', command=self.search)
        self.but6 = tk.Button(text='Вернуться', activebackground='#00FFEF', bg='#00FFEF', command=self.default)
        self.combo2 = ttk.Combobox(self, font='TimesNewRoman 16',
                                   values=['Age', 'Nationality', 'Club', 'Value', 'Wage', 'Crossing', 'Finishing'])
        self.but7 = tk.Button(text='Наглядное количественное\nотображение данных', activebackground='#00FFEF',
                              bg='#00FFEF', font='TimesNewRoman 16', command=self.show_relation)
        self.but8 = tk.Button(text='Первый элемент', activebackground='#00FFEF', bg='#00FFEF', font='TimesNewRoman 16',
                              command=self.set_focus)
        self.but9 = tk.Button(text='Последний элемент', activebackground='#00FFEF', bg='#00FFEF',
                              font='TimesNewRoman 16', command=self.set_focus_last)

        # Заполнение дерева элементами из базы данных sql
        for i in range(len(self.df)):
            self.tree.insert('', tk.END, values=list(self.df.iloc[i]))

        self.tree.bind('<<TreeviewSelect>>', self.select_value)

    def put_widgets(self):
        # Размещение виджетов на окне
        self.tree.grid(row=0, column=0, columnspan=10, padx=20, pady=10, stick='')
        self.scroll1.grid(row=0, column=11, stick='ns', pady=10)
        self.but1.grid(row=1, column=0, stick='wens')
        self.but2.grid(row=1, column=1, stick='wens', padx=7)
        self.combo1.grid(row=2, column=1, padx=7)
        self.rad1.grid(row=3, column=1, stick='w', padx=7)
        self.rad2.grid(row=4, column=1, stick='wn', padx=7)
        self.but3.grid(row=1, column=5, stick='wens')
        self.ent1.grid(row=1, column=4, stick='wens', padx=8)
        self.text1.grid(row=3, column=4, stick='wens', rowspan=3, padx=8)
        self.lab2.grid(row=2, column=4, stick='ws', padx=8)
        self.but4.grid(row=3, column=5, stick='wne')
        self.ent3.grid(row=6, column=6, stick='e')
        self.but5.grid(row=6, column=7, stick='w', padx=5)
        self.but6.grid(row=6, column=7)
        self.combo2.grid(row=1, column=7, stick='n')
        self.but7.grid(row=1, column=8, stick='ns')
        self.but8.grid(row=2, column=0, stick='wens', pady=10)
        self.but9.grid(row=3, column=0, stick='we')

    def set_focus_last(self):
        self.tree.selection_set(self.tree.get_children()[-1])
        self.scroll1.set(0.99000999000999, 1.0)

    def set_focus(self):
        self.tree.selection_set(self.tree.get_children()[0])
        self.scroll1.set(0.0, 0.0)

    def show_relation(self):
        if not self.combo2.get():
            messagebox.showerror('Ошибка', 'Позиция не выбрана')
            return
        sns.set()
        sns.displot(df[self.combo2.get()])
        plt.show()

    def default(self):
        self.clear_database()
        for i in range(len(self.df)):
            self.tree.insert('', tk.END, value=list(self.df.iloc[i]))

    def search(self):
        self.local_df = df[df['Name'] == self.ent3.get()]
        self.ent3.delete(0, tk.END)
        if not len(self.local_df):
            messagebox.showinfo('Attention', 'Игрок не найден')
            return
        self.clear_database()
        for i in range(len(self.local_df)):
            self.tree.insert('', tk.END, values=list(self.local_df.iloc[i]))

    def enter_sql(self):
        if self.text1.get(1.0, tk.END) == '\n':
            messagebox.showinfo('Внимание', 'Поле для sql запроса пустое')
        else:
            if messagebox.askquestion('Подтверждение', 'Выполнить sql запрос?') == 'yes':
                try:
                    with sq.connect('database.db') as con:
                        print(pd.read_sql(self.text1.get(1.0, tk.END), con))
                except BaseException:
                    messagebox.showerror('Ошибка', 'Неверный sql запрос')

    def destroy_quit(self):
        answer = messagebox.askyesno('Question', 'Сохранить изменения в базу данных?')
        if answer:
            self.save_sql()
        self.destroy()

    def save_sql(self):
        with sq.connect('database.db') as con:
            con.execute('DROP TABLE IF EXISTS footballers_changes')
            self.df.to_sql('footballers_changes', con, index=False)

    def add_member(self):
        if not self.ent1.get():
            messagebox.showerror('Ошибка', 'Введите данные')
            return
        elif len(self.ent1.get().split(',')) != 8:
            messagebox.showwarning('Внимание', 'Введите 8 данных через запятую')
            return
        self.df.loc[len(self.df)] = [len(self.df), *[int(i.strip()) if i.isdigit() else i.strip() for i in
                                                     self.ent1.get().split(',')]]
        self.ent1.delete(0, 'end')
        self.clear_database()
        for i in range(len(self.df)):
            self.tree.insert('', tk.END, values=list(self.df.iloc[i]))

    # Очищает дерево
    def clear_database(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def sorting(self):
        self.df.sort_values(self.combo1.get(), inplace=True, ascending=self.more_many_var.get())
        self.clear_database()
        for i in range(len(self.df)):
            self.tree.insert('', tk.END, values=list(self.df.iloc[i]))

    def delete_element(self):
        try:
            self.df.drop(self.value, inplace=True)  # удаляет выбранный в дереве элемент из датафрейма
            self.clear_database()
            for i in range(len(self.df)):
                self.tree.insert('', tk.END, values=list(self.df.iloc[i]))
        except (AttributeError, KeyError):
            messagebox.showinfo('Attention', 'Выберите индекс для удаления!')
            for i in range(len(self.df)):
                self.tree.insert('', tk.END, values=list(self.df.iloc[i]))

    def select_value(self, event):
        for i in self.tree.selection():
            self.value = self.tree.item(i)['values'][0]


with sq.connect('database.db') as con:
    cur = con.cursor()
    df = pd.read_sql('SELECT "index", Name, Age, Nationality, Club, Value, Wage, Crossing, Finishing  FROM footballers',
                     con).iloc[:1001]

root = App(df)
root.put_widgets()
root.mainloop()

