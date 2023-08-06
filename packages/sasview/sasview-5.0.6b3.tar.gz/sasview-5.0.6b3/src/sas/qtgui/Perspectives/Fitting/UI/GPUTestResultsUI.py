# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Perspectives\Fitting\UI\GPUTestResultsUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GPUTestResults(object):
    def setupUi(self, GPUTestResults):
        GPUTestResults.setObjectName("GPUTestResults")
        GPUTestResults.resize(487, 532)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../UI/res/ball.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GPUTestResults.setWindowIcon(icon)
        self.gridLayout_3 = QtWidgets.QGridLayout(GPUTestResults)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TestResultsBox = QtWidgets.QGroupBox(GPUTestResults)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TestResultsBox.sizePolicy().hasHeightForWidth())
        self.TestResultsBox.setSizePolicy(sizePolicy)
        self.TestResultsBox.setObjectName("TestResultsBox")
        self.gridLayout = QtWidgets.QGridLayout(self.TestResultsBox)
        self.gridLayout.setObjectName("gridLayout")
        self.resultsText = QtWidgets.QTextEdit(self.TestResultsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultsText.sizePolicy().hasHeightForWidth())
        self.resultsText.setSizePolicy(sizePolicy)
        self.resultsText.setMinimumSize(QtCore.QSize(300, 300))
        self.resultsText.setReadOnly(True)
        self.resultsText.setObjectName("resultsText")
        self.gridLayout.addWidget(self.resultsText, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.TestResultsBox, 0, 0, 1, 1)
        self.falingTestsNoOpenCL = QtWidgets.QLabel(GPUTestResults)
        self.falingTestsNoOpenCL.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.falingTestsNoOpenCL.setObjectName("falingTestsNoOpenCL")
        self.gridLayout_2.addWidget(self.falingTestsNoOpenCL, 1, 0, 1, 1)
        self.howToReportIssues = QtWidgets.QLabel(GPUTestResults)
        self.howToReportIssues.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.howToReportIssues.setWordWrap(True)
        self.howToReportIssues.setObjectName("howToReportIssues")
        self.gridLayout_2.addWidget(self.howToReportIssues, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtWidgets.QDialogButtonBox(GPUTestResults)
        self.okButton.setOrientation(QtCore.Qt.Horizontal)
        self.okButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.okButton.setCenterButtons(False)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(GPUTestResults)
        self.okButton.accepted.connect(GPUTestResults.accept)
        self.okButton.rejected.connect(GPUTestResults.reject)
        QtCore.QMetaObject.connectSlotsByName(GPUTestResults)

    def retranslateUi(self, GPUTestResults):
        _translate = QtCore.QCoreApplication.translate
        GPUTestResults.setWindowTitle(_translate("GPUTestResults", "OpenCL Test Results"))
        self.TestResultsBox.setTitle(_translate("GPUTestResults", "OpenCL test results"))
        self.falingTestsNoOpenCL.setText(_translate("GPUTestResults", "If tests fail on OpenCL devices, please select the No OpenCL option."))
        self.howToReportIssues.setText(_translate("GPUTestResults", "In the case where many tests are failing, please consider sending the above report to help@sasview.org."))

