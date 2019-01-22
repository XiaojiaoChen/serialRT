# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\40207\OneDrive\OneDriveDocumentation\PythonWorkSpace\serialRT\serialRT\UIBellow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_bellow(object):
    def setupUi(self, bellow):
        bellow.setObjectName("bellow")
        bellow.resize(189, 85)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(bellow.sizePolicy().hasHeightForWidth())
        bellow.setSizePolicy(sizePolicy)
        bellow.setMaximumSize(QtCore.QSize(116775, 116775))
        self.gridLayout_2 = QtWidgets.QGridLayout(bellow)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.digit = QtWidgets.QGroupBox(bellow)
        self.digit.setAlignment(QtCore.Qt.AlignCenter)
        self.digit.setFlat(False)
        self.digit.setCheckable(False)
        self.digit.setObjectName("digit")
        self.gridLayout = QtWidgets.QGridLayout(self.digit)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.digit)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.digit)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.pressureReal = QtWidgets.QLabel(self.digit)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressureReal.setFont(font)
        self.pressureReal.setAlignment(QtCore.Qt.AlignCenter)
        self.pressureReal.setObjectName("pressureReal")
        self.gridLayout.addWidget(self.pressureReal, 1, 0, 1, 1)
        self.pressure = QtWidgets.QSpinBox(self.digit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pressure.sizePolicy().hasHeightForWidth())
        self.pressure.setSizePolicy(sizePolicy)
        self.pressure.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressure.setFont(font)
        self.pressure.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pressure.setAutoFillBackground(False)
        self.pressure.setAlignment(QtCore.Qt.AlignCenter)
        self.pressure.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.pressure.setMinimum(-100)
        self.pressure.setMaximum(200)
        self.pressure.setObjectName("pressure")
        self.gridLayout.addWidget(self.pressure, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.digit, 0, 0, 1, 1)

        self.retranslateUi(bellow)
        self.pressure.valueChanged['int'].connect(bellow.slotPressureValueChanged)
        QtCore.QMetaObject.connectSlotsByName(bellow)

    def retranslateUi(self, bellow):
        _translate = QtCore.QCoreApplication.translate
        bellow.setWindowTitle(_translate("bellow", "Form"))
        self.digit.setTitle(_translate("bellow", "DIP"))
        self.label_2.setText(_translate("bellow", "Measure"))
        self.label.setText(_translate("bellow", "Command"))
        self.pressureReal.setText(_translate("bellow", "0"))

