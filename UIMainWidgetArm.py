# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\40207\OneDrive\OneDriveDocumentation\PythonWorkSpace\serialRT\serialRT\UIMainWidgetArm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWidgetArm(object):
    def setupUi(self, mainWidgetArm):
        mainWidgetArm.setObjectName("mainWidgetArm")
        mainWidgetArm.resize(985, 324)
        mainWidgetArm.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout_2 = QtWidgets.QGridLayout(mainWidgetArm)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.arm = MyArm(mainWidgetArm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arm.sizePolicy().hasHeightForWidth())
        self.arm.setSizePolicy(sizePolicy)
        self.arm.setMinimumSize(QtCore.QSize(0, 30))
        self.arm.setMaximumSize(QtCore.QSize(1400, 600))
        self.arm.setObjectName("arm")
        self.gridLayout_2.addWidget(self.arm, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.serial = MySerial(mainWidgetArm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial.sizePolicy().hasHeightForWidth())
        self.serial.setSizePolicy(sizePolicy)
        self.serial.setMinimumSize(QtCore.QSize(0, 0))
        self.serial.setObjectName("serial")
        self.gridLayout.addWidget(self.serial, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(mainWidgetArm)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(mainWidgetArm)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.retranslateUi(mainWidgetArm)
        self.serial.sigNewLine.connect(self.arm.slotNewDataArrived)
        self.arm.sigSendCommand['QString'].connect(self.serial.slotSendRequest)
        QtCore.QMetaObject.connectSlotsByName(mainWidgetArm)

    def retranslateUi(self, mainWidgetArm):
        _translate = QtCore.QCoreApplication.translate
        mainWidgetArm.setWindowTitle(_translate("mainWidgetArm", "SoftHand"))
        self.saveButton.setText(_translate("mainWidgetArm", "Save Configuration"))

from myArm import MyArm
from mySerial import MySerial
