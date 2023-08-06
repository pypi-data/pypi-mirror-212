# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\ImageViewerOptionsUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageViewerOptionsUI(object):
    def setupUi(self, ImageViewerOptionsUI):
        ImageViewerOptionsUI.setObjectName("ImageViewerOptionsUI")
        ImageViewerOptionsUI.resize(454, 246)
        self.gridLayout_4 = QtWidgets.QGridLayout(ImageViewerOptionsUI)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(ImageViewerOptionsUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.txtXmin = QtWidgets.QLineEdit(self.groupBox)
        self.txtXmin.setObjectName("txtXmin")
        self.gridLayout.addWidget(self.txtXmin, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        self.txtYmin = QtWidgets.QLineEdit(self.groupBox)
        self.txtYmin.setObjectName("txtYmin")
        self.gridLayout.addWidget(self.txtYmin, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 1, 1, 1)
        self.txtZmax = QtWidgets.QLineEdit(self.groupBox)
        self.txtZmax.setObjectName("txtZmax")
        self.gridLayout.addWidget(self.txtZmax, 2, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txtXmax = QtWidgets.QLineEdit(self.groupBox)
        self.txtXmax.setObjectName("txtXmax")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtXmax)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txtYmax = QtWidgets.QLineEdit(self.groupBox)
        self.txtYmax.setObjectName("txtYmax")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtYmax)
        self.gridLayout_2.addLayout(self.formLayout_2, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(ImageViewerOptionsUI)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_4.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImageViewerOptionsUI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.groupBox.raise_()
        self.buttonBox.raise_()
        self.textBrowser.raise_()

        self.retranslateUi(ImageViewerOptionsUI)
        self.buttonBox.accepted.connect(ImageViewerOptionsUI.accept)
        self.buttonBox.rejected.connect(ImageViewerOptionsUI.reject)
        QtCore.QMetaObject.connectSlotsByName(ImageViewerOptionsUI)

    def retranslateUi(self, ImageViewerOptionsUI):
        _translate = QtCore.QCoreApplication.translate
        ImageViewerOptionsUI.setWindowTitle(_translate("ImageViewerOptionsUI", "Image Conversion Options"))
        self.groupBox.setTitle(_translate("ImageViewerOptionsUI", "GroupBox"))
        self.label.setText(_translate("ImageViewerOptionsUI", "x values from pixel # to:"))
        self.label_6.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>X<span style=\" vertical-align:sub;\">min</span></p></body></html>"))
        self.label_2.setText(_translate("ImageViewerOptionsUI", "y values from pixel # to:"))
        self.label_7.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>Y<span style=\" vertical-align:sub;\">min</span></p></body></html>"))
        self.label_3.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>z value range</p></body></html>"))
        self.label_8.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>From 0 to:</p></body></html>"))
        self.label_4.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>X<span style=\" vertical-align:sub;\">max</span></p></body></html>"))
        self.label_5.setText(_translate("ImageViewerOptionsUI", "<html><head/><body><p>Y<span style=\" vertical-align:sub;\">max</span></p></body></html>"))
        self.textBrowser.setHtml(_translate("ImageViewerOptionsUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Note</span><span style=\" font-size:8pt;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Recommend to use an image with 8 bit Grey scale (and with No. of pixels &lt; 300 x 300).</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Otherwise, z = 0.299R + 0.587G + 0.114B.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))

