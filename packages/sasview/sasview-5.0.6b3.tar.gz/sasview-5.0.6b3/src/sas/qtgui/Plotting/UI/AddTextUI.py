# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Plotting\UI\AddTextUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddText(object):
    def setupUi(self, AddText):
        AddText.setObjectName("AddText")
        AddText.setWindowModality(QtCore.Qt.ApplicationModal)
        AddText.resize(432, 324)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddText.sizePolicy().hasHeightForWidth())
        AddText.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(AddText)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(AddText)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 44, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnFont = QtWidgets.QPushButton(AddText)
        self.btnFont.setObjectName("btnFont")
        self.horizontalLayout.addWidget(self.btnFont)
        self.btnColor = QtWidgets.QPushButton(AddText)
        self.btnColor.setObjectName("btnColor")
        self.horizontalLayout.addWidget(self.btnColor)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddText)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(AddText)
        self.buttonBox.accepted.connect(AddText.accept)
        self.buttonBox.rejected.connect(AddText.reject)
        QtCore.QMetaObject.connectSlotsByName(AddText)

    def retranslateUi(self, AddText):
        _translate = QtCore.QCoreApplication.translate
        AddText.setWindowTitle(_translate("AddText", "Add Text"))
        self.groupBox.setTitle(_translate("AddText", "Custom Text "))
        self.btnFont.setText(_translate("AddText", "Font..."))
        self.btnColor.setText(_translate("AddText", "Color..."))

