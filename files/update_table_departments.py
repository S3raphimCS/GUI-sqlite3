# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update_table_departments.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form8(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(394, 283)
        Form.setMinimumSize(QtCore.QSize(394, 283))
        Form.setMaximumSize(QtCore.QSize(394, 283))
        self.number_2 = QtWidgets.QLabel(Form)
        self.number_2.setGeometry(QtCore.QRect(20, 140, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number_2.setFont(font)
        self.number_2.setWordWrap(True)
        self.number_2.setObjectName("number_2")
        self.number_3 = QtWidgets.QLabel(Form)
        self.number_3.setGeometry(QtCore.QRect(20, 70, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number_3.setFont(font)
        self.number_3.setWordWrap(True)
        self.number_3.setObjectName("number_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 220, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_number_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_number_2.setGeometry(QtCore.QRect(120, 150, 261, 31))
        self.lineEdit_number_2.setObjectName("lineEdit_number_2")
        self.name = QtWidgets.QLabel(Form)
        self.name.setGeometry(QtCore.QRect(110, 30, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.number_4 = QtWidgets.QLabel(Form)
        self.number_4.setGeometry(QtCore.QRect(120, 70, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number_4.setFont(font)
        self.number_4.setText("")
        self.number_4.setWordWrap(True)
        self.number_4.setObjectName("number_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.number_2.setText(_translate("Form", "Название отдела"))
        self.number_3.setText(_translate("Form", "Номер отдела"))
        self.pushButton.setText(_translate("Form", "Изменить"))
        self.name.setText(_translate("Form", "Изменение записи"))
