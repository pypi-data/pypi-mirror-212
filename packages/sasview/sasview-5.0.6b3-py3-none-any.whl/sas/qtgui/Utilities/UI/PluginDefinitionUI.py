# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\PluginDefinitionUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PluginDefinition(object):
    def setupUi(self, PluginDefinition):
        PluginDefinition.setObjectName("PluginDefinition")
        PluginDefinition.resize(723, 784)
        self.gridLayout_7 = QtWidgets.QGridLayout(PluginDefinition)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_6 = QtWidgets.QGroupBox(PluginDefinition)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.txtName = QtWidgets.QLineEdit(self.groupBox_6)
        self.txtName.setObjectName("txtName")
        self.gridLayout_5.addWidget(self.txtName, 0, 0, 1, 1)
        self.chkOverwrite = QtWidgets.QCheckBox(self.groupBox_6)
        self.chkOverwrite.setObjectName("chkOverwrite")
        self.gridLayout_5.addWidget(self.chkOverwrite, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(PluginDefinition)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.txtDescription = QtWidgets.QLineEdit(self.groupBox_5)
        self.txtDescription.setObjectName("txtDescription")
        self.gridLayout_4.addWidget(self.txtDescription, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_5, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(PluginDefinition)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.tblParams = QtWidgets.QTableWidget(self.groupBox_3)
        self.tblParams.setObjectName("tblParams")
        self.tblParams.setColumnCount(2)
        self.tblParams.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tblParams.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParams.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParams.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tblParams, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tblParamsPD = QtWidgets.QTableWidget(self.groupBox_4)
        self.tblParamsPD.setObjectName("tblParamsPD")
        self.tblParamsPD.setColumnCount(2)
        self.tblParamsPD.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tblParamsPD.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParamsPD.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblParamsPD.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tblParamsPD, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_4, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(PluginDefinition)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.txtFunction = QtWidgets.QTextBrowser(self.groupBox_2)
        self.txtFunction.setReadOnly(False)
        self.txtFunction.setObjectName("txtFunction")
        self.gridLayout_6.addWidget(self.txtFunction, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_2, 3, 0, 1, 1)

        self.retranslateUi(PluginDefinition)
        QtCore.QMetaObject.connectSlotsByName(PluginDefinition)

    def retranslateUi(self, PluginDefinition):
        _translate = QtCore.QCoreApplication.translate
        PluginDefinition.setWindowTitle(_translate("PluginDefinition", "Plugin Definition"))
        self.groupBox_6.setTitle(_translate("PluginDefinition", "Plugin name"))
        self.txtName.setPlaceholderText(_translate("PluginDefinition", "Enter a plugin name"))
        self.chkOverwrite.setText(_translate("PluginDefinition", "Overwrite existing plugin model of this name"))
        self.groupBox_5.setTitle(_translate("PluginDefinition", "Description"))
        self.txtDescription.setPlaceholderText(_translate("PluginDefinition", "Enter a description of the model"))
        self.groupBox.setTitle(_translate("PluginDefinition", "Fit parameters"))
        self.groupBox_3.setTitle(_translate("PluginDefinition", "Non-polydisperse"))
        item = self.tblParams.horizontalHeaderItem(0)
        item.setText(_translate("PluginDefinition", "Parameters"))
        item = self.tblParams.horizontalHeaderItem(1)
        item.setText(_translate("PluginDefinition", "Initial\n"
"value"))
        self.groupBox_4.setTitle(_translate("PluginDefinition", "Polydisperse"))
        item = self.tblParamsPD.horizontalHeaderItem(0)
        item.setText(_translate("PluginDefinition", "Parameters"))
        item = self.tblParamsPD.horizontalHeaderItem(1)
        item.setText(_translate("PluginDefinition", "Initial\n"
"value"))
        self.groupBox_2.setTitle(_translate("PluginDefinition", "Function(x)"))
        self.txtFunction.setHtml(_translate("PluginDefinition", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

