# -*- encoding: utf-8 -*-
import sqlite3
import xml.etree.ElementTree as ET

'''
Перекинуть все функции работы с таблицами в начало в def и, желательно, закинуть на git
'''


def database_connect():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print('База данных подключена')
        sqlite_select_query = 'SELECT sqlite_version();'
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print(f'Версия базы данных - {record}')
        return cursor, sqlite_connection
    except sqlite3.Error as error:
        print(f'Ошибка при подключении к БД - {error}')
        return None


def database_disconnect(sqlite_connection):
    if sqlite_connection:
        sqlite_connection.close()
        print('Подлючение к БД закрыто')
    else:
        print('Возникла какая-то ошибка')


# Запись в xml файл
def to_xml():
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()

    # Вытаскивание информации из таблиц (название столбцов таблиц   и содержимое)
    cursor.execute('SELECT * FROM [Налоги]')
    data1 = cursor.fetchall()
    data2 = cursor.description
    cursor.execute('SELECT * FROM [Работники]')
    data3 = cursor.fetchall()
    data4 = cursor.description
    cursor.execute('SELECT * FROM [Отделы]')
    data5 = cursor.fetchall()
    data6 = cursor.description
    tables = ET.Element('Таблицы')
    dues = ET.SubElement(tables, 'Налоги')
    workers = ET.SubElement(tables, 'Работники')
    departments = ET.SubElement(tables, 'Отделы')
    dues_columns = []
    workers_columns = []
    departments_columns = []

    # Создание списка с названиями столбцов таблиц
    for i in data2:
        dues_columns.append(i[0])
    for i in data4:
        workers_columns.append(i[0])
    for i in data6:
        departments_columns.append(i[0])

    # Заполнение xml файла в одну строку всеми таблицами
    for i in data1:
        item = ET.SubElement(dues, 'Налог')
        item.set("id", str(i[0]))
        for el in range(1, len(i)):
            value = ET.SubElement(item, f'{dues_columns[el]}')
            value.text = str(i[el])
    for i in data3:
        for el in range(len(i)):
            value = ET.SubElement(workers, f'{workers_columns[el]}')
            value.text = str(i[el])
    for i in data5:
        for el in range(len(i)):
            value = ET.SubElement(departments, f'{departments_columns[el]}')
            value.text = str(i[el])

    sqlite_connection.close()

    # my_data = ET.tostring(dues)
    # myfile = open('items.xml', 'w', encoding='UTF-8')
    # myfile.write(str(my_data))
    # myfile.close()
    ET.ElementTree(tables).write('items.xml', encoding='UTF-8')


# Удаление записи из таблицы "Налоги"
def delete_from_dues(number_of_due):
    sqlite_query = f'DELETE FROM [Налоги] WHERE [ID] = "{number_of_due}"'
    return sqlite_query


# Поиск в таблице "Работники"
def search_in_workers(query):
    sqlite_select_query = 'SELECT * FROM [Работники]' \
                         f'WHERE (([ФИО] LIKE "%{query}%") OR ([Номер отдела] LIKE "%{query}%"))'
    return sqlite_select_query


# Поиск в таблице "Отделы"
def search_in_departments(query):
    sqlite_select_query = 'SELECT * FROM [Отделы]' \
                          f'WHERE (([Номер отдела] LIKE "%{query}%") OR ([Название отдела] LIKE "%{query}%"))'
    return sqlite_select_query


# Поиск в таблице "Налог"
def search_in_dues(query):
    sqlite_select_query = 'SELECT * FROM [Налоги]' \
                         f'WHERE ((ID LIKE "%{query}%") OR (ФИО LIKE "%{query}%") OR (Месяц LIKE "%{query}%") OR ([Зарплата (руб.)] LIKE "%{query}%") OR ([Налог (руб.)] LIKE "%{query}%"))'
    return sqlite_select_query


# Создание записи в таблице "Работники"
def insert_to_workers(name: str, number_of_department: int):
    sqlite_query: str = f'INSERT INTO [Работники] ("ФИО", "Номер отдела")' \
                        f'VALUES ("{name}", "{number_of_department}")'
    return sqlite_query


# Создание записи в таблице "Отделы"
def insert_to_departments(number_of_department: int, name_of_department: str):
    sqlite_query: str = f'INSERT INTO [Отделы] ("Номер отдела", "Название отдела")' \
                        f'VALUES ("{number_of_department}", "{name_of_department}")'
    return sqlite_query


# Создание записи в таблице "Налоги"
def insert_to_dues(name: str, month: str, salary: int):
    sqlite_query: str = f'INSERT INTO [Налоги] ("ФИО", "Месяц", [Зарплата (руб.)])' \
                        f'VALUES ("{name}", "{month}", "{salary}")'
    return sqlite_query

#
def work_with_current_dues(cursor, department):

    sqlite_query = f'SELECT * FROM [Налоги] WHERE ()'


# Функция активирующая скрипт работы с таблицей "Налоги"
def work_with_dues(cursor):
    print('Таблица "Налоги": ')
    sqlite_query = 'SELECT * FROM [Налоги]'
    cursor.execute(sqlite_query)
    record = cursor.description
    for i in record:
        print(i[0], end='  |  ')
    print('')
    sqlite_query = 'SELECT * FROM [Налоги]'
    cursor.execute(sqlite_query)
    record = cursor.fetchall()
    for i in record:
        print(i)
    print()

    print('Возможные действия: ')
    print('1 - Поиск в таблице\n'
          '2 - Удалить запись из таблицы\n'
          '3 - Добавить запись в таблицу\n'
          '4 - Изменить запись\n'
          '5 - Перейти в таблицу Работники\n'
          '6 - Перейти в таблицу Отделы\n'
          '0 - Переход в Меню')
    select = int(input('Введите номер действия: '))

    if select == 1:
        try:
            search_line = str(input('Введите запрос: '))
            sqlite_select_query = search_in_dues(search_line)
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            if len(record) != 0:
                print('Результаты запроса: ')
                for i in record:
                    print(i)
            else:
                print('По вашему запросу ничего не найдено')
            print()
            work_with_dues(cursor)

        except Exception as excp:
            print(f'Поиск не был завершен из-за ошибки - {excp}')
            print()
            work_with_dues(cursor)

    elif select == 2:
        try:
            id = int(input('Введите ID записи, которую хотите удалить: '))
            sqlite_query = delete_from_dues(id)
            cursor.execute(sqlite_query)

        except Exception as excp:
            print(f'Не удалось удалить из-за ошибки - {excp}')
            print()
            work_with_dues(cursor)

        else:
            print('Запись успешно удалена')
            print()
            work_with_dues(cursor)

    elif select == 3:
        try:
            name = str(input('Введите ФИО сотрудника: '))
            month = str(input('Введите месяц: '))
            salary = float(input('Введите зарплату сотрудника: '))
            sqlite_insert_query = insert_to_dues(name, month, salary)
            cursor.execute(sqlite_insert_query)
        except Exception as excp:
            print(f'Не удалось добавить запись из-за ошибки - {excp}')
            print()
            work_with_dues(cursor)

        else:
            print('Запись успешно добавлена')
            print()
            work_with_dues(cursor)

    elif select == 4:
        try:
            id = int(input('Введите ID записи, которую хотите изменить: '))
            sqlite_query = f'SELECT * FROM [Налоги] WHERE [ID] = {id}'
            cursor.execute(sqlite_query)
            for i in cursor.description:
                print(i[0], end=' | ')
            print()
            row = cursor.fetchall()
            print(row)
            print('Какой поле вы хотите изменить?\n'
                               '1 - ФИО\n'
                               '2 - Месяц\n'
                               '3 - Зарплата (руб.)\n'
                               '4 - Все')
            column = int(input('Введите команду: '))
            if column == 1:
                try:
                    name = str(input('На какое ФИО вы хотели бы изменить (0 для отмены)? '))
                    if name == str(0):
                        pass
                    else:
                        sqlite_query = f'UPDATE [Налоги] SET [ФИО] = "{name}" WHERE [ID] = {id}'
                        cursor.execute(sqlite_query)

                except Exception as excp:
                    print(f'Запись не удалось изменить из-за ошибки - {excp}')
                    print()
                    work_with_dues(cursor)

                else:
                    if name == str(0):
                        print('Действие отменено')
                    else:
                        print('Запись успешно изменена')
                    print()
                    work_with_dues(cursor)

            elif column == 2:
                try:
                    month = str(input('На какой месяц вы хотели бы сменить (0 для отмены)? '))
                    if month == str(0):
                        pass
                    else:
                        sqlite_query = f'UPDATE [Налоги] SET [Месяц] = "{month}" WHERE [ID] = {id}'
                        cursor.execute(sqlite_query)

                except Exception as excp:
                    print(f'Запись не удалось изменить из-за ошибки - {excp}')
                    print()
                    work_with_dues(cursor)

                else:
                    if month == str(0):
                        print('Отмена действия')
                    else:
                        print('Запись успешно изменена')
                    print()
                    work_with_dues(cursor)

            elif column == 3:
                try:
                    salary = float(input('На какую зарплату вы хотели бы сменить (0 для отмены)? '))
                    if salary == float(0):
                        pass
                    else:
                        sqlite_query = f'UPDATE [Налоги] SET [Зарплата (руб.)] = {salary} WHERE [ID] = {id}'
                        cursor.execute(sqlite_query)
                except Exception as excp:
                    print(f'Запись не удалось изменить из-за ошибки - {excp}')
                    print()
                    work_with_dues(cursor)

                else:
                    if salary == float(0):
                        print('Отмена действия')
                    else:
                        print('Запись успешно изменена')
                    print()
                    work_with_dues(cursor)

            elif column == 4:
                try:
                    name = str(input('На какое ФИО вы хотели бы изменить (0 для отмены)? '))
                    month = str(input('На какой месяц вы хотели бы сменить? '))
                    salary = float(input('На какую зарплату вы хотели бы сменить? '))
                    if name != str(0):
                        sqlite_query = f'UPDATE [Налоги] SET [Месяц] = "{month}", [ФИО] = "{name}", [Зарплата (руб.)] = {salary} WHERE [ID] = {id}'
                        cursor.execute(sqlite_query)
                    else:
                        pass

                except Exception as excp:
                    print(f'Запись не удалось изменить из-за ошибки - {excp}')
                    print()
                    work_with_dues(cursor)

                else:
                    if name != str(0):
                        print('Запись успешно изменена')
                    else:
                        print('Отмена действия')
                    print()
                    work_with_dues(cursor)

        except Exception as excp:
            print(f'Не удалось изменить запись из-за ошибки - {excp}')
            print()
            work_with_dues(cursor)

    elif select == 5:
        print()
        work_with_workers(cursor)

    elif select == 6:
        print()
        work_with_departments(cursor)

    elif select == 0:
        print('Переход в Меню')
        print()

    else:
        print('Введена неверная команда')
        print()
        work_with_dues(cursor)


# Функция активирующая скрипт работы с таблицей "Работники"
def work_with_workers(cursor):
    print('Таблица "Работники": ')
    sqlite_query = 'SELECT * FROM [Работники]'
    cursor.execute(sqlite_query)
    record = cursor.description
    for i in record:
        print(i[0], end='  |  ')
    print('')
    sqlite_query = 'SELECT * FROM [Работники]'
    cursor.execute(sqlite_query)
    record = cursor.fetchall()
    for i in record:
        print(i)
    print()

    print('Возможные действия: ')
    print('1 - Поиск в таблице\n'
          '2 - Изменить запись в таблице\n'
          '3 - Добавить запись в таблице\n'
          '4 - Перейти в таблицу Налоги\n'
          '5 - Перейти в таблицу Отделы\n'
          '0 - Перейти в Меню')
    select = int(input('Введите номер действия: '))
    if select == 1:
        try:
            search_line = str(input('Введите запрос: '))
            sqlite_select_query = search_in_workers(search_line)
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            if len(record) > 0:
                print('Результаты запроса:')
                for i in record:
                    print(i)
            else:
                print('По вашему запросу ничего не найдено')
            print()
            work_with_workers(cursor)

        except Exception as excp:
            print(f'Поиск не был завершен из-за ошибки - {excp}')
            print()
            work_with_workers(cursor)

    elif select == 2:
        try:
            print('Какой столбец вы бы хотели изменить?\n'
                  '1 - ФИО\n'
                  '2 - Номер отдела')
            column = int(input('Введите номер команды: '))

            if column == 1:
                name = str(input('Введите ФИО работника, которое хотите изменить: '))
                sqlite_query = f'SELECT * FROM [Работники] WHERE [ФИО] = "{name}"'
                cursor.execute(sqlite_query)
                for i in cursor.description:
                    print(i[0], end=' | ')
                print()
                print(cursor.fetchall())
                request = str(input('Введите ФИО на которое хотели бы изменить: '))
                sqlite_query = f'UPDATE [Работники] SET [ФИО] = "{request}" WHERE [ФИО] = "{name}"'
                cursor.execute(sqlite_query)

            elif column == 2:
                name = str(input('Введите ФИО работника, которое хотите изменить: '))
                sqlite_query = f'SELECT * FROM [Работники] WHERE [ФИО] = "{name}"'
                cursor.execute(sqlite_query)
                for i in cursor.description:
                    print(i[0], end=' | ')
                print()
                print(cursor.fetchall())
                request = int(input('Введите номер отдела, на который хотели бы изменить: '))
                sqlite_query = f'UPDATE [Работники] SET [Номер отдела] = {request} WHERE [ФИО] = "{name}"'
                cursor.execute(sqlite_query)

            else:
                print('Введена неверная команда')

        except Exception as excp:
            print(f'Запись не удалось изменить из-за ошибки - {excp}')
            print()
            work_with_workers(cursor)

        else:
            if column not in [1, 2]:
                print('Запись не была изменена')
            else:
                print('Запись успешно изменена')
            print()
            work_with_workers(cursor)

    elif select == 3:
        try:
            name = str(input('Введите ФИО: '))
            number_of_department = int(input('Введите номер отдела: '))
            sqlite_query = insert_to_workers(name, number_of_department)
            cursor.execute(sqlite_query)

        except Exception as excp:
            print(f'Запись не была добавлена из-за ошибки - {excp}')
            print()
            work_with_workers(cursor)

        else:
            print('Запись успешно добавлена')
            print()
            work_with_workers(cursor)

    elif select == 4:
        print()
        work_with_dues(cursor)

    elif select == 5:
        print()
        work_with_departments(cursor)

    elif select == 0:
        print()
        print('Переход в Меню')
        print()

    else:
        print('Введена неверная команда')
        print()
        work_with_workers(cursor)


# Функция активирующая скрипт работы с таблицей "Отделы"
def work_with_departments(cursor):
    print('Таблица "Отделы": ')
    sqlite_query = 'SELECT * FROM [Отделы]'
    cursor.execute(sqlite_query)
    record = cursor.description
    for i in record:
        print(i[0], end='  |  ')
    print('')
    sqlite_query = 'SELECT * FROM [Отделы]'
    cursor.execute(sqlite_query)
    record = cursor.fetchall()
    for i in record:
        print(i)
    print()

    print('Возможные действия: ')
    print('1 - Поиск в таблице\n'
          '2 - Изменить запись в таблице\n'
          '3 - Добавить запись в таблице\n'
          '4 - Перейти в таблицу Налоги\n'
          '5 - Перейти в таблицу Работники\n'
          '0 - Переход в Меню')
    select = int(input('Введите номер действия: '))
    if select == 1:
        try:
            search_line = str(input('Введите запрос: '))
            sqlite_select_query = search_in_departments(search_line)
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            if len(record) != 0:
                print('Результаты запросы: ')
                for i in record:
                    print(i)
            else:
                print('По вашему запросу ничего не найдено')
            print()
            work_with_departments(cursor)

        except Exception as excp:
            print(f'Поиск не был завершен из-за ошибки - {excp}')
            print()
            work_with_departments(cursor)

    elif select == 2:
        try:
            print('Какой столбец хотите изменить?\n'
                  '1 - Номер отдела\n'
                  '2 - Название отдела')
            column = int(input('Введите команду: '))
            if column == 1:
                id = int(input('Введите номер отдела, номер которого хотите изменить: '))
                sqlite_query = f'SELECT  * FROM [Отделы] WHERE [Номер отдела] = {id}'
                cursor.execute(sqlite_query)
                for i in cursor.description:
                    print(i[0], end=' | ')
                print()
                print(cursor.fetchall())
                request = int(input('Введите номер, на который хотите изменить (0 для отмены): '))
                if request == 0:
                    pass
                else:
                    sqlite_query = f'UPDATE [Отделы] SET [Номер отдела] = {request} WHERE [Номер отдела] = {id}'
                    cursor.execute(sqlite_query)

            elif column == 2:
                id = int(input('Введите номер отдела, название которого хотите изменить (0 для отмены): '))
                sqlite_query = f'SELECT * FROM [Отделы] WHERE [Номер отдела] = {id}'
                cursor.execute(sqlite_query)
                for i in cursor.description:
                    print(i[0], end=' | ')
                print()
                print(cursor.fetchall())
                request = str(input('Введите название, на которое хотели бы изменить (0 для отмены): '))
                if request == 0:
                    pass
                else:
                    sqlite_query = f'UPDATE [Отделы] SET [Название отдела] = "{request}" WHERE [Номер отдела] = {id}'
                    cursor.execute(sqlite_query)

        except Exception as excp:
            print(f'Запись не была изменена из-за ошибки - {excp}')
            print()
            work_with_departments(cursor)

        else:
            if request == 0:
                pass
            else:
                print('Запись успешно изменена')
            print()
            work_with_departments(cursor)

    elif select == 3:
        try:
            number_of_department = int(input('Введите номер отдела: '))
            name_of_department = str(input('Введите название отдела: '))
            sqlite_query = insert_to_departments(number_of_department, name_of_department)
            cursor.execute(sqlite_query)

        except Exception as excp:
            print(f'Запись не была добавлена из-за ошибки - {excp}')
            print()
            work_with_departments(cursor)

        else:
            print('Запись успешно добавлена')
            print()
            work_with_departments(cursor)

    elif select == 4:
        print()
        work_with_dues(cursor)

    elif select == 5:
        print()
        work_with_workers(cursor)

    elif select == 0:
        print('Переход в Меню')
        print()

    else:
        print('Введена неверная команда')
        print()

# Функция начинающая работу программы
def start():
    try:
        cursor, sqlite_connection = database_connect()

        print('Возможные действия:')
        print('1 - Работать с таблицей Налоги\n'
              '2 - Работать с таблицей Работники\n'
              '3 - Работать с таблицей Отделы\n'
              '10 - Выгрузка в xml\n'
              '0 - Закончить работу')
        choice = int(input('Выберите действие: '))
        print()

        if choice == 1:
            work_with_dues(cursor)

        elif choice == 2:
            work_with_workers(cursor)

        elif choice == 3:
            work_with_departments(cursor)

        elif choice == 10:
            try:
                to_xml()
            except Exception as excp:
                print(f'Не удалось сохранить из-за ошибки - {excp}')
            else:
                print('Команда успешно выполнена')
                print()

        elif choice == 0:
            print('Конец работы.')
            return None
        else:
            print('Введено неверное число')

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(f'Ошибка при подключении к БД - {error}')

    finally:
        database_disconnect(sqlite_connection)
        if choice == 0:
            pass
        elif choice in [1, 2, 3, 10]:
            return start()
        else:
            print('Введена неверная команда. Конец работы.')


if __name__ == '__main__':
    print('Добро пожаловать в программу формирования списков Налогов и управления ими.')
    #start()
    cursor, sqlite_connection = database_connect()
    query = 'PRAGMA foreign_keys=ON'
    cursor.execute(query)
    for i in cursor.fetchall():
        print(i)
    database_disconnect(sqlite_connection)

query = '''CREATE TABLE Налоги (
    ID                INTEGER    PRIMARY KEY AUTOINCREMENT,
    ФИО               TEXT       NOT NULL
                                 REFERENCES Работники (ФИО) ON DELETE CASCADE
                                                            ON UPDATE CASCADE DEFERRABLE INITIALLY IMMEDIATE,
    Месяц             TEXT       NOT NULL
                                 CHECK (Месяц = "Январь" OR 
                                        Месяц = "Февраль" OR 
                                        Месяц = "Март" OR 
                                        Месяц = "Апрель" OR 
                                        Месяц = "Май" OR 
                                        Месяц = "Июнь" OR 
                                        Месяц = "Июль" OR 
                                        Месяц = "Август" OR 
                                        Месяц = "Сентябрь" OR 
                                        Месяц = "Октябрь" OR 
                                        Месяц = "Ноябрь" OR 
                                        Месяц = "Декабрь"),
    [Зарплата (руб.)] REAL       NOT NULL
                                 CHECK ("Зарплата (руб.)" > 0),
    [Налог (руб.)]    "[REAL ] " GENERATED ALWAYS AS (CASE WHEN [Зарплата (руб.)] < 9049 THEN ([Зарплата (руб.)] / 10) ELSE ([Зарплата (руб.)] * 13 / 100) END) STORED
)'''
query = '''CREATE TABLE Отделы (
    [Номер отдела]    INTEGER PRIMARY KEY
                              NOT NULL,
    [Название отдела] TEXT    NOT NULL
)'''
query = '''CREATE TABLE Работники (
    ФИО            CHAR    PRIMARY KEY
                           NOT NULL,
    [Номер отдела] INTEGER REFERENCES Отделы ([Номер отдела]) ON DELETE CASCADE
                                                              ON UPDATE CASCADE
                                                              MATCH [FULL] NOT DEFERRABLE INITIALLY IMMEDIATE
)'''