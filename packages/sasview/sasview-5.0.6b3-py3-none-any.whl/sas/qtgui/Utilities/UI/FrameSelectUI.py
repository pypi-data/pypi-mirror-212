# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\FrameSelectUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameSelect(object):
    def setupUi(self, FrameSelect):
        FrameSelect.setObjectName("FrameSelect")
        FrameSelect.setWindowModality(QtCore.Qt.WindowModal)
        FrameSelect.resize(278, 173)
        self.gridLayout_3 = QtWidgets.QGridLayout(FrameSelect)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblDescription = QtWidgets.QLabel(FrameSelect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDescription.sizePolicy().hasHeightForWidth())
        self.lblDescription.setSizePolicy(sizePolicy)
        self.lblDescription.setObjectName("lblDescription")
        self.gridLayout_2.addWidget(self.lblDescription, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(FrameSelect)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.txtFirstFrame = QtWidgets.QLineEdit(FrameSelect)
        self.txtFirstFrame.setObjectName("txtFirstFrame")
        self.gridLayout.addWidget(self.txtFirstFrame, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(FrameSelect)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtLastFrame = QtWidgets.QLineEdit(FrameSelect)
        self.txtLastFrame.setObjectName("txtLastFrame")
        self.gridLayout.addWidget(self.txtLastFrame, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(FrameSelect)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.txtIncrement = QtWidgets.QLineEdit(FrameSelect)
        self.txtIncrement.setObjectName("txtIncrement")
        self.gridLayout.addWidget(self.txtIncrement, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.chkSeparateFiles = QtWidgets.QCheckBox(FrameSelect)
        self.chkSeparateFiles.setObjectName("chkSeparateFiles")
        self.gridLayout_2.addWidget(self.chkSeparateFiles, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QtWidgets.QPushButton(FrameSelect)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(FrameSelect)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(FrameSelect)
        QtCore.QMetaObject.connectSlotsByName(FrameSelect)

    def retranslateUi(self, FrameSelect):
        _translate = QtCore.QCoreApplication.translate
        FrameSelect.setWindowTitle(_translate("FrameSelect", "Frame Select"))
        self.lblDescription.setText(_translate("FrameSelect", "text"))
        self.label_2.setText(_translate("FrameSelect", "First frame:"))
        self.label_3.setText(_translate("FrameSelect", "Last frame:"))
        self.label_4.setText(_translate("FrameSelect", "Increment:"))
        self.chkSeparateFiles.setText(_translate("FrameSelect", "Export each frame to separate file"))
        self.cmdOK.setText(_translate("FrameSelect", "OK"))
        self.cmdCancel.setText(_translate("FrameSelect", "Cancel"))

