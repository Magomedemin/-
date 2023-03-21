from tkinter import *
from tkinter import messagebox
import psycopg2

######## PSQL
conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
cursor = conn.cursor()
# создание таблицы телефонов
createPhone = """
CREATE TABLE IF NOT EXISTS phone(
    id serial NOT NULL,
    phone_name VARCHAR(100) NOT NULL,
    memory VARCHAR(20) NOT NULL,
    op_memory VARCHAR(20) NOT NULL,
    processor VARCHAR(100) NOT NULL
);"""
# создание таблицы ролей
createRoles = """
CREATE TABLE IF NOT EXISTS roles (
    id serial PRIMARY KEY NOT NULL,
    system_role VARCHAR(35) NOT NULL
    );"""
# создание таблицы пользователей
createUsers = """
CREATE TABLE IF NOT EXISTS users (
    id serial NOT NULL,
    surname VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50) NOT NULL,
    login VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    roles_id int DEFAULT 2,
    FOREIGN KEY (roles_id) REFERENCES roles (id),
    is_deleted boolean DEFAULT FALSE
    );"""
# добавление ролей
insertRole = """
INSERT INTO roles (system_role) VALUES
('Администратор'),
('Посетитель магазина');
"""

cursor.execute(createPhone)
cursor.execute(createRoles)
cursor.execute(createUsers)
cursor.execute(insertRole)
conn.commit()
conn.close()


def login_window():
    login_win = Toplevel(root)
    login_win.title('Окно авторизации')
    login_win.geometry('250x160+200+200')

    login_frame = Frame(login_win)
    login_frame.pack(pady=10)

    login_label = Label(login_frame, text="Введите логин и пароль")
    login_label.grid(row=1, columnspan=2, pady=10)

    login_entry = Entry(login_frame)
    login_entry.grid(row=2, column=0, padx=5, pady=5)

    password_entry = Entry(login_frame, show="*")
    password_entry.grid(row=3, column=0, padx=5, pady=5)

    btn_login = Button(login_frame, text="Войти", command=lambda: login(login_entry.get(), password_entry.get()))
    btn_login.grid(row=2, column=1, padx=5, pady=5)

    btn_cancel = Button(login_frame, text="Отмена", command=login_win.destroy)
    btn_cancel.grid(row=3, column=1, padx=5, pady=5)

    def login(login, password):
        if not (login and password):
            messagebox.showerror(title='Ошибка', message='Заполните все поля')
        else:
            conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
            cur = conn.cursor()
            try:
                cur.execute('SELECT * FROM users WHERE login=%s AND password=%s AND is_deleted = false', (login, password))
                user = cur.fetchone()
                if user:
                    if user is not None:
                        if user[6] == 1:
                            login_win.destroy()
                            admin_window(user)
                        elif user[6] == 2:
                            login_win.destroy()
                            visitor_window(user)
                else:
                    messagebox.showerror(title='Ошибка', message='Ошибка в логине или пароле')


                cur.close()
                conn.close()
            except Exception:
                print('Ошибка авторизации')

def delete_user(login):
    conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
    cur = conn.cursor()
    try:
        cur.execute(f"UPDATE users SET is_deleted = true WHERE login='{login}';")
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo(title='Информация', message='Аккаунт удален.\nПрограмма будет закрыта.')
        root.destroy()
    except Exception:
        print('Ошибка удаления аккаунта')

def admin_window(user):
    admin_win = Toplevel(root)
    admin_win.grab_set()
    admin_win.title("Окно администратора")

    admin_frame = LabelFrame(admin_win, text='Информация о пользователе', pady=5, padx=5)
    admin_frame.pack(side=TOP, fill=X)
    # логин активного пользователя
    login_label = Label(admin_frame, text=f"Вы вошли как - {user[4]}", font=('Calibri', 12))
    login_label.pack(side=LEFT)
    # кнопка удалить аккаунт
    btn_delete = Button(admin_frame, text="Удалить аккаунт", font=('Calibri', 11), command=lambda: delete_user(user[4]))
    btn_delete.pack(side=RIGHT)

    # фрейм добавления телефона
    add_phone_frame = LabelFrame(admin_win, text='Добавление телефона')
    add_phone_frame.pack(side=TOP, fill=X, pady=10)
    # название телефона
    l_ph_name = Label(add_phone_frame, text='Модель')
    l_ph_name.grid(row=1, column=0, padx=5, pady=10)
    e_ph_name = Entry(add_phone_frame)
    e_ph_name.grid(row=1, column=1, padx=5, pady=10)
    # память телефона
    l_memory = Label(add_phone_frame, text='Размер памяти')
    l_memory.grid(row=1, column=2, padx=5, pady=10)
    e_memory = Entry(add_phone_frame)
    e_memory.grid(row=1, column=3, padx=5, pady=10)
    # оперативная память
    l_op_memory = Label(add_phone_frame, text='Оперативная память')
    l_op_memory.grid(row=1, column=4, padx=5, pady=10)
    e_op_memory = Entry(add_phone_frame)
    e_op_memory.grid(row=1, column=5, padx=5, pady=10)
    # процессор
    l_processor = Label(add_phone_frame, text='Процессор')
    l_processor.grid(row=1, column=6, padx=5, pady=10)
    e_processor = Entry(add_phone_frame)
    e_processor.grid(row=1, column=7, padx=5, pady=10)
    # кнопка добавить телефон
    b_add_phone = Button(add_phone_frame, text='Добавить', command=lambda: insertPhone())
    b_add_phone.grid(row=2, column=0, pady=10, padx=2)


    # изменить роль пользователя
    change_role_frame = LabelFrame(admin_win, text='Редактирование роли пользователя (1 - Admin, 2 - User)')
    change_role_frame.pack(side=BOTTOM, fill=X, pady=10)
    l_user_id = Label(change_role_frame, text='Введите ID пользователя')
    l_user_id.pack(side=LEFT, padx=7)
    e_user_id = Entry(change_role_frame)
    e_user_id.pack(side=LEFT, padx=7)
    l_new_role = Label(change_role_frame, text='и ID новой роли')
    l_new_role.pack(side=LEFT, padx=7)
    e_new_role = Entry(change_role_frame)
    e_new_role.pack(side=LEFT, padx=7)
    b_change_role = Button(change_role_frame, text='Изменить роль', command=lambda: changeRole())
    b_change_role.pack(side=LEFT, pady=7, padx=20)

    # удаление телефона
    delete_phone_frame = LabelFrame(admin_win, text='Удаление телефона')
    delete_phone_frame.pack(side=BOTTOM, fill=X, pady=35)
    l_phone_id = Label(delete_phone_frame, text='Удалить телефон с ID')
    l_phone_id.pack(side=LEFT, padx=7)
    e_phone_id = Entry(delete_phone_frame)
    e_phone_id.pack(side=LEFT)
    b_delete_phone = Button(delete_phone_frame, text='Удалить телефон', command=lambda: deletePhone())
    b_delete_phone.pack(side=LEFT, pady=7, padx=20)


    # список телефонов
    phone_list = LabelFrame(admin_win, text='Список телефонов')
    phone_list.pack(side=LEFT, fill=X, padx=2)
    list_1 = Label(phone_list, height=20, width=64)
    list_1.grid(row=1, column=0)
    b_show_phone = Button(phone_list, text='Показать\Обновить список', command=lambda: showPhone())
    b_show_phone.grid(row=8, column=0)

    # список пользователей
    user_list = LabelFrame(admin_win, text='Список пользователей')
    user_list.pack(side=LEFT, fill=X, padx=1)
    list_2 = Label(user_list, height=20, width=64)
    list_2.grid(row=1, column=0)
    b_show_user = Button(user_list, text='Показать\Обновить список', command=lambda: showUsers())
    b_show_user.grid(row=8, column=0)


    # функция изменения роли
    def changeRole():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        param1 = e_user_id.get()
        param2 = e_new_role.get()
        try:
            cursor.execute('UPDATE users SET roles_id = %s WHERE id = %s', (param2, param1))
            conn.commit()
            messagebox.showinfo(title='Информация', message='Роль изменена')
        except Exception:
            print('Ошибка изменения роли')
            conn.rollback()
        conn.close()

    # функция удаления телефона по номеру ИД
    def deletePhone():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM phone WHERE id = ' + e_phone_id.get())
            conn.commit()
            messagebox.showinfo(title='Информация', message='Телефон удален')
        except Exception:
            print('Ошибка удаления телефона')
            conn.rollback()
        conn.close()

    # добавить телефон
    def insertPhone():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO phone (phone_name, memory, op_memory, processor) VALUES (%s, %s, %s, %s)""",
                           (e_ph_name.get(), e_memory.get(), e_op_memory.get(), e_processor.get()))
            conn.commit()
            messagebox.showinfo(title='Информация', message='Телефон добавлен')
        except Exception:
            print('Ошибка добавления телефона')
            conn.rollback()
        conn.close()

    # показать список телефонов
    def showPhone():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM phone')
            records = cursor.fetchall()
            output = ''

            for record in records:
                list_1.config(text=f'{output} \n {record[0]} - {record[1]}, {record[2]}, {record[3]}, {record[4]}')
                output = list_1['text']
        except Exception:
            print('Ошибка формирования списка')
            conn.rollback()
        conn.close()

    # показать список пользователей
    def showUsers():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users')
            records = cursor.fetchall()
            output = ''

            for record in records:
                list_2.config(text=f'{output} \n ID: {record[0]} - ФИО: {record[1]} {record[2]} {record[3]}.\n '
                                   f'Логин: {record[4]}. Пароль: {record[5]}.\n Роль в системе: {record[6]}.'
                                   f'Логическое удаление: {record[7]}')
                output = list_2['text']
        except Exception:
            print('Ошибка формирования списка')
            conn.rollback()
        conn.close()

def visitor_window(user):
    visitor_win = Toplevel(root)
    visitor_win.title("Окно пользователя")
    visitor_win.geometry('600x400+200+200')
    # инфо о пользователе
    visitor_frame = LabelFrame(visitor_win, text='Информация о пользователе', pady=5, padx=5)
    visitor_frame.pack(side=TOP, fill=X)
    # логин активного пользователя
    login_label = Label(visitor_frame, text=f"Вы вошли как - {user[4]}", font=('Calibri', 12))
    login_label.pack(side=LEFT)
    # кнопка удалить аккаунт
    btn_delete = Button(visitor_frame, text="Удалить аккаунт", font=('Calibri', 11), command=lambda: delete_user(user[4]))
    btn_delete.pack(side=RIGHT)

    # список телефонов
    phone_list = LabelFrame(visitor_win, text='Список телефонов')
    phone_list.pack(side=TOP, fill=X)
    list_1 = Label(phone_list, height=18, width=63)
    list_1.pack()
    b_show_phone = Button(phone_list, text='Показать\Обновить список', command=lambda: showPhone())
    b_show_phone.pack(side=BOTTOM)

    def showPhone():
        conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost', port='5432')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM phone')
            records = cursor.fetchall()
            output = ''

            for record in records:
                list_1.config(text=f'{output} \n {record[0]} - {record[1]}, {record[2]}, {record[3]}, {record[4]}')
                output = list_1['text']
        except Exception:
            print('Ошибка формирования списка')
            conn.rollback()
        conn.close()

def reg_window():
    reg_win = Toplevel(root)
    reg_win.title("Регистрация")
    reg_win.geometry('400x320+200+200')
    reg_win.grab_set()

    reg_frame = Frame(reg_win)
    reg_frame.pack(pady=10)

    label = Label(reg_frame, text="Заполните все поля для регистрации")
    label.pack()

    l_surname = Label(reg_frame, text='Фамилия:').pack()
    e_surname = Entry(reg_frame)
    e_surname.pack()
    l_name = Label(reg_frame, text='Имя:').pack()
    e_name = Entry(reg_frame)
    e_name.pack()
    l_patronymic = Label(reg_frame, text='Отчество:').pack()
    e_patronymic = Entry(reg_frame)
    e_patronymic.pack()
    l_log = Label(reg_frame, text='Логин:').pack()
    e_log = Entry(reg_frame)
    e_log.pack()
    l_regpass = Label(reg_frame, text='Пароль:').pack()
    e_regpass = Entry(reg_frame)
    e_regpass.pack()

    btn_register = Button(reg_frame, text="Зарегистрироваться",
                          command=lambda: registration(e_surname.get(), e_name.get(), e_patronymic.get(),
                                                       e_log.get(), e_regpass.get()))
    btn_register.pack(pady=15)

    btn_cancel = Button(reg_frame, text="Отмена", command=reg_win.destroy)
    btn_cancel.pack()

    def registration(surname, name, patronymic, login, password):
        surname = e_surname.get()
        name = e_name.get()
        patronymic = e_patronymic.get()
        login = e_log.get()
        password = e_regpass.get()
        if not (surname and name and patronymic and login and password):
            messagebox.showerror(title='Ошибка', message='Заполните все поля')
            return False
        else:
            conn = psycopg2.connect(database='postgres', user='postgres', password='0712', host='localhost',
                                    port='5432')
            cursor = conn.cursor()
            try:
                cursor.execute("""INSERT INTO users (surname, name, patronymic, login, password) 
                VALUES (%s, %s, %s, %s, %s)""", (surname, name, patronymic, login, password))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo(title='Информация', message='Успешная регистрация')
                reg_win.destroy()
                return True
            except Exception:
                print('Ошибка регистрации')
                return False


root = Tk()
root.title('Промежуточная аттестация. Модуль 2.')
root.geometry('400x320+200+200')

button_1 = Button(text='Авторизоваться', bg='#333', fg='#eee', font='18', activebackground='#070',
                     activeforeground='#006', state='normal', command=login_window).pack(pady=15)

button_2 = Button(text='Зарегистрироваться', bg='#333', fg='#eee', font='18', activebackground='#070',
                     activeforeground='#006', state='normal', command=reg_window).pack(pady=20)

quitButton = Button(text='Выход', bg='#333', fg='#eee', font='18', command=root.destroy).pack(pady=40)


root.mainloop()