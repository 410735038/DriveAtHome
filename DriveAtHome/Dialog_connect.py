# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_connect.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_connect(object):
    def setupUi(self, Dialog_connect):
        Dialog_connect.setObjectName("Dialog_connect")
        Dialog_connect.resize(400, 300)
        self.car_con_lab = QtWidgets.QLabel(Dialog_connect)
        self.car_con_lab.setGeometry(QtCore.QRect(130, 180, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.car_con_lab.setFont(font)
        self.car_con_lab.setObjectName("car_con_lab")
        self.wait_dia_btn = QtWidgets.QPushButton(Dialog_connect)
        self.wait_dia_btn.setGeometry(QtCore.QRect(150, 240, 93, 28))
        self.wait_dia_btn.setObjectName("wait_dia_btn")
        self.show_car_loading_gif = QtWidgets.QLabel(Dialog_connect)
        self.show_car_loading_gif.setGeometry(QtCore.QRect(70, 60, 271, 111))
        self.show_car_loading_gif.setText("")
        self.show_car_loading_gif.setObjectName("show_car_loading_gif")

        self.retranslateUi(Dialog_connect)
        QtCore.QMetaObject.connectSlotsByName(Dialog_connect)

    def retranslateUi(self, Dialog_connect):
        _translate = QtCore.QCoreApplication.translate
        Dialog_connect.setWindowTitle(_translate("Dialog_connect", "Dialog"))
        self.car_con_lab.setText(_translate("Dialog_connect", "車子連接中"))
        self.wait_dia_btn.setText(_translate("Dialog_connect", "取消"))