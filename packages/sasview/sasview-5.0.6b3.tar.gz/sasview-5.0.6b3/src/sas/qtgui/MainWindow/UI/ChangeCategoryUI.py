# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\MainWindow\UI\ChangeCategoryUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangeCategoryUI(object):
    def setupUi(self, ChangeCategoryUI):
        ChangeCategoryUI.setObjectName("ChangeCategoryUI")
        ChangeCategoryUI.resize(357, 485)
        self.gridLayout_2 = QtWidgets.QGridLayout(ChangeCategoryUI)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblTitle = QtWidgets.QLabel(ChangeCategoryUI)
        self.lblTitle.setObjectName("lblTitle")
        self.gridLayout_2.addWidget(self.lblTitle, 0, 0, 1, 1)
        self.lstCategories = QtWidgets.QListWidget(ChangeCategoryUI)
        self.lstCategories.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lstCategories.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lstCategories.setObjectName("lstCategories")
        self.gridLayout_2.addWidget(self.lstCategories, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(ChangeCategoryUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.rbExisting = QtWidgets.QRadioButton(self.groupBox)
        self.rbExisting.setObjectName("rbExisting")
        self.gridLayout.addWidget(self.rbExisting, 0, 0, 1, 1)
        self.txtNewCategory = QtWidgets.QLineEdit(self.groupBox)
        self.txtNewCategory.setObjectName("txtNewCategory")
        self.gridLayout.addWidget(self.txtNewCategory, 1, 1, 1, 2)
        self.cbCategories = QtWidgets.QComboBox(self.groupBox)
        self.cbCategories.setObjectName("cbCategories")
        self.gridLayout.addWidget(self.cbCategories, 0, 1, 1, 2)
        self.rbNew = QtWidgets.QRadioButton(self.groupBox)
        self.rbNew.setObjectName("rbNew")
        self.gridLayout.addWidget(self.rbNew, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(208, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.cmdAdd = QtWidgets.QPushButton(self.groupBox)
        self.cmdAdd.setObjectName("cmdAdd")
        self.gridLayout.addWidget(self.cmdAdd, 2, 2, 1, 1)
        self.cbCategories.raise_()
        self.txtNewCategory.raise_()
        self.cmdAdd.raise_()
        self.rbNew.raise_()
        self.rbExisting.raise_()
        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmdRemove = QtWidgets.QPushButton(ChangeCategoryUI)
        self.cmdRemove.setObjectName("cmdRemove")
        self.horizontalLayout.addWidget(self.cmdRemove)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QtWidgets.QPushButton(ChangeCategoryUI)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(ChangeCategoryUI)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(ChangeCategoryUI)
        QtCore.QMetaObject.connectSlotsByName(ChangeCategoryUI)

    def retranslateUi(self, ChangeCategoryUI):
        _translate = QtCore.QCoreApplication.translate
        ChangeCategoryUI.setWindowTitle(_translate("ChangeCategoryUI", "Change Category:"))
        self.lblTitle.setText(_translate("ChangeCategoryUI", "Current categories for "))
        self.groupBox.setTitle(_translate("ChangeCategoryUI", "Add Category"))
        self.rbExisting.setText(_translate("ChangeCategoryUI", "Choose existing"))
        self.rbNew.setText(_translate("ChangeCategoryUI", "Create new"))
        self.cmdAdd.setText(_translate("ChangeCategoryUI", "Add"))
        self.cmdRemove.setText(_translate("ChangeCategoryUI", "Remove"))
        self.cmdOK.setText(_translate("ChangeCategoryUI", "OK"))
        self.cmdCancel.setText(_translate("ChangeCategoryUI", "Cancel"))

