# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chushi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_chushi(object):
    def setupUi(self, chushi):
        chushi.setObjectName("chushi")
        chushi.resize(1000, 820)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/source/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        chushi.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(chushi)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_6 = QtWidgets.QFrame(self.centralwidget)
        self.frame_6.setStyleSheet("background-color: rgb(86, 128, 172);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 36)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_23 = QtWidgets.QLabel(self.frame_7)
        self.label_23.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("隶书")
        font.setPointSize(28)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("border-radius: 10px;\n"
"border-bottom-left-radius: 0px;\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 rgba(255, 255, 255, 20%), stop:1 rgba(255, 255, 255, 0));")
        self.label_23.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_23.setIndent(10)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_4.addWidget(self.label_23)
        self.pushButton = QtWidgets.QPushButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton.setStyleSheet("border-image: url(:/source/close.svg);\n"
"background-color: rgb(29, 93, 192);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.frame_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.frame = QtWidgets.QFrame(self.frame_6)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(381, 481))
        self.frame_4.setMaximumSize(QtCore.QSize(381, 481))
        self.frame_4.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.frame_2 = QtWidgets.QFrame(self.frame_4)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 381, 481))
        self.frame_2.setMinimumSize(QtCore.QSize(381, 481))
        self.frame_2.setMaximumSize(QtCore.QSize(381, 481))
        self.frame_2.setStyleSheet("QFrame{image: url(:/svg/未标题-1.png);\n"
"\n"
"background-color: rgba(255, 255, 255, 0);}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(-10, 0, 391, 481))
        self.frame_3.setStyleSheet("QFrame{\n"
"    image: none;\n"
"background-color: rgba(255, 255, 255, 20%);\n"
"border-radius:6px \n"
"}\n"
"QLabel{\n"
"\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(24, 24, 24, 8)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 24)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.frame_10)
        self.label.setMaximumSize(QtCore.QSize(16777215, 26777))
        font = QtGui.QFont()
        font.setFamily("方正舒体")
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.verticalLayout_3.addWidget(self.frame_10)
        self.frame_9 = QtWidgets.QFrame(self.frame_3)
        self.frame_9.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.frame_9)
        self.frame_11 = QtWidgets.QFrame(self.frame_3)
        self.frame_11.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.pushButton_new = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_new.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_new.setFont(font)
        self.pushButton_new.setStyleSheet("QPushButton{\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-radius:20px ;\n"
"    color: rgb(255, 255, 255);\n"
"\n"
"\n"
"}")
        self.pushButton_new.setObjectName("pushButton_new")
        self.verticalLayout_6.addWidget(self.pushButton_new)
        self.pushButton_new_2 = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_new_2.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_new_2.setFont(font)
        self.pushButton_new_2.setStyleSheet("QPushButton{\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-radius:20px ;\n"
"    color: rgb(255, 255, 255);\n"
"\n"
"\n"
"}")
        self.pushButton_new_2.setObjectName("pushButton_new_2")
        self.verticalLayout_6.addWidget(self.pushButton_new_2)
        self.pushButton_read = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_read.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_read.setFont(font)
        self.pushButton_read.setStyleSheet("QPushButton{\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-radius:20px ;\n"
"    color: rgb(255, 255, 255);\n"
"\n"
"\n"
"}")
        self.pushButton_read.setObjectName("pushButton_read")
        self.verticalLayout_6.addWidget(self.pushButton_read)
        self.pushButton_open = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_open.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_open.setFont(font)
        self.pushButton_open.setStyleSheet("QPushButton{\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-radius:20px ;\n"
"    color: rgb(255, 255, 255);\n"
"\n"
"\n"
"}")
        self.pushButton_open.setObjectName("pushButton_open")
        self.verticalLayout_6.addWidget(self.pushButton_open)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.frame_11)
        self.horizontalLayout_2.addWidget(self.frame_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.widget_8 = QtWidgets.QWidget(self.frame)
        self.widget_8.setMinimumSize(QtCore.QSize(550, 250))
        self.widget_8.setStyleSheet("border-image: url(:/source/leaf.png);")
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_2.addWidget(self.widget_8)
        self.verticalLayout.addWidget(self.frame)
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(24)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(24)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_12 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_12.setStyleSheet("border-image: url(:/source/xh.png);")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_3.addWidget(self.frame_12)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.frame_5)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout.addLayout(self.verticalLayout_9)
        self.horizontalLayout.addWidget(self.frame_6)
        chushi.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(chushi)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        chushi.setMenuBar(self.menubar)

        self.retranslateUi(chushi)
        QtCore.QMetaObject.connectSlotsByName(chushi)

    def retranslateUi(self, chushi):
        _translate = QtCore.QCoreApplication.translate
        chushi.setWindowTitle(_translate("chushi", "HTDO V1.0"))
        self.label_23.setText(_translate("chushi", "高效透平设计及优化系统"))
        self.label.setText(_translate("chushi", "WELCOME"))
        self.pushButton_new.setText(_translate("chushi", "分析及优化"))
        self.pushButton_new_2.setText(_translate("chushi", "设计及优化"))
        self.pushButton_read.setText(_translate("chushi", "读取现有文件"))
        self.pushButton_open.setText(_translate("chushi", "显示内置模板"))
        self.label_5.setText(_translate("chushi", "2023.4"))
        self.label_4.setText(_translate("chushi", "西安交通大学叶轮机械研究所"))
import ui.source.pic_rc
