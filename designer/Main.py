# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(545, 206)
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.dateEdit_start_date = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_start_date.setCalendarPopup(True)
        self.dateEdit_start_date.setObjectName("dateEdit_start_date")
        self.gridLayout.addWidget(self.dateEdit_start_date, 1, 1, 1, 1)
        self.label_path_folder = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_path_folder.sizePolicy().hasHeightForWidth())
        self.label_path_folder.setSizePolicy(sizePolicy)
        self.label_path_folder.setObjectName("label_path_folder")
        self.gridLayout.addWidget(self.label_path_folder, 0, 0, 1, 1)
        self.label_device = QtWidgets.QLabel(self.centralwidget)
        self.label_device.setObjectName("label_device")
        self.gridLayout.addWidget(self.label_device, 1, 2, 1, 1)
        self.spinBox_device = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_device.setMinimum(1)
        self.spinBox_device.setMaximum(10000)
        self.spinBox_device.setObjectName("spinBox_device")
        self.gridLayout.addWidget(self.spinBox_device, 1, 3, 1, 1)
        self.lineEdit_path_folder = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_path_folder.setObjectName("lineEdit_path_folder")
        self.gridLayout.addWidget(self.lineEdit_path_folder, 0, 1, 1, 2)
        self.pushButton_path_folder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_path_folder.setObjectName("pushButton_path_folder")
        self.gridLayout.addWidget(self.pushButton_path_folder, 0, 3, 1, 1)
        self.label_start_date = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_start_date.sizePolicy().hasHeightForWidth())
        self.label_start_date.setSizePolicy(sizePolicy)
        self.label_start_date.setObjectName("label_start_date")
        self.gridLayout.addWidget(self.label_start_date, 1, 0, 1, 1)
        self.pushButton_start_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_stop.setObjectName("pushButton_start_stop")
        self.gridLayout.addWidget(self.pushButton_start_stop, 2, 1, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Изменение дат"))
        self.label_path_folder.setText(_translate("MainWindow", "Путь к папке"))
        self.label_device.setText(_translate("MainWindow", "Изделий в сутках"))
        self.pushButton_path_folder.setText(_translate("MainWindow", "Открыть"))
        self.label_start_date.setText(_translate("MainWindow", "Начальная дата"))
        self.pushButton_start_stop.setText(_translate("MainWindow", "Старт"))