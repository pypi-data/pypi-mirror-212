# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\MainWindow\UI\AcknowledgementsUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Acknowledgements(object):
    def setupUi(self, Acknowledgements):
        Acknowledgements.setObjectName("Acknowledgements")
        Acknowledgements.setWindowModality(QtCore.Qt.ApplicationModal)
        Acknowledgements.resize(468, 316)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Acknowledgements.sizePolicy().hasHeightForWidth())
        Acknowledgements.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Acknowledgements)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Acknowledgements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Acknowledgements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 85))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 85))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Acknowledgements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(Acknowledgements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy)
        self.textBrowser_2.setMaximumSize(QtCore.QSize(16777215, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Acknowledgements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)

        self.retranslateUi(Acknowledgements)
        QtCore.QMetaObject.connectSlotsByName(Acknowledgements)

    def retranslateUi(self, Acknowledgements):
        _translate = QtCore.QCoreApplication.translate
        Acknowledgements.setWindowTitle(_translate("Acknowledgements", "Acknowledging SasView"))
        self.label.setText(_translate("Acknowledgements", "<html><head/><body><p>To ensure the long term support and development of this software please remember to:</p><p>(1) Acknowledge its use in your publications as:<br/></p><p><br/></p></body></html>"))
        self.textBrowser.setHtml(_translate("Acknowledgements", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">This work benefited from the use of the SasView application, originally developed under NSF Award DMR-0520547. SasView also contains code developed with funding from the EU Horizon 2020 programme under the SINE2020 project Grant No 654000.</span></p></body></html>"))
        self.label_2.setText(_translate("Acknowledgements", "<html><head/><body><p>(2) Reference SasView as:</p><p><br/></p><p><br/></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("Acknowledgements", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">M. Doucet et al. SasView Version 5.0.3, Zenodo, 10.5281/zenodo.3930098</span></p></body></html>"))
        self.label_3.setText(_translate("Acknowledgements", "<html><head/><body><p>(3) Reference the model you used if appropriate (see documentation for refs)</p><p>(4) Send us your reference for our records: developers@sasview.org</p></body></html>"))

