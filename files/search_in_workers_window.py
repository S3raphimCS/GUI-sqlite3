# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_in_workers_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(284, 325)
        Form.setMinimumSize(QtCore.QSize(284, 325))
        Form.setMaximumSize(QtCore.QSize(284, 325))
        self.name = QtWidgets.QLabel(Form)
        self.name.setGeometry(QtCore.QRect(20, 20, 251, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.FIO = QtWidgets.QLabel(Form)
        self.FIO.setGeometry(QtCore.QRect(20, 80, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.FIO.setFont(font)
        self.FIO.setObjectName("FIO")
        self.number = QtWidgets.QLabel(Form)
        self.number.setGeometry(QtCore.QRect(20, 130, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number.setFont(font)
        self.number.setObjectName("number")
        self.lineEdit_number = QtWidgets.QLineEdit(Form)
        self.lineEdit_number.setGeometry(QtCore.QRect(130, 130, 131, 31))
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.lineedit_fio = QtWidgets.QLineEdit(Form)
        self.lineedit_fio.setGeometry(QtCore.QRect(130, 80, 131, 31))
        self.lineedit_fio.setObjectName("lineedit_fio")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 250, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.number_2 = QtWidgets.QLabel(Form)
        self.number_2.setGeometry(QtCore.QRect(20, 170, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number_2.setFont(font)
        self.number_2.setWordWrap(True)
        self.number_2.setObjectName("number_2")
        self.lineEdit_number_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_number_2.setGeometry(QtCore.QRect(130, 180, 131, 31))
        self.lineEdit_number_2.setObjectName("lineEdit_number_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name.setText(_translate("Form", "Поиск в таблице Работники"))
        self.FIO.setText(_translate("Form", "ФИО"))
        self.number.setText(_translate("Form", "Номер отдела"))
        self.pushButton.setText(_translate("Form", "Искать"))
        self.number_2.setText(_translate("Form", "Название отдела"))