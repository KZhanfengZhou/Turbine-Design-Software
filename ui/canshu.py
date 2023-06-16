from ui.canshu_designed import Ui_canshu
from PyQt5 import QtWidgets
import matplotlib
from PyQt5 import QtCore

matplotlib.use('Qt5Agg')


class canshu(QtWidgets.QMainWindow, Ui_canshu):
    returnResultSignal = QtCore.pyqtSignal(list)

    def __init__(self, z, zr, opt):
        super().__init__()
        self.setupUi(self)
        self.widget1.setVisible(False)
        self.widget2.setVisible(False)
        self.pushButton_yiwei.clicked.connect(self.switch1)
        self.pushButton_jingxiang.clicked.connect(self.switch2)
        self.pushButton_yepian.clicked.connect(self.switch3)
        self.pushButton_confirm.clicked.connect(self.data_confirm)
        self.z = z
        self.zr = zr
        self.opt = opt

    def data_confirm(self):
        ret = []
        if self.opt == 0:
            ret.append(float(self.lineEdit_Eff_26.text()))  # 静叶进口几何角
            ret.append(float(self.lineEdit_k_12.text()))  # 静叶出口几何角
            ret.append(float(self.lineEdit_omaga_16.text()))  # 静叶安装角
            ret.append(float(self.lineEdit_alph2z_24.text()))  # 静叶最大厚度
            ret.append(float(self.lineEdit_faiz_12.text()))  # 静叶前缘半径
            ret.append(float(self.lineEdit_taoz_12.text()))  # 静叶尾缘半径
            ret.append(float(self.lineEdit_Maz_25.text()))  # 静叶节距
            ret.append(float(self.lineEdit_alph2z_25.text()))  # 静叶叶片数
            ret.append(float(self.lineEdit_taoz_13.text()))  # 静叶叶宽
        else:
            ret.append(float(self.lineEdit_Eff_25.text()))  # 动叶进口几何角
            ret.append(float(self.lineEdit_k_11.text()))  # 动叶出口几何角
            ret.append(float(self.lineEdit_omaga_15.text()))  # 动叶安装角
            ret.append(float(self.lineEdit_alph2z_22.text()))  # 动叶最大厚度
            ret.append(float(self.lineEdit_faiz_11.text()))  # 动叶前缘半径
            ret.append(float(self.lineEdit_taoz_11.text()))  # 动叶尾缘半径
            ret.append(float(self.lineEdit_Maz_24.text()))  # 动叶节距
            ret.append(float(self.lineEdit_alph2z_23.text()))  # 动叶叶片数
            ret.append(float(self.lineEdit_taoz_14.text()))  # 动叶叶宽
        ret.append(self.z)
        ret.append(self.zr)
        ret.append(self.opt)
        self.returnResultSignal.emit(ret)
        self.close()

    def switch1(self):
        self.widget.setVisible(True)
        self.widget1.setVisible(False)
        self.widget2.setVisible(False)

    def switch2(self):
        self.widget1.setVisible(True)
        self.widget.setVisible(False)
        self.widget2.setVisible(False)

    def switch3(self):
        self.widget2.setVisible(True)
        self.widget1.setVisible(False)
        self.widget.setVisible(False)
        if self.opt == 0:
            self.widget_dong.setVisible(False)
            self.widget_jing.setVisible(True)
        else:
            self.widget_dong.setVisible(True)
            self.widget_jing.setVisible(False)
