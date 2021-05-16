from PyQt5.QtWidgets import QHeaderView, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor

from stack import *
import data_processing_module as DataModel

ColorList = [QColor(85, 239, 196), QColor(255, 234, 167), QColor(129, 236, 236)
    , QColor(250, 177, 160), QColor(255, 118, 117), QColor(116, 185, 255), QColor(253, 121, 168), QColor(178, 190, 195),
             QColor(45, 52, 54)
    , QColor(162, 155, 254)]
TaskAttr = ["task_id", "task_esp", "task_ebp"]
MethodAttr = ["method", "esp", "ebp"]
ColNum = 3
ItemDataMethodType = 1


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)

        self.forward_button.clicked.connect(lambda: self.forward_handler())  # 单击运行
        self.back_button.clicked.connect(lambda: self.back_handler())
        self.show_stack.itemClicked.connect(self.show_stack_item_handler)

        self.init_stack_info()
        self.show_current_data()

    def init_stack_info(self):
        self.show_stack.setColumnCount(3)
        self.show_stack.setRowCount(10)
        self.show_stack.verticalHeader().setVisible(False)
        self.show_stack.horizontalHeader().setVisible(False)
        self.show_stack.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.show_stack.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def clear_items(self):
        for i in range(0, 30):
            item = QTableWidgetItem()
            item.setBackground(QBrush(QColor(255, 255, 255)))
            self.show_stack.setItem(0, i, item)

    def get_color(self, idx):
        return QBrush(ColorList[int(idx)])

    def forward_handler(self):
        self.clear_items()
        if DataModel.ShowDataIndex < len(DataModel.ShowData) - 1:
            DataModel.ShowDataIndex += 1
        self.show_current_data()

    def back_handler(self):
        self.clear_items()
        if DataModel.ShowDataIndex > 0:
            DataModel.ShowDataIndex -= 1
        self.show_current_data()

    def show_current_data(self):
        data_dict = DataModel.get_task_info()
        # 展示数据到task_info框中
        self.task_info.setText(self.build_attr_str(data_dict, TaskAttr, ": ", "\n"))

        position = 1
        stack_info_str = ""
        method_infos = data_dict.get('method_infos')
        for method_dict in method_infos:
            item = QTableWidgetItem()
            # 设置字体
            item.setFont(self.get_my_font())
            # 设置背景颜色
            item.setBackground(self.get_color(position / ColNum))
            # 给每一个item设置当前函数数据
            method_info_str = self.build_attr_str(method_dict, MethodAttr, ": ", "\n")
            item.setData(ItemDataMethodType, method_info_str)
            item.setText(method_dict.get('method'))
            self.show_stack.setItem(0, position, item)
            position += ColNum
            stack_info_str += method_info_str + "\n"
        self.stack_info.setText(stack_info_str[:-1])

    def show_stack_item_handler(self):
        item = self.show_stack.selectedItems()[0]
        method_text = item.data(ItemDataMethodType)
        if method_text:
            self.method_info.setText(method_text)

    def build_attr_str(self, data_dict, attr_list, cat_symbol, end_symbol):
        ret_str = ""
        for attr in attr_list:
            value = data_dict.get(attr)
            if value:
                ret_str = ret_str + attr + cat_symbol + str(value) + end_symbol
        return ret_str

    def get_my_font(self):
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(8)
        return font
