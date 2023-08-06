# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Plotting\UI\SetGraphRangeUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_setGraphRangeUI(object):
    def setupUi(self, setGraphRangeUI):
        setGraphRangeUI.setObjectName("setGraphRangeUI")
        setGraphRangeUI.resize(358, 144)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(setGraphRangeUI.sizePolicy().hasHeightForWidth())
        setGraphRangeUI.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        setGraphRangeUI.setWindowIcon(icon)
        setGraphRangeUI.setModal(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(setGraphRangeUI)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(setGraphRangeUI)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtXmin = QtWidgets.QLineEdit(setGraphRangeUI)
        self.txtXmin.setObjectName("txtXmin")
        self.gridLayout.addWidget(self.txtXmin, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(setGraphRangeUI)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.txtXmax = QtWidgets.QLineEdit(setGraphRangeUI)
        self.txtXmax.setObjectName("txtXmax")
        self.gridLayout.addWidget(self.txtXmax, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(setGraphRangeUI)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtYmin = QtWidgets.QLineEdit(setGraphRangeUI)
        self.txtYmin.setObjectName("txtYmin")
        self.gridLayout.addWidget(self.txtYmin, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(setGraphRangeUI)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.txtYmax = QtWidgets.QLineEdit(setGraphRangeUI)
        self.txtYmax.setObjectName("txtYmax")
        self.gridLayout.addWidget(self.txtYmax, 1, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(setGraphRangeUI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(setGraphRangeUI)
        self.buttonBox.accepted.connect(setGraphRangeUI.accept)
        self.buttonBox.rejected.connect(setGraphRangeUI.reject)
        QtCore.QMetaObject.connectSlotsByName(setGraphRangeUI)

    def retranslateUi(self, setGraphRangeUI):
        _translate = QtCore.QCoreApplication.translate
        setGraphRangeUI.setWindowTitle(_translate("setGraphRangeUI", "Set Graph Range"))
        self.label.setText(_translate("setGraphRangeUI", "X min"))
        self.label_2.setText(_translate("setGraphRangeUI", "X max"))
        self.label_3.setText(_translate("setGraphRangeUI", "Y min"))
        self.label_4.setText(_translate("setGraphRangeUI", "Y max"))

