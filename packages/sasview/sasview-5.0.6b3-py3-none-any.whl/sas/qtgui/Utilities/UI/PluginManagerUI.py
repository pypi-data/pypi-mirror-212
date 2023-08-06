# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\PluginManagerUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PluginManagerUI(object):
    def setupUi(self, PluginManagerUI):
        PluginManagerUI.setObjectName("PluginManagerUI")
        PluginManagerUI.resize(528, 442)
        self.gridLayout = QtWidgets.QGridLayout(PluginManagerUI)
        self.gridLayout.setObjectName("gridLayout")
        self.lstModels = QtWidgets.QListWidget(PluginManagerUI)
        self.lstModels.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.lstModels.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstModels.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstModels.setObjectName("lstModels")
        self.gridLayout.addWidget(self.lstModels, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cmdAdd = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdAdd.setObjectName("cmdAdd")
        self.verticalLayout.addWidget(self.cmdAdd)
        self.cmdAddFile = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdAddFile.setObjectName("cmdAddFile")
        self.verticalLayout.addWidget(self.cmdAddFile)
        self.cmdDuplicate = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdDuplicate.setObjectName("cmdDuplicate")
        self.verticalLayout.addWidget(self.cmdDuplicate)
        self.cmdEdit = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdEdit.setObjectName("cmdEdit")
        self.verticalLayout.addWidget(self.cmdEdit)
        self.cmdDelete = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdDelete.setObjectName("cmdDelete")
        self.verticalLayout.addWidget(self.cmdDelete)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdHelp = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdHelp.setObjectName("cmdHelp")
        self.horizontalLayout.addWidget(self.cmdHelp)
        self.cmdOK = QtWidgets.QPushButton(PluginManagerUI)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(PluginManagerUI)
        QtCore.QMetaObject.connectSlotsByName(PluginManagerUI)

    def retranslateUi(self, PluginManagerUI):
        _translate = QtCore.QCoreApplication.translate
        PluginManagerUI.setWindowTitle(_translate("PluginManagerUI", "Plugin Manager"))
        self.cmdAdd.setText(_translate("PluginManagerUI", "Add..."))
        self.cmdAddFile.setText(_translate("PluginManagerUI", "Add file..."))
        self.cmdDuplicate.setText(_translate("PluginManagerUI", "Duplicate"))
        self.cmdEdit.setText(_translate("PluginManagerUI", "Edit..."))
        self.cmdDelete.setText(_translate("PluginManagerUI", "Delete"))
        self.cmdHelp.setText(_translate("PluginManagerUI", "Help"))
        self.cmdOK.setText(_translate("PluginManagerUI", "Close"))

