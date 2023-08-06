# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Plotting\UI\WindowTitleUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WindowTitle(object):
    def setupUi(self, WindowTitle):
        WindowTitle.setObjectName("WindowTitle")
        WindowTitle.setWindowModality(QtCore.Qt.ApplicationModal)
        WindowTitle.resize(287, 137)
        self.gridLayout = QtWidgets.QGridLayout(WindowTitle)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WindowTitle)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtTitle = QtWidgets.QLineEdit(WindowTitle)
        self.txtTitle.setObjectName("txtTitle")
        self.gridLayout.addWidget(self.txtTitle, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(WindowTitle)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(WindowTitle)
        self.buttonBox.accepted.connect(WindowTitle.accept)
        self.buttonBox.rejected.connect(WindowTitle.reject)
        QtCore.QMetaObject.connectSlotsByName(WindowTitle)

    def retranslateUi(self, WindowTitle):
        _translate = QtCore.QCoreApplication.translate
        WindowTitle.setWindowTitle(_translate("WindowTitle", "Modify Window Title"))
        self.label.setText(_translate("WindowTitle", "New title"))

