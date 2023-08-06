# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\ModelEditor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ModelEditor(object):
    def setupUi(self, ModelEditor):
        ModelEditor.setObjectName("ModelEditor")
        ModelEditor.resize(549, 632)
        self.gridLayout = QtWidgets.QGridLayout(ModelEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_13 = QtWidgets.QGroupBox(ModelEditor)
        self.groupBox_13.setObjectName("groupBox_13")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.groupBox_13)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.txtEditor = QCodeEditor(self.groupBox_13)
        self.txtEditor.setObjectName("txtEditor")
        self.gridLayout_16.addWidget(self.txtEditor, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_13, 0, 0, 1, 1)

        self.retranslateUi(ModelEditor)
        QtCore.QMetaObject.connectSlotsByName(ModelEditor)

    def retranslateUi(self, ModelEditor):
        _translate = QtCore.QCoreApplication.translate
        ModelEditor.setWindowTitle(_translate("ModelEditor", "Model Editor"))
        self.groupBox_13.setTitle(_translate("ModelEditor", "Model"))

from sas.qtgui.Utilities.CodeEditor import QCodeEditor
