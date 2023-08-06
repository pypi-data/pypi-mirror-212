# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Plotting\UI\PlotPropertiesUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotPropertiesUI(object):
    def setupUi(self, PlotPropertiesUI):
        PlotPropertiesUI.setObjectName("PlotPropertiesUI")
        PlotPropertiesUI.resize(319, 285)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PlotPropertiesUI.sizePolicy().hasHeightForWidth())
        PlotPropertiesUI.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlotPropertiesUI.setWindowIcon(icon)
        self.gridLayout_3 = QtWidgets.QGridLayout(PlotPropertiesUI)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(PlotPropertiesUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.cbShape = QtWidgets.QComboBox(self.groupBox)
        self.cbShape.setObjectName("cbShape")
        self.gridLayout.addWidget(self.cbShape, 0, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.sbSize = QtWidgets.QSpinBox(self.groupBox)
        self.sbSize.setMinimum(1)
        self.sbSize.setMaximum(72)
        self.sbSize.setObjectName("sbSize")
        self.gridLayout.addWidget(self.sbSize, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.cbColor = QtWidgets.QComboBox(self.groupBox)
        self.cbColor.setObjectName("cbColor")
        self.gridLayout.addWidget(self.cbColor, 1, 1, 1, 1)
        self.cmdCustom = QtWidgets.QPushButton(self.groupBox)
        self.cmdCustom.setObjectName("cmdCustom")
        self.gridLayout.addWidget(self.cmdCustom, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(PlotPropertiesUI)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtLegend = QtWidgets.QLineEdit(PlotPropertiesUI)
        self.txtLegend.setObjectName("txtLegend")
        self.horizontalLayout.addWidget(self.txtLegend)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(PlotPropertiesUI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(PlotPropertiesUI)
        self.buttonBox.accepted.connect(PlotPropertiesUI.accept)
        self.buttonBox.rejected.connect(PlotPropertiesUI.reject)
        QtCore.QMetaObject.connectSlotsByName(PlotPropertiesUI)

    def retranslateUi(self, PlotPropertiesUI):
        _translate = QtCore.QCoreApplication.translate
        PlotPropertiesUI.setWindowTitle(_translate("PlotPropertiesUI", "Modify Plot Properties"))
        self.groupBox.setTitle(_translate("PlotPropertiesUI", "Symbol"))
        self.label_2.setText(_translate("PlotPropertiesUI", "Shape"))
        self.label_4.setText(_translate("PlotPropertiesUI", "Size"))
        self.label_3.setText(_translate("PlotPropertiesUI", "Color"))
        self.cmdCustom.setText(_translate("PlotPropertiesUI", "Custom.."))
        self.label.setText(_translate("PlotPropertiesUI", "Legend Label"))

