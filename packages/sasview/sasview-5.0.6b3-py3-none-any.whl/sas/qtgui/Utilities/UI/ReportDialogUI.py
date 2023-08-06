# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\ReportDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReportDialogUI(object):
    def setupUi(self, ReportDialogUI):
        ReportDialogUI.setObjectName("ReportDialogUI")
        ReportDialogUI.resize(519, 461)
        self.gridLayout = QtWidgets.QGridLayout(ReportDialogUI)
        self.gridLayout.setObjectName("gridLayout")
        self.txtBrowser = QtWidgets.QTextBrowser(ReportDialogUI)
        self.txtBrowser.setObjectName("txtBrowser")
        self.gridLayout.addWidget(self.txtBrowser, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdPrint = QtWidgets.QPushButton(ReportDialogUI)
        self.cmdPrint.setObjectName("cmdPrint")
        self.horizontalLayout.addWidget(self.cmdPrint)
        self.cmdSave = QtWidgets.QPushButton(ReportDialogUI)
        self.cmdSave.setObjectName("cmdSave")
        self.horizontalLayout.addWidget(self.cmdSave)
        self.cmdClose = QtWidgets.QPushButton(ReportDialogUI)
        self.cmdClose.setObjectName("cmdClose")
        self.horizontalLayout.addWidget(self.cmdClose)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(ReportDialogUI)
        self.cmdClose.clicked.connect(ReportDialogUI.close)
        QtCore.QMetaObject.connectSlotsByName(ReportDialogUI)

    def retranslateUi(self, ReportDialogUI):
        _translate = QtCore.QCoreApplication.translate
        ReportDialogUI.setWindowTitle(_translate("ReportDialogUI", "Report: Fitting"))
        self.cmdPrint.setText(_translate("ReportDialogUI", "Print"))
        self.cmdSave.setText(_translate("ReportDialogUI", "Save"))
        self.cmdClose.setText(_translate("ReportDialogUI", "Close"))

