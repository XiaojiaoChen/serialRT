# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\40207\OneDrive\OneDriveDocumentation\PythonWorkSpace\serialRT\serialRT\UISerial.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_serialGUI(object):
    def setupUi(self, serialGUI):
        serialGUI.setObjectName("serialGUI")
        serialGUI.resize(379, 531)
        self.gridLayout_3 = QtWidgets.QGridLayout(serialGUI)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.portButton = QtWidgets.QPushButton(serialGUI)
        self.portButton.setObjectName("portButton")
        self.gridLayout.addWidget(self.portButton, 0, 0, 1, 1)
        self.baudRate = QtWidgets.QComboBox(serialGUI)
        self.baudRate.setEditable(False)
        self.baudRate.setObjectName("baudRate")
        self.baudRate.addItem("")
        self.baudRate.addItem("")
        self.baudRate.addItem("")
        self.baudRate.addItem("")
        self.gridLayout.addWidget(self.baudRate, 1, 1, 1, 1)
        self.portList = QtWidgets.QComboBox(serialGUI)
        self.portList.setObjectName("portList")
        self.gridLayout.addWidget(self.portList, 0, 1, 1, 1)
        self.baudLabel = QtWidgets.QLabel(serialGUI)
        self.baudLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.baudLabel.setObjectName("baudLabel")
        self.gridLayout.addWidget(self.baudLabel, 1, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.connectButton = QtWidgets.QPushButton(serialGUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setCheckable(True)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_2.addWidget(self.connectButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.receiveText = QtWidgets.QPlainTextEdit(serialGUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receiveText.sizePolicy().hasHeightForWidth())
        self.receiveText.setSizePolicy(sizePolicy)
        self.receiveText.setReadOnly(True)
        self.receiveText.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.receiveText.setObjectName("receiveText")
        self.verticalLayout_2.addWidget(self.receiveText)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelRx = QtWidgets.QLabel(serialGUI)
        self.labelRx.setObjectName("labelRx")
        self.horizontalLayout_3.addWidget(self.labelRx)
        self.RxNum = QtWidgets.QLabel(serialGUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RxNum.sizePolicy().hasHeightForWidth())
        self.RxNum.setSizePolicy(sizePolicy)
        self.RxNum.setMinimumSize(QtCore.QSize(60, 0))
        self.RxNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.RxNum.setObjectName("RxNum")
        self.horizontalLayout_3.addWidget(self.RxNum)
        self.labelTx = QtWidgets.QLabel(serialGUI)
        self.labelTx.setObjectName("labelTx")
        self.horizontalLayout_3.addWidget(self.labelTx)
        self.TxNum = QtWidgets.QLabel(serialGUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TxNum.sizePolicy().hasHeightForWidth())
        self.TxNum.setSizePolicy(sizePolicy)
        self.TxNum.setMinimumSize(QtCore.QSize(50, 0))
        self.TxNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TxNum.setObjectName("TxNum")
        self.horizontalLayout_3.addWidget(self.TxNum)
        self.saveButton = QtWidgets.QPushButton(serialGUI)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.RxType = QtWidgets.QComboBox(serialGUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RxType.sizePolicy().hasHeightForWidth())
        self.RxType.setSizePolicy(sizePolicy)
        self.RxType.setObjectName("RxType")
        self.RxType.addItem("")
        self.RxType.addItem("")
        self.horizontalLayout_3.addWidget(self.RxType)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sendText = QtWidgets.QPlainTextEdit(serialGUI)
        self.sendText.setReadOnly(False)
        self.sendText.setObjectName("sendText")
        self.horizontalLayout.addWidget(self.sendText)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sendButton = QtWidgets.QPushButton(serialGUI)
        self.sendButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendButton.sizePolicy().hasHeightForWidth())
        self.sendButton.setSizePolicy(sizePolicy)
        self.sendButton.setObjectName("sendButton")
        self.verticalLayout.addWidget(self.sendButton)
        self.clearButton = QtWidgets.QPushButton(serialGUI)
        self.clearButton.setObjectName("clearButton")
        self.verticalLayout.addWidget(self.clearButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(serialGUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.historyList = QtWidgets.QListWidget(self.groupBox)
        self.historyList.setObjectName("historyList")
        self.gridLayout_2.addWidget(self.historyList, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(serialGUI)
        self.connectButton.toggled['bool'].connect(serialGUI.connectButtonClicked)
        self.portButton.clicked.connect(serialGUI.portButtonClicked)
        self.sendButton.clicked.connect(serialGUI.sendButtonClicked)
        self.clearButton.clicked.connect(serialGUI.clearButtonClicked)
        self.saveButton.clicked.connect(serialGUI.saveButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(serialGUI)

    def retranslateUi(self, serialGUI):
        _translate = QtCore.QCoreApplication.translate
        serialGUI.setWindowTitle(_translate("serialGUI", "Form"))
        self.portButton.setText(_translate("serialGUI", "Port"))
        self.baudRate.setItemText(0, _translate("serialGUI", "921600"))
        self.baudRate.setItemText(1, _translate("serialGUI", "256000"))
        self.baudRate.setItemText(2, _translate("serialGUI", "115200"))
        self.baudRate.setItemText(3, _translate("serialGUI", "9600"))
        self.baudLabel.setText(_translate("serialGUI", "BaudRate"))
        self.connectButton.setText(_translate("serialGUI", "Connect"))
        self.labelRx.setText(_translate("serialGUI", "Rx:"))
        self.RxNum.setText(_translate("serialGUI", "0"))
        self.labelTx.setText(_translate("serialGUI", "Tx:"))
        self.TxNum.setText(_translate("serialGUI", "0"))
        self.saveButton.setText(_translate("serialGUI", "Save"))
        self.RxType.setItemText(0, _translate("serialGUI", "Text Display"))
        self.RxType.setItemText(1, _translate("serialGUI", "Bin Display"))
        self.sendButton.setText(_translate("serialGUI", "Send"))
        self.sendButton.setShortcut(_translate("serialGUI", "Ctrl+Return"))
        self.clearButton.setText(_translate("serialGUI", "CLear"))
        self.groupBox.setTitle(_translate("serialGUI", "Command History"))
