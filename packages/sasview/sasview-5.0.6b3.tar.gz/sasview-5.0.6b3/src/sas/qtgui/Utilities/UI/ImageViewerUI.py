# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\sas\qtgui\Utilities\UI\ImageViewerUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageViewerUI(object):
    def setupUi(self, ImageViewerUI):
        ImageViewerUI.setObjectName("ImageViewerUI")
        ImageViewerUI.resize(492, 418)
        self.centralwidget = QtWidgets.QWidget(ImageViewerUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.imgFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imgFrame.sizePolicy().hasHeightForWidth())
        self.imgFrame.setSizePolicy(sizePolicy)
        self.imgFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgFrame.setObjectName("imgFrame")
        self.gridLayout.addWidget(self.imgFrame, 0, 0, 1, 1)
        ImageViewerUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ImageViewerUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 492, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuImage = QtWidgets.QMenu(self.menubar)
        self.menuImage.setObjectName("menuImage")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.menuHelp.setObjectName("menuHelp")
        ImageViewerUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ImageViewerUI)
        self.statusbar.setObjectName("statusbar")
        ImageViewerUI.setStatusBar(self.statusbar)
        self.actionLoad_Image = QtWidgets.QAction(ImageViewerUI)
        self.actionLoad_Image.setObjectName("actionLoad_Image")
        self.actionSave_Image = QtWidgets.QAction(ImageViewerUI)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionPrint_Image = QtWidgets.QAction(ImageViewerUI)
        self.actionPrint_Image.setObjectName("actionPrint_Image")
        self.actionCopy_Image = QtWidgets.QAction(ImageViewerUI)
        self.actionCopy_Image.setObjectName("actionCopy_Image")
        self.actionConvert_to_Data = QtWidgets.QAction(ImageViewerUI)
        self.actionConvert_to_Data.setObjectName("actionConvert_to_Data")
        self.actionHow_To = QtWidgets.QAction(ImageViewerUI)
        self.actionHow_To.setObjectName("actionHow_To")
        self.menuFile.addAction(self.actionLoad_Image)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionPrint_Image)
        self.menuEdit.addAction(self.actionCopy_Image)
        self.menuImage.addAction(self.actionConvert_to_Data)
        self.menuHelp.addAction(self.actionHow_To)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(ImageViewerUI)
        QtCore.QMetaObject.connectSlotsByName(ImageViewerUI)

    def retranslateUi(self, ImageViewerUI):
        _translate = QtCore.QCoreApplication.translate
        ImageViewerUI.setWindowTitle(_translate("ImageViewerUI", "Image Viewer"))
        self.menuFile.setTitle(_translate("ImageViewerUI", "File"))
        self.menuEdit.setTitle(_translate("ImageViewerUI", "Edit"))
        self.menuImage.setTitle(_translate("ImageViewerUI", "Image"))
        self.menuHelp.setTitle(_translate("ImageViewerUI", "Help"))
        self.actionLoad_Image.setText(_translate("ImageViewerUI", "Load Image"))
        self.actionSave_Image.setText(_translate("ImageViewerUI", "Save Image"))
        self.actionPrint_Image.setText(_translate("ImageViewerUI", "Print Image"))
        self.actionCopy_Image.setText(_translate("ImageViewerUI", "Copy"))
        self.actionConvert_to_Data.setText(_translate("ImageViewerUI", "Convert to Data"))
        self.actionHow_To.setText(_translate("ImageViewerUI", "How To"))

