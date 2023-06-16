from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel, QGroupBox, QGridLayout
from PyQt5.QtCore import Qt


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_edits = []

        # 创建一个包含输入字段的小组框架
        group_box = QGroupBox(self)
        layout = QGridLayout(group_box)
        layout.setColumnStretch(1, 2)

        # 创建输入字段和标签
        for i, label_text, default_value in zip(range(4), ['交叉概率', '变异概率', '迭代步数', '群体大小'],
                                                ['0.8', '0.1', '10000', '100']):
            label = QLabel(label_text, self)
            line_edit = QLineEdit(self)
            line_edit.setText(default_value)
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
            self.line_edits.append(line_edit)

        # 创建按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText('确定')
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText('取消')
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(button_box, i + 1, 0, 1, 2)

        # 将小组框添加到布局中
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group_box)

        # 设置对话框的样式
        self.setWindowTitle("请输入遗传算法参数")
        self.setFixedWidth(300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def get_values(self):
        return [line_edit.text() for line_edit in self.line_edits]
