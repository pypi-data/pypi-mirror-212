# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\MainWindow\UI\WelcomePanelUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WelcomePanelUI(object):
    def setupUi(self, WelcomePanelUI):
        WelcomePanelUI.setObjectName("WelcomePanelUI")
        WelcomePanelUI.resize(658, 737)
        self.gridLayout = QtWidgets.QGridLayout(WelcomePanelUI)
        self.gridLayout.setObjectName("gridLayout")
        self.imgSasView = QtWidgets.QLabel(WelcomePanelUI)
        self.imgSasView.setText("")
        self.imgSasView.setPixmap(QtGui.QPixmap(":/res/SVwelcome.png"))
        self.imgSasView.setAlignment(QtCore.Qt.AlignCenter)
        self.imgSasView.setObjectName("imgSasView")
        self.gridLayout.addWidget(self.imgSasView, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(WelcomePanelUI)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.lblAcknowledgements = QtWidgets.QLabel(WelcomePanelUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAcknowledgements.sizePolicy().hasHeightForWidth())
        self.lblAcknowledgements.setSizePolicy(sizePolicy)
        self.lblAcknowledgements.setWordWrap(True)
        self.lblAcknowledgements.setObjectName("lblAcknowledgements")
        self.gridLayout.addWidget(self.lblAcknowledgements, 2, 0, 1, 1)
        self.lblVersion = QtWidgets.QLabel(WelcomePanelUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblVersion.sizePolicy().hasHeightForWidth())
        self.lblVersion.setSizePolicy(sizePolicy)
        self.lblVersion.setObjectName("lblVersion")
        self.gridLayout.addWidget(self.lblVersion, 3, 0, 1, 1)
        self.lblLink = QtWidgets.QLabel(WelcomePanelUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLink.sizePolicy().hasHeightForWidth())
        self.lblLink.setSizePolicy(sizePolicy)
        self.lblLink.setOpenExternalLinks(True)
        self.lblLink.setObjectName("lblLink")
        self.gridLayout.addWidget(self.lblLink, 4, 0, 1, 1)

        self.retranslateUi(WelcomePanelUI)
        QtCore.QMetaObject.connectSlotsByName(WelcomePanelUI)

    def retranslateUi(self, WelcomePanelUI):
        _translate = QtCore.QCoreApplication.translate
        WelcomePanelUI.setWindowTitle(_translate("WelcomePanelUI", "Dialog"))
        self.lblAcknowledgements.setText(_translate("WelcomePanelUI", "This work originally developed as part of the DANSE project funded by the NSF under grant DMR-0520547, and currently maintained by UTK, UMD, ESS, NIST, ORNL, ISIS, ILL, DLS, TUD, BAM and ANSTO."))
        self.lblVersion.setText(_translate("WelcomePanelUI", "<html><head/><body><p>SasView 4.0.0-Alpha<br/>Build: 1<br/>(c) 2009 - 2017, UTK, UMD, NIST, ORNL, ISIS, ESS, ILL and ANSTO</p><p><br/></p></body></html>"))
        self.lblLink.setText(_translate("WelcomePanelUI", "<html><head/><body><p>Comments? Bugs? Requests?</p>\n"
"<p>Send us a ticket at: <a href=\"mailto:help@sasview.org\"><span style=\" text-decoration: underline; color:#0000ff;\"> help@sasview.org</span></a></p></body></html>"))

