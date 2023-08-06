# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\MainWindow\UI\ChangeNameUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangeCategoryUI(object):
    def setupUi(self, ChangeCategoryUI):
        ChangeCategoryUI.setObjectName("ChangeCategoryUI")
        ChangeCategoryUI.resize(341, 295)
        ChangeCategoryUI.setMinimumSize(QtCore.QSize(341, 295))
        self.groupBox = QtWidgets.QGroupBox(ChangeCategoryUI)
        self.groupBox.setGeometry(QtCore.QRect(11, 11, 321, 211))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.rbDataName = QtWidgets.QRadioButton(self.groupBox)
        self.rbDataName.setObjectName("rbDataName")
        self.gridLayout.addWidget(self.rbDataName, 1, 0, 1, 1)
        self.txtFileName = QtWidgets.QLineEdit(self.groupBox)
        self.txtFileName.setObjectName("txtFileName")
        self.gridLayout.addWidget(self.txtFileName, 2, 2, 1, 1)
        self.txtCurrentName = QtWidgets.QLineEdit(self.groupBox)
        self.txtCurrentName.setObjectName("txtCurrentName")
        self.gridLayout.addWidget(self.txtCurrentName, 0, 2, 1, 1)
        self.txtDataName = QtWidgets.QLineEdit(self.groupBox)
        self.txtDataName.setObjectName("txtDataName")
        self.gridLayout.addWidget(self.txtDataName, 1, 2, 1, 1)
        self.rbExisting = QtWidgets.QRadioButton(self.groupBox)
        self.rbExisting.setObjectName("rbExisting")
        self.gridLayout.addWidget(self.rbExisting, 0, 0, 1, 1)
        self.txtNewCategory = QtWidgets.QLineEdit(self.groupBox)
        self.txtNewCategory.setObjectName("txtNewCategory")
        self.gridLayout.addWidget(self.txtNewCategory, 3, 2, 1, 1)
        self.rbFileName = QtWidgets.QRadioButton(self.groupBox)
        self.rbFileName.setObjectName("rbFileName")
        self.gridLayout.addWidget(self.rbFileName, 2, 0, 1, 1)
        self.rbNew = QtWidgets.QRadioButton(self.groupBox)
        self.rbNew.setObjectName("rbNew")
        self.gridLayout.addWidget(self.rbNew, 3, 0, 1, 1)
        self.txtNewCategory.raise_()
        self.rbNew.raise_()
        self.rbExisting.raise_()
        self.txtCurrentName.raise_()
        self.rbDataName.raise_()
        self.rbFileName.raise_()
        self.txtDataName.raise_()
        self.txtFileName.raise_()
        self.horizontalLayoutWidget = QtWidgets.QWidget(ChangeCategoryUI)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 321, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cmdOK = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout_2.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout_2.addWidget(self.cmdCancel)

        self.retranslateUi(ChangeCategoryUI)
        QtCore.QMetaObject.connectSlotsByName(ChangeCategoryUI)

    def retranslateUi(self, ChangeCategoryUI):
        _translate = QtCore.QCoreApplication.translate
        ChangeCategoryUI.setWindowTitle(_translate("ChangeCategoryUI", "Change Category:"))
        self.groupBox.setTitle(_translate("ChangeCategoryUI", "Change Display Name"))
        self.rbDataName.setText(_translate("ChangeCategoryUI", "Data name"))
        self.rbExisting.setText(_translate("ChangeCategoryUI", "Current name"))
        self.rbFileName.setText(_translate("ChangeCategoryUI", "File name"))
        self.rbNew.setText(_translate("ChangeCategoryUI", "Create new"))
        self.cmdOK.setText(_translate("ChangeCategoryUI", "OK"))
        self.cmdCancel.setText(_translate("ChangeCategoryUI", "Cancel"))

