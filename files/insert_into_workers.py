# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insert_into_workers.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form4(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(396, 291)
        Form.setMinimumSize(QtCore.QSize(396, 291))
        Form.setMaximumSize(QtCore.QSize(396, 291))
        self.lineEdit_number = QtWidgets.QLineEdit(Form)
        self.lineEdit_number.setGeometry(QtCore.QRect(120, 80, 261, 31))
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.FIO_2 = QtWidgets.QLabel(Form)
        self.FIO_2.setGeometry(QtCore.QRect(20, 80, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.FIO_2.setFont(font)
        self.FIO_2.setObjectName("FIO_2")
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
        self.name.setGeometry(QtCore.QRect(20, 20, 361, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.number_2 = QtWidgets.QLabel(Form)
        self.number_2.setGeometry(QtCore.QRect(20, 140, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.number_2.setFont(font)
        self.number_2.setWordWrap(True)
        self.number_2.setObjectName("number_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.FIO_2.setText(_translate("Form", "??????"))
        self.pushButton.setText(_translate("Form", "????????????????"))
        self.name.setText(_translate("Form", "???????????????????? ???????????? ?? ?????????????? ??????????????????"))
        self.number_2.setText(_translate("Form", "?????????? ????????????"))
