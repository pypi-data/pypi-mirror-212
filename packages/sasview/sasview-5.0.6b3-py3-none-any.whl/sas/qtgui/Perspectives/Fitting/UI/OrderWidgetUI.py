# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Perspectives\Fitting\UI\OrderWidgetUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OrderWidgetUI(object):
    def setupUi(self, OrderWidgetUI):
        OrderWidgetUI.setObjectName("OrderWidgetUI")
        OrderWidgetUI.resize(511, 417)
        self.gridLayout_2 = QtWidgets.QGridLayout(OrderWidgetUI)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(OrderWidgetUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lstOrder = QtWidgets.QListWidget(self.groupBox)
        self.lstOrder.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstOrder.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lstOrder.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.lstOrder.setAlternatingRowColors(True)
        self.lstOrder.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstOrder.setObjectName("lstOrder")
        self.gridLayout.addWidget(self.lstOrder, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(OrderWidgetUI)
        QtCore.QMetaObject.connectSlotsByName(OrderWidgetUI)

    def retranslateUi(self, OrderWidgetUI):
        _translate = QtCore.QCoreApplication.translate
        OrderWidgetUI.setWindowTitle(_translate("OrderWidgetUI", "Dataset Ordering"))
        self.groupBox.setTitle(_translate("OrderWidgetUI", "Data Order"))
        self.label.setText(_translate("OrderWidgetUI", "<html><head/><body><p>Drag and move items to define the order of fitting.</p></body></html>"))

