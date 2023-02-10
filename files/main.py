# -*- encoding: utf-8 -*-

from time import sleep
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt, QThread
from des import *
from search_in_workers_window import *
from search_in_departments_window import *
from search_in_dues_window import *
from insert_into_dues import *
from insert_into_workers import *
from insert_into_departments import *
from update_table_dues import *
from update_table_departments import *
from update_table_workers import *
import sqlite3
import xml.etree.ElementTree as ET
from os.path import exists, abspath
from os import remove
import json


# Connect to sqlite database
def database_connect():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        return cursor, sqlite_connection
    except sqlite3.Error as error:
        print(f'Ошибка при подключении к БД - {error}')
        return None


# Disconnect from sqlite database
def database_disconnect(sqlite_connection):
    sqlite_connection.commit()
    if sqlite_connection:
        sqlite_connection.close()
        
    else:
        print('Возникла какая-то ошибка в <<database_disconnect>>\nНе было соединения с БД')


# Creating of database with required tables
def create_database():
    cursor, sqlite_connection = database_connect()

    query = '''CREATE TABLE IF NOT EXISTS Налоги (
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
        [Налог (руб.)]    "[REAL ] " GENERATED ALWAYS AS (CASE WHEN [Зарплата (руб.)] < 9049 
        THEN ([Зарплата (руб.)] / 10) ELSE ([Зарплата (руб.)] * 13 / 100) END) STORED
    )'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS Отделы (
        [Номер отдела]    INTEGER PRIMARY KEY
                                  NOT NULL,
        [Название отдела] TEXT    NOT NULL
    )'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS Работники (
        ФИО            CHAR    PRIMARY KEY
                               NOT NULL,
        [Номер отдела] INTEGER REFERENCES Отделы ([Номер отдела]) ON DELETE CASCADE
                                                                  ON UPDATE CASCADE
                                                                  MATCH [FULL] NOT DEFERRABLE INITIALLY IMMEDIATE
    )'''
    cursor.execute(query)

    cursor.close()
    database_disconnect(sqlite_connection)


# search for database sqlite_python
def search_db():
    try:
        if not exists(abspath('sqlite_python.db')):
             return create_database()
        else:
            pass
    except Exception as excp:
        print(f'Ошибка при поиске БД - {excp}')


# recreate the database
def recreate_db():
    try:
        remove('sqlite_python.db')
        search_db()

    except Exception as excp:
        print(f'Ошибка при пересоздании БД - {excp}')


# convert to json
def to_json():

    def write(data, filename):
        data = json.dumps(data)
        data = json.loads(str(data))
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.close()

    cursor, sqlite_connection = database_connect()
    dues = 'SELECT * FROM [Налоги]'
    cursor.execute(dues)
    dues = cursor.fetchall()
    dues_columns = cursor.description
    workers = 'SELECT * FROM [Работники]'
    cursor.execute(workers)
    workers = cursor.fetchall()
    workers_columns = cursor.description
    departments = 'SELECT * FROM [Отделы]'
    cursor.execute(departments)
    departments = cursor.fetchall()
    departments_columns = cursor.description
    data = {}
    data['Налоги'] = {}
    for row in range(len(dues)):
        data['Налоги'][str(row + 1)] = {}
        for column in range(len(dues_columns)):
            data['Налоги'][str(row + 1)][dues_columns[column][0]] = dues[row][column]
    data['Работники'] = {}
    for row in range(len(workers)):
        data['Работники'][str(row + 1)] = {}
        for column in range(len(workers_columns)):
            data['Работники'][str(row + 1)][workers_columns[column][0]] = workers[row][column]
    data['Отделы'] = {}
    for row in range(len(departments)):
        data['Отделы'][str(row + 1)] = {}
        for column in range(len(departments_columns)):
            data['Отделы'][str(row + 1)][departments_columns[column][0]] = departments[row][column]
    write(data, 'data.json')

    cursor.close()
    database_disconnect(sqlite_connection)


# Запись в xml файл
def to_xml():
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()

    # Вытаскивание информации из таблиц (название столбцов таблиц и содержимое)
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

    ET.ElementTree(tables).write('items.xml', encoding='UTF-8')


class SQLThread(QThread):
    def __init__(self, mainwindow=None, changewindow=None,
                 table=None, action=None, parent=None):
        super().__init__()
        self.mainWindow = mainwindow
        self.changeWindow = changewindow
        self.table = table
        self.action = action

    def run(self):
        try:
            if self.action == 'Добавление':
                if self.table == 'Налоги':
                    cursor, sqlite_connection = database_connect()
                    name = self.mainWindow.insert_into_dues.lineEdit_number.text()
                    month = self.mainWindow.insert_into_dues.lineEdit_number_2.text()
                    salary = self.mainWindow.insert_into_dues.lineEdit_number_3.text()
                    query = f'INSERT INTO [Налоги] ([ФИО], [Месяц], [Зарплата (руб.)]) VALUES ("{name}", "{month}", "{salary}")'
                    cursor.execute(query)
                elif self.table == 'Работники':
                    cursor, sqlite_connection = database_connect()
                    name = self.mainWindow.insert_into_workers.lineEdit_number.text()
                    number_of_department = self.mainWindow.insert_into_workers.lineEdit_number_2.text()
                    query = f'INSERT INTO [Работники] ([ФИО], [Номер отдела]) VALUES ("{name}", "{number_of_department}")'
                    cursor.execute(query)
                elif self.table == 'Отделы':
                    cursor, sqlite_connection = database_connect()
                    number_of_department = self.mainWindow.insert_into_departments.lineEdit_number.text()
                    name = self.mainWindow.insert_into_departments.lineEdit_number_2.text()
                    query = f'INSERT INTO [Отделы] ([Номер отдела], [Название отдела]) ' \
                            f'VALUES ("{number_of_department}", "{name}")'
                    cursor.execute(query)

            elif self.action == 'Удаление':
                if self.table == 'Налоги':

                    cursor, sqlite_connection = database_connect()
                    query = f'DELETE FROM [Налоги] WHERE [ID] = {self.mainWindow.tableWidget.item(self.mainWindow.tableWidget.currentRow(), 0).text()}'
                    cursor.execute(query)

                elif self.table == 'Работники':

                    cursor, sqlite_connection = database_connect()
                    query = f'DELETE FROM [Работники] WHERE [ФИО] = "{self.mainWindow.tableWidget.item(self.mainWindow.tableWidget.currentRow(), 0).text()}"'
                    cursor.execute(query)

                else:

                    cursor, sqlite_connection = database_connect()
                    query = f'DELETE FROM [Отделы] WHERE [Номер отдела] = {self.mainWindow.tableWidget.item(self.mainWindow.tableWidget.currentRow(), 0).text()}'
                    cursor.execute(query)

        except sqlite3.Error as err:
            self.changeWindow.result = err
            if self.action == 'Добавление':
                self.changeWindow.statusbar.showMessage(f'Возникла ошибка - {err}')
            else:
                self.mainWindow.statusbar.showMessage(f'Возникла ошибка - {err}')
        else:
            if self.action == 'Добавление':
                self.changeWindow.result = 'True'
                self.changeWindow.statusbar.showMessage(f'Запись успешно добавлена.')
            else:
                self.mainWindow.statusbar.showMessage(f'Запись успешно изменена.')
        finally:
            if sqlite_connection is not None:
                try:
                    cursor.close()
                    database_disconnect(sqlite_connection)
                except:
                    pass


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_table = ''
        self.last_query = ''
        self.result = None

        # menubar
        # Processing the buttons "Файл" -> "Выгрузка в xml"
        self.ui.action_xml.triggered.connect(self.xml_notification)

        # Processing the button "Файл" -> "Выгрузка в json"
        self.ui.action_json.triggered.connect(self.json_notification)

        # Processing the buttons "О программе" -> "Показать информацию о программе"
        self.ui.action_6.triggered.connect(self.about)

        # Processing the buttons "Файл" -> "Очистить Базу Данных"
        self.ui.action_3.triggered.connect(self.recreate)
        self.ui.action_3.triggered.connect(lambda: self.set_table(self.last_query))

        # Processing the button 'Добавить запись' using function <<insert_into_table>>
        self.ui.pushButton_4.clicked.connect(self.insert_into_table)

        # Processing the button 'Изменить запись' using function <<update_table>>
        self.ui.pushButton_5.clicked.connect(self.update_table)

        # Processing the button 'Удалить запись' using function <<delete_from_table>>
        self.ui.pushButton_6.clicked.connect(self.delete_from_table)

        #  Processing the button 'Показать' using function <<set_table>>
        self.ui.pushButton_3.clicked.connect(lambda: self.set_table(''))

        # **Decorative** Enabled standard radioButton
        self.ui.radioButton.setChecked(True)

        # Processing the button 'Поиск' using function <<search button>>
        self.ui.pushButton_2.clicked.connect(self.search)

        # set the start table <<Налоги>>
        self.set_table()

    # combine the funtions for recreate db
    def recreate(self):
        result = QtWidgets.QMessageBox.question(self, 'Подтверждение действия',
                                                'Вы уверены, что хотите удалить БД и создать заново?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            recreate_db()

    # function return some info about program
    def about(self):
        QtWidgets.QMessageBox.information(self.ui,
                                    'О программе',
                                    'Данная программа позволяет вести учет налогов, предоставляя возможность работать с базой данных предприятия.')

    def red_text(self):
        self.ui.statusbar.setStyleSheet('''
                                font: bold 12px;
                                color: red;''')

    def green_text(self):
        self.ui.statusbar.setStyleSheet('''
                                font: bold 12px;
                                color: green;''')

    def default_text(self):
        self.ui.statusbar.setStyleSheet('''
                                font: bold 12px;
                                color: black;''')

    # Return the table when you clicked the button "Показать".
    # Depends on the checked radiobutton and last_query (if it calls from some other function)
    def set_table(self, last_query=''):

        def set_size_for_dues():
            header = self.ui.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        def set_size_for_workers():
            header = self.ui.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        def set_size_for_departments():
            header = self.ui.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Если активна <<Налоги>>
        if self.ui.radioButton.isChecked():

            if self.current_table != 'Налоги':
                query = f'''SELECT * FROM [{self.ui.radioButton.text()}]'''
                cursor, sqlite_connection = database_connect()
                cursor.execute(query)
                data = cursor.fetchall()
                self.ui.tableWidget.setColumnCount(0)
                self.ui.tableWidget.setColumnCount(5)
                set_size_for_dues()
                self.ui.tableWidget.setSortingEnabled(False)
                self.ui.tableWidget.setSortingEnabled(True)
                self.ui.tableWidget.setHorizontalHeaderLabels(
                    ['ID', 'ФИО', 'Месяц', 'Зарплата (руб.)', 'Налог (руб.)'])
                self.ui.tableWidget.setRowCount(len(data))
                for i in range(len(data)):
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, data[i][0])
                    self.ui.tableWidget.setItem(i, 0, item)
                    self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                    self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(data[i][2])))
                    item2 = QTableWidgetItem()
                    item2.setData(Qt.DisplayRole, data[i][3])
                    self.ui.tableWidget.setItem(i, 3, item2)
                    item3 = QTableWidgetItem()
                    item3.setData(Qt.DisplayRole, data[i][4])
                    self.ui.tableWidget.setItem(i, 4, item3)
                self.last_query = f'''SELECT * FROM [{self.ui.radioButton.text()}]'''
                cursor.close()
                database_disconnect(sqlite_connection)
                self.default_text()
                self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                self.current_table = self.ui.radioButton.text()
            else:
                if last_query != '':
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(last_query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(5)
                    set_size_for_dues()
                    self.ui.tableWidget.setSortingEnabled(False)
                    self.ui.tableWidget.setSortingEnabled(True)
                    self.ui.tableWidget.setHorizontalHeaderLabels(
                        ['ID', 'ФИО', 'Месяц', 'Зарплата (руб.)', 'Налог (руб.)'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][0])
                        self.ui.tableWidget.setItem(i, 0, item)
                        self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                        self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(data[i][2])))
                        item2 = QTableWidgetItem()
                        item2.setData(Qt.DisplayRole, data[i][3])
                        self.ui.tableWidget.setItem(i, 3, item2)
                        item3 = QTableWidgetItem()
                        item3.setData(Qt.DisplayRole, data[i][4])
                        self.ui.tableWidget.setItem(i, 4, item3)
                    self.last_query = last_query
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    self.current_table = self.ui.radioButton.text()
                else:
                    query = f'''SELECT * FROM [{self.ui.radioButton.text()}]'''
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(5)
                    set_size_for_dues()
                    self.ui.tableWidget.setSortingEnabled(False)
                    self.ui.tableWidget.setSortingEnabled(True)
                    self.ui.tableWidget.setHorizontalHeaderLabels(
                        ['ID', 'ФИО', 'Месяц', 'Зарплата (руб.)', 'Налог (руб.)'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][0])
                        self.ui.tableWidget.setItem(i, 0, item)
                        self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                        self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(data[i][2])))
                        item2 = QTableWidgetItem()
                        item2.setData(Qt.DisplayRole, data[i][3])
                        self.ui.tableWidget.setItem(i, 3, item2)
                        item3 = QTableWidgetItem()
                        item3.setData(Qt.DisplayRole, data[i][4])
                        self.ui.tableWidget.setItem(i, 4, item3)
                    self.last_query = f'''SELECT * FROM [{self.ui.radioButton.text()}]'''
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.current_table = self.ui.radioButton.text()
            cursor, sqlite_connection = database_connect()
            due = f'SELECT SUM([Налог (руб.)]) FROM (SELECT [Налог (руб.)] FROM ({self.last_query}))'
            cursor.execute(due)
            try:
                due = round(cursor.fetchall()[0][0], 2)
            except:
                due = 0
            self.ui.label_3.setText(f'Сумм. налог: {due}')
            cursor.close()
            database_disconnect(sqlite_connection)

        # Если активна <<Работники>>
        elif self.ui.radioButton_2.isChecked():

            if self.current_table != 'Работники':
                query = f'''SELECT * FROM [{self.ui.radioButton_2.text()}]'''
                cursor, sqlite_connection = database_connect()
                cursor.execute(query)
                data = cursor.fetchall()
                self.ui.tableWidget.setColumnCount(0)
                self.ui.tableWidget.setColumnCount(2)
                set_size_for_workers()
                self.ui.tableWidget.setHorizontalHeaderLabels(['ФИО', 'Номер отдела'])
                self.ui.tableWidget.setRowCount(len(data))
                for i in range(len(data)):
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, data[i][1])
                    self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(data[i][0])))
                    self.ui.tableWidget.setItem(i, 1, item)
                self.last_query = f'''SELECT * FROM [{self.ui.radioButton_2.text()}]'''
                cursor.close()
                database_disconnect(sqlite_connection)
                self.default_text()
                self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                self.current_table = self.ui.radioButton_2.text()

            elif self.current_table == 'Работники':
                if last_query != '':
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(last_query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(2)
                    set_size_for_workers()
                    self.ui.tableWidget.setHorizontalHeaderLabels(['ФИО', 'Номер отдела'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][1])
                        self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(data[i][0])))
                        self.ui.tableWidget.setItem(i, 1, item)
                    self.last_query = f'''SELECT * FROM [{self.ui.radioButton_2.text()}]'''
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.last_query = last_query
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    self.current_table = self.ui.radioButton_2.text()
                else:
                    query = f'''SELECT * FROM [{self.ui.radioButton_2.text()}]'''
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(2)
                    set_size_for_workers()
                    self.ui.tableWidget.setHorizontalHeaderLabels(['ФИО', 'Номер отдела'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][1])
                        self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(data[i][0])))
                        self.ui.tableWidget.setItem(i, 1, item)
                    self.last_query = f'''SELECT * FROM [{self.ui.radioButton_2.text()}]'''
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.last_query = last_query
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    self.current_table = self.ui.radioButton_2.text()
            self.ui.label_3.setText('')

        # Если активна <<Отделы>>
        else:
            if self.current_table != 'Отделы':
                query = f'''SELECT * FROM [{self.ui.radioButton_3.text()}]'''
                cursor, sqlite_connection = database_connect()
                cursor.execute(query)
                data = cursor.fetchall()
                self.ui.tableWidget.setColumnCount(0)
                self.ui.tableWidget.setColumnCount(2)
                set_size_for_departments()
                self.ui.tableWidget.setHorizontalHeaderLabels(['Номер отдела', 'Название отдела'])
                self.ui.tableWidget.setRowCount(len(data))
                for i in range(len(data)):
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, data[i][0])
                    self.ui.tableWidget.setItem(i, 0, item)
                    self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                self.last_query = f'''SELECT * FROM [{self.ui.radioButton_3.text()}]'''
                cursor.close()
                database_disconnect(sqlite_connection)
                self.default_text()
                self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                self.current_table = self.ui.radioButton_3.text()

            elif self.current_table == 'Отделы':
                if last_query != '':
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(last_query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(2)
                    set_size_for_departments()
                    self.ui.tableWidget.setHorizontalHeaderLabels(['Номер отдела', 'Название отдела'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][0])
                        self.ui.tableWidget.setItem(i, 0, item)
                        self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                    self.last_query = last_query
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    self.current_table = self.ui.radioButton_3.text()
                else:
                    query = f'''SELECT * FROM [{self.ui.radioButton_3.text()}]'''
                    cursor, sqlite_connection = database_connect()
                    cursor.execute(query)
                    data = cursor.fetchall()
                    self.ui.tableWidget.setColumnCount(0)
                    self.ui.tableWidget.setColumnCount(2)
                    set_size_for_departments()
                    self.ui.tableWidget.setHorizontalHeaderLabels(['Номер отдела', 'Название отдела'])
                    self.ui.tableWidget.setRowCount(len(data))
                    for i in range(len(data)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, data[i][0])
                        self.ui.tableWidget.setItem(i, 0, item)
                        self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(data[i][1])))
                    self.last_query = f'''SELECT * FROM [{self.ui.radioButton_3.text()}]'''
                    cursor.close()
                    database_disconnect(sqlite_connection)
                    self.default_text()
                    self.ui.statusbar.showMessage(f'Кол-во обнаруженных записей по данному запросу - {len(data)}', 1500)
                    self.current_table = self.ui.radioButton_3.text()
            self.ui.label_3.setText('')

        self.ui.label.setText('Таблица: ' + str(self.current_table))

    def search(self):

        if self.current_table == 'Налоги':

            dues_window = search_in_dues_window(self)
            dues_window.show()

            def create_search_query_for_dues():
                min_sal = f'SELECT min([Зарплата (руб.)]) FROM [Налоги]'
                max_sal = f'SELECT max([Зарплата (руб.)]) FROM [Налоги]'
                min_due = f'SELECT min([Налог (руб.)]) FROM [Налоги]'
                max_due = f'SELECT max([Налог (руб.)]) FROM [Налоги]'
                cursor, sqlite_connection = database_connect()
                cursor.execute(min_sal)
                min_sal = cursor.fetchall()[0][0]
                cursor.execute(max_sal)
                max_sal = cursor.fetchall()[0][0]
                cursor.execute(min_due)
                min_due = cursor.fetchall()[0][0]
                cursor.execute(max_due)
                max_due = cursor.fetchall()[0][0]
                cursor.close()
                database_disconnect(sqlite_connection)
                id = dues_window.modal.lineEdit_number.text()
                name = dues_window.modal.lineEdit_number_2.text()
                month = dues_window.modal.lineEdit_number_3.text()
                min_salary = dues_window.modal.lineEdit_number_4.text()
                max_salary = dues_window.modal.lineEdit_number_5.text()
                minimum_due = dues_window.modal.lineEdit_number_6.text()
                maximum_due = dues_window.modal.lineEdit_number_7.text()
                number = dues_window.modal.lineEdit_number_8.text()
                name_of_department = dues_window.modal.lineEdit_number_9.text()
                query = f'SELECT * FROM [Налоги] WHERE [ID] LIKE "{"%" + id + "%" if (id != "") else "%"}" AND ' \
                        f'[ФИО] LIKE "{"%" + name + "%" if (name != "") else "%"}" AND ' \
                        f'[Месяц] LIKE "{"%" + month + "%" if (month != "") else "%"}" AND ' \
                        f'([Зарплата (руб.)] >= "{min_salary if (min_salary != "") else min_sal}" AND ' \
                        f'[Зарплата (руб.)] <= "{max_salary if (max_salary != "") else max_sal}") AND ' \
                        f'([Налог (руб.)] >= "{minimum_due if (minimum_due != "") else min_due}" AND ' \
                        f'[Налог (руб.)] <= "{maximum_due if (maximum_due != "") else max_due}") AND ' \
                        f'([ФИО] IN (SELECT [ФИО] FROM [Работники] WHERE ' \
                        f'[Номер отдела] LIKE "{"%" + number + "%" if (number != "") else "%"}")) AND ' \
                        f'[ФИО] IN (SELECT [ФИО] FROM [Работники] WHERE ' \
                        f'[Номер отдела] IN (SELECT [Номер отдела] FROM [Отделы] WHERE ' \
                        f'[Название отдела] LIKE "{"%"+name_of_department+"%" if (name_of_department!="") else "%"}"))'
                self.ui.radioButton.setChecked(True)
                self.set_table(query)

            dues_window.modal.pushButton.clicked.connect(create_search_query_for_dues)
            dues_window.modal.pushButton.clicked.connect(dues_window.close)

        elif self.current_table == 'Работники':

            worker_window = search_in_workers_window(self)
            worker_window.show()

            def create_search_query_for_workers():
                fio = worker_window.modal.lineedit_fio.text()
                number = worker_window.modal.lineEdit_number.text()
                name_of_department = worker_window.modal.lineEdit_number_2.text()
                query = f'SELECT * FROM [Работники] ' \
                        f'WHERE [ФИО] LIKE "{("%" + fio + "%") if (fio != "") else "%"}" AND ' \
                        f'[Номер отдела] LIKE "{number if (number != "") else "%"}" AND ' \
                        f'[Номер отдела] IN (SELECT [Номер отдела] FROM [Отделы] ' \
                        f'WHERE [Название отдела] LIKE ' \
                        f'"{"%" + name_of_department + "%" if (name_of_department != "") else "%"}")'
                self.ui.radioButton_2.setChecked(True)
                self.set_table(query)

            worker_window.modal.pushButton.clicked.connect(create_search_query_for_workers)
            worker_window.modal.pushButton.clicked.connect(worker_window.close)

        else:

            departments_window = search_in_departments_window(self)
            departments_window.show()

            def create_search_query_for_departments():
                number = departments_window.modal.lineEdit_number.text()
                name = departments_window.modal.lineEdit_number_2.text()
                query = f'SELECT * FROM [Отделы] ' \
                        f'WHERE [Номер отдела] LIKE "{("%" + number + "%") if (number != "") else "%"}" AND ' \
                        f'[Название отдела] LIKE "{("%" + name + "%") if (name != "") else "%"}"'
                self.ui.radioButton_3.setChecked(True)
                self.set_table(query)

            departments_window.modal.pushButton.clicked.connect(create_search_query_for_departments)
            departments_window.modal.pushButton.clicked.connect(departments_window.close)

    # pushButton_4
    def insert_into_table(self):
        if self.current_table == 'Налоги':

            dues_window = insert_into_dues(self)
            dues_window.show()

            def insert_due():
                try:
                    self.SQLInsertThread = SQLThread(mainwindow=dues_window, changewindow=self.ui,
                                                     table=self.current_table, action='Добавление')
                    self.SQLInsertThread.start()
                finally:
                    self.SQLInsertThread.quit()
                    sleep(0.5)
                    self.set_table()
                    if self.ui.result == 'True':
                        self.green_text()
                        self.ui.statusbar.showMessage('Запись успешно добавлена', 1500)
                    else:
                        self.red_text()
                        self.ui.statusbar.showMessage(f'Запись не была добавлена из-за возникшей ошибки - {self.ui.result}', 1500)

            dues_window.insert_into_dues.pushButton.clicked.connect(insert_due)
            dues_window.insert_into_dues.pushButton.clicked.connect(dues_window.close)

        elif self.current_table == 'Работники':

            workers_window = insert_into_workers(self)
            workers_window.show()

            def insert_worker():
                try:
                    self.SQLInsertThread = SQLThread(mainwindow=workers_window, changewindow=self.ui,
                                                     table=self.current_table, action='Добавление')
                    self.SQLInsertThread.start()
                finally:
                    sleep(0.5)
                    self.set_table()
                    self.SQLInsertThread.quit()
                    if self.ui.result == 'True':
                        self.green_text()
                        self.ui.statusbar.showMessage('Запись успешно добавлена', 1500)
                    else:
                        self.red_text()
                        self.ui.statusbar.showMessage(f'Запись не была добавлена из-за возникшей ошибки - {self.ui.result}', 1500)

            workers_window.insert_into_workers.pushButton.clicked.connect(insert_worker)
            workers_window.insert_into_workers.pushButton.clicked.connect(workers_window.close)

        else:

            departments_window = insert_into_departments(self)
            departments_window.show()

            def insert_department():
                try:
                    self.SQLInsertThread = SQLThread(mainwindow=departments_window, changewindow=self.ui,
                                                     table=self.current_table, action='Добавление')
                    self.SQLInsertThread.start()
                finally:
                    sleep(0.5)
                    self.set_table()
                    self.SQLInsertThread.quit()
                    if self.ui.result == 'True':
                        self.green_text()
                        self.ui.statusbar.showMessage('Запись успешно добавлена', 1500)
                    else:
                        self.red_text()
                        self.ui.statusbar.showMessage(f'Запись не была добавлена из-за возникшей ошибки - {self.ui.result}', 1500)


            departments_window.insert_into_departments.pushButton.clicked.connect(insert_department)
            departments_window.insert_into_departments.pushButton.clicked.connect(departments_window.close)

    # pushButton_6
    def delete_from_table(self):

        def func():
            try:
                self.SQLDeleteThread = SQLThread(mainwindow=self.ui, changewindow=None,
                                                 table=self.current_table, action='Удаление')
                self.SQLDeleteThread.start()
            finally:
                self.SQLDeleteThread.quit()

        try:
            if self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0):
                result = QtWidgets.QMessageBox.question(self.ui, 'Подтверждение удаления записи',
                                                        'Вы действительно хотите удалить выбранную запись?',
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    if self.current_table == 'Налоги':
                        func()
                        sleep(0.5)
                        self.set_table(self.last_query)

                    elif self.current_table == 'Работники':
                        func()
                        sleep(0.5)
                        self.set_table(self.last_query)
                    else:
                        func()
                        sleep(0.5)
                        self.set_table(self.last_query)
                else:
                    pass
            else:
                raise Exception('Не выбран столбец')

        except Exception as err:
            self.red_text()
            self.ui.statusbar.showMessage(f'Возникла ошибка - {err}', 1500)
        else:
            self.green_text()
            self.ui.statusbar.showMessage('Запись успешно удалена', 1500)

    # pushbutton_5
    def update_table(self):
        # marker showing that update() is completed successfully
        self.complete = 0
        try:
            if self.current_table == 'Налоги':
                if self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0):
                    dues_window = update_table_dues(self)
                    dues_window.update_table_dues.lineEdit_number.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 1).text())
                    dues_window.update_table_dues.lineEdit_number_2.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
                    dues_window.update_table_dues.lineEdit_number_3.setText(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 3).text()))
                    dues_window.id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()

                    dues_window.show()

                    def update():
                        try:
                            cursor, sqlite_connection = database_connect()
                            id = dues_window.id
                            name = dues_window.update_table_dues.lineEdit_number.text()
                            month = dues_window.update_table_dues.lineEdit_number_2.text()
                            salary = dues_window.update_table_dues.lineEdit_number_3.text()
                            query = f'UPDATE [Налоги] SET [ФИО] = "{name}", [Месяц] = "{month}", ' \
                                    f'[Зарплата (руб.)] = "{salary}" WHERE [ID] = "{id}"'
                            cursor.execute(query)
                            sleep(0.5)
                        except sqlite3.Error as err:
                            self.complete = 0
                            exception = err
                        except Exception as err:
                            self.complete = 0
                        else:
                            self.complete = 1
                        finally:
                            cursor.close()
                            database_disconnect(sqlite_connection)
                            self.set_table(self.last_query)
                            if self.complete == 1:
                                self.green_text()
                                self.ui.statusbar.showMessage('Запись успешно изменена', 1500)
                            else:
                                self.red_text()
                                self.ui.statusbar.showMessage(f'Возникла ошибка - {exception}', 1500)

                    dues_window.update_table_dues.pushButton.clicked.connect(update)
                    dues_window.update_table_dues.pushButton.clicked.connect(dues_window.close)

                else:
                    raise Exception('Не выбран столбец')

            elif self.current_table == 'Работники':
                if self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0):
                    workers_window = update_table_workers(self)
                    workers_window.update_table_workers.lineEdit_number.setText(
                        self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
                    workers_window.update_table_workers.lineEdit_number_2.setText(
                        self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 1).text())

                    workers_window.old_name = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()

                    workers_window.show()

                    def update():
                        try:
                            cursor, sqlite_connection = database_connect()
                            name = workers_window.update_table_workers.lineEdit_number.text()
                            department = workers_window.update_table_workers.lineEdit_number_2.text()

                            query = f'UPDATE [Работники] SET [ФИО] = "{name}", [Номер отдела] = {department} ' \
                                    f'WHERE [ФИО] = "{workers_window.old_name}"'
                            cursor.execute(query)
                            sleep(0.5)
                        except sqlite3.Error as err:
                            self.complete = 0
                            exception = err
                        except Exception as err:
                            self.complete = 0
                        else:
                            self.complete = 1
                        finally:
                            cursor.close()
                            database_disconnect(sqlite_connection)
                            self.set_table(self.last_query)
                            if self.complete == 1:
                                self.green_text()
                                self.ui.statusbar.showMessage('Запись успешно изменена', 1500)
                            else:
                                self.red_text()
                                self.ui.statusbar.showMessage(f'Возникла ошибка - {exception}', 1500)

                    workers_window.update_table_workers.pushButton.clicked.connect(update)
                    workers_window.update_table_workers.pushButton.clicked.connect(workers_window.close)

                else:
                    raise Exception('Не выбран столбец')

            else:
                if self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0):
                    departments_window = update_table_departments(self)
                    departments_window.update_table_departments.number_4.setText(
                        self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
                    departments_window.update_table_departments.lineEdit_number_2.setText(
                        self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 1).text())

                    departments_window.number = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()

                    departments_window.show()

                    def update():
                        try:
                            cursor, sqlite_connection = database_connect()
                            name = departments_window.update_table_departments.lineEdit_number_2.text()
                            query = f'UPDATE [Отделы] SET [Название отдела] = "{name}" ' \
                                    f'WHERE [Номер отдела] = {departments_window.number}'
                            cursor.execute(query)
                            sleep(0.5)
                        except sqlite3.Error as err:
                            self.complete = 0
                            exception = err
                        except Exception as err:
                            self.complete = 0
                        else:
                            self.complete = 1
                        finally:
                            cursor.close()
                            database_disconnect(sqlite_connection)
                            self.set_table(self.last_query)
                            if self.complete == 1:
                                self.green_text()
                                self.ui.statusbar.showMessage('Запись успешно изменена', 1500)
                            else:
                                self.red_text()
                                self.ui.statusbar.showMessage(f'Возникла ошибка - {exception}', 1500)

                    departments_window.update_table_departments.pushButton.clicked.connect(update)
                    departments_window.update_table_departments.pushButton.clicked.connect(departments_window.close)

                else:
                    raise Exception('Не выбран столбец')

        except Exception as err:
            self.red_text()
            self.ui.statusbar.showMessage(f'Возникла ошибка - {err}', 1500)

    # Notification about successful xml convertation
    def xml_notification(self):
        to_xml()
        QtWidgets.QMessageBox.about(self, 'Оповещение', 'Запись успешно сохранена в xml.')

    # Notification about successful json convertation
    def json_notification(self):
        to_json()
        QtWidgets.QMessageBox.about(self, 'Оповещение', 'Запись успешно сохранена в json')


class search_in_workers_window(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form()
        self.modal.setupUi(self)
        self.setWindowModality(2)


class search_in_departments_window(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form2()
        self.modal.setupUi(self)
        self.setWindowModality(2)


class search_in_dues_window(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.modal = Ui_Form3()
        self.modal.setupUi(self)
        self.setWindowModality(2)


class insert_into_workers(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.insert_into_workers = Ui_Form4()
        self.insert_into_workers.setupUi(self)
        self.setWindowModality(2)


class insert_into_departments(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.insert_into_departments = Ui_Form5()
        self.insert_into_departments.setupUi(self)
        self.setWindowModality(2)


class insert_into_dues(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.insert_into_dues = Ui_Form6()
        self.insert_into_dues.setupUi(self)
        self.setWindowModality(2)


class update_table_workers(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.update_table_workers = Ui_Form7()
        self.update_table_workers.setupUi(self)
        self.setWindowModality(2)


class update_table_departments(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.update_table_departments = Ui_Form8()
        self.update_table_departments.setupUi(self)
        self.setWindowModality(2)


class update_table_dues(QtWidgets.QWidget):
    def __init__(self, parent=GUI):
        super().__init__(parent, QtCore.Qt.Window)
        self.update_table_dues = Ui_Form9()
        self.update_table_dues.setupUi(self)
        self.setWindowModality(2)


if __name__ == '__main__':
    try:
        create_database()
        app = QtWidgets.QApplication(sys.argv)
        window = GUI()
        window.show()
        sys.exit(app.exec_())

    except Exception as error:
        print(f'Ошибка при работе программы - {error}')

    finally:
        print('Конец работы')

