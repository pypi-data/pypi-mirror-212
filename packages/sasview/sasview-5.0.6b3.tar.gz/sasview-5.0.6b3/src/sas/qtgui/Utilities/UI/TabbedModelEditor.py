# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\TabbedModelEditor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabbedModelEditor(object):
    def setupUi(self, TabbedModelEditor):
        TabbedModelEditor.setObjectName("TabbedModelEditor")
        TabbedModelEditor.resize(688, 697)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabbedModelEditor.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(TabbedModelEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(TabbedModelEditor)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmdLoad = QtWidgets.QPushButton(TabbedModelEditor)
        self.cmdLoad.setObjectName("cmdLoad")
        self.horizontalLayout.addWidget(self.cmdLoad)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(TabbedModelEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TabbedModelEditor)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(TabbedModelEditor)

    def retranslateUi(self, TabbedModelEditor):
        _translate = QtCore.QCoreApplication.translate
        TabbedModelEditor.setWindowTitle(_translate("TabbedModelEditor", "Model Editor"))
        self.cmdLoad.setText(_translate("TabbedModelEditor", "Load plugin..."))

