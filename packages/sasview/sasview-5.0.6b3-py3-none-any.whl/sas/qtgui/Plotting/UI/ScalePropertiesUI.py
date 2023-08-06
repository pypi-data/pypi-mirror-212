# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Plotting\UI\ScalePropertiesUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_scalePropertiesUI(object):
    def setupUi(self, scalePropertiesUI):
        scalePropertiesUI.setObjectName("scalePropertiesUI")
        scalePropertiesUI.resize(400, 137)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(scalePropertiesUI.sizePolicy().hasHeightForWidth())
        scalePropertiesUI.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        scalePropertiesUI.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(scalePropertiesUI)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(scalePropertiesUI)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(scalePropertiesUI)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(scalePropertiesUI)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.cbX = QtWidgets.QComboBox(scalePropertiesUI)
        self.cbX.setObjectName("cbX")
        self.gridLayout.addWidget(self.cbX, 1, 0, 1, 1)
        self.cbY = QtWidgets.QComboBox(scalePropertiesUI)
        self.cbY.setObjectName("cbY")
        self.gridLayout.addWidget(self.cbY, 1, 1, 1, 1)
        self.cbView = QtWidgets.QComboBox(scalePropertiesUI)
        self.cbView.setObjectName("cbView")
        self.gridLayout.addWidget(self.cbView, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(scalePropertiesUI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(scalePropertiesUI)
        self.buttonBox.accepted.connect(scalePropertiesUI.accept)
        self.buttonBox.rejected.connect(scalePropertiesUI.reject)
        QtCore.QMetaObject.connectSlotsByName(scalePropertiesUI)

    def retranslateUi(self, scalePropertiesUI):
        _translate = QtCore.QCoreApplication.translate
        scalePropertiesUI.setWindowTitle(_translate("scalePropertiesUI", "Scale Properties"))
        self.label.setText(_translate("scalePropertiesUI", "X"))
        self.label_2.setText(_translate("scalePropertiesUI", "Y"))
        self.label_3.setText(_translate("scalePropertiesUI", "View"))

