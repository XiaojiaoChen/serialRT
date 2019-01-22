# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\40207\OneDrive\OneDriveDocumentation\PythonWorkSpace\serialRT\serialRT\UIMainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWidget(object):
    def setupUi(self, mainWidget):
        mainWidget.setObjectName("mainWidget")
        mainWidget.resize(985, 418)
        mainWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout_2 = QtWidgets.QGridLayout(mainWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(mainWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 3, 2, 1, 2)
        self.sequence = MySequence(mainWidget)
        self.sequence.setMinimumSize(QtCore.QSize(0, 0))
        self.sequence.setObjectName("sequence")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.sequence)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout.addWidget(self.sequence, 2, 0, 2, 1)
        self.saveButton = QtWidgets.QPushButton(mainWidget)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 2, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.serial = MySerial(mainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial.sizePolicy().hasHeightForWidth())
        self.serial.setSizePolicy(sizePolicy)
        self.serial.setMinimumSize(QtCore.QSize(0, 0))
        self.serial.setObjectName("serial")
        self.gridLayout.addWidget(self.serial, 0, 2, 2, 2)
        spacerItem2 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 2, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 1)
        self.hand = MyHand(mainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hand.sizePolicy().hasHeightForWidth())
        self.hand.setSizePolicy(sizePolicy)
        self.hand.setMinimumSize(QtCore.QSize(0, 30))
        self.hand.setMaximumSize(QtCore.QSize(1400, 600))
        self.hand.setObjectName("hand")
        self.gridLayout.addWidget(self.hand, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(mainWidget)
        self.hand.sigSendCommand['QString'].connect(self.serial.slotSendRequest)
        self.hand.sigAddFrame.connect(self.sequence.slotAddFrame)
        self.sequence.sigSendCommandFromSequence.connect(self.serial.slotSendRequestBin)
        self.saveButton.clicked.connect(self.hand.slotSaveConfiguration)
        self.sequence.sigReadyToSave.connect(mainWidget.slotReadyToSave)
        self.hand.sigReadyToSave.connect(self.sequence.slotSaveConfiguration)
        self.serial.sigNewLine.connect(self.hand.slotNewDataArrived)
        self.serial.sigAngleCommandChanged.connect(self.hand.slotAngleCommandChanged)
        self.hand.sigSendLeapMotion.connect(self.serial.slotSendRequestBin)
        QtCore.QMetaObject.connectSlotsByName(mainWidget)

    def retranslateUi(self, mainWidget):
        _translate = QtCore.QCoreApplication.translate
        mainWidget.setWindowTitle(_translate("mainWidget", "SoftHand"))
        self.saveButton.setText(_translate("mainWidget", "Save Configuration"))

from myHand import MyHand
from mySequence import MySequence
from mySerial import MySerial
