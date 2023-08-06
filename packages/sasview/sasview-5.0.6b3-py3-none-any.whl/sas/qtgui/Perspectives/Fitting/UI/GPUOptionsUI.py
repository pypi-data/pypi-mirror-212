# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Perspectives\Fitting\UI\GPUOptionsUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GPUOptions(object):
    def setupUi(self, GPUOptions):
        GPUOptions.setObjectName("GPUOptions")
        GPUOptions.resize(505, 268)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GPUOptions.sizePolicy().hasHeightForWidth())
        GPUOptions.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../../../../Users/UI/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GPUOptions.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(GPUOptions)
        self.gridLayout.setObjectName("gridLayout")
        self.openCLCheckBoxGroup = QtWidgets.QGroupBox(GPUOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openCLCheckBoxGroup.sizePolicy().hasHeightForWidth())
        self.openCLCheckBoxGroup.setSizePolicy(sizePolicy)
        self.openCLCheckBoxGroup.setMinimumSize(QtCore.QSize(300, 150))
        self.openCLCheckBoxGroup.setObjectName("openCLCheckBoxGroup")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.openCLCheckBoxGroup)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 391, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.optionsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.optionsLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.optionsLayout.setContentsMargins(0, 0, 0, 0)
        self.optionsLayout.setObjectName("optionsLayout")
        self.gridLayout.addWidget(self.openCLCheckBoxGroup, 0, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(GPUOptions)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.okButton = QtWidgets.QPushButton(GPUOptions)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.resetButton = QtWidgets.QPushButton(GPUOptions)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout.addWidget(self.resetButton)
        self.testButton = QtWidgets.QPushButton(GPUOptions)
        self.testButton.setObjectName("testButton")
        self.horizontalLayout.addWidget(self.testButton)
        self.helpButton = QtWidgets.QPushButton(GPUOptions)
        self.helpButton.setAutoDefault(True)
        self.helpButton.setObjectName("helpButton")
        self.horizontalLayout.addWidget(self.helpButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.retranslateUi(GPUOptions)
        self.resetButton.clicked.connect(GPUOptions.reject)
        self.okButton.clicked.connect(GPUOptions.accept)
        QtCore.QMetaObject.connectSlotsByName(GPUOptions)

    def retranslateUi(self, GPUOptions):
        _translate = QtCore.QCoreApplication.translate
        GPUOptions.setWindowTitle(_translate("GPUOptions", "OpenCL Options"))
        self.openCLCheckBoxGroup.setTitle(_translate("GPUOptions", "Available OpenCL Options"))
        self.okButton.setText(_translate("GPUOptions", "OK"))
        self.resetButton.setText(_translate("GPUOptions", "Reset"))
        self.testButton.setText(_translate("GPUOptions", "Test"))
        self.helpButton.setText(_translate("GPUOptions", "Help"))

