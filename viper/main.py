import sys

from PySide6.QtWidgets import (
    QWidget,  # 窗口部件
    QVBoxLayout,  # 垂直布局
    QHBoxLayout,  # 水平布局
    QApplication  # 应用程序
)
from qfluentwidgets import (
    CardWidget,  # 卡片样式组件
    PushButton,  # 按钮
    SearchLineEdit,  # 搜索输入框
    TableWidget,  # 表格组件
    setCustomStyleSheet  # 设置自定义样式
)

from viper.styles import (
    ADD_BUTTON_STYLE,  # 新增
    BATCH_DELETE_BUTTON_STYLE  # 批量删除
)


class StudentInterface(QWidget):

    def __init__(self):  # 初始化方法
        super().__init__()  # 调用父类 QWidget 的初始化方法
        self.setObjectName("studentInterface")  # 设置当前界面的对象名称
        self.setup_ui()  # 调用 setup_ui() 方法，设置界面布局和组件

    def setup_ui(self):  # 定义 setup_ui 方法，用于设置界面的布局和组件
        layout = QVBoxLayout(self)  # 创建一个垂直布局，并将其设置为当前窗口的布局

        # 顶部按钮组
        card_widget = CardWidget(self)  # 创建一个卡片组件作为按钮组容器，并设置父组件为当前窗口
        buttons_layout = QHBoxLayout(card_widget)  # 创建水平布局，用于放置按钮，并将其设置为 card_widget 的布局
        self.addButton = PushButton("新增", self)  # 创建一个 "新增" 按钮，并将其设置为当前窗口的子组件
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)  # 设置“新增”按钮的样式
        self.searchInput = SearchLineEdit(self)  # 创建一个搜索输入框，并将其设置为当前窗口的子组件
        self.searchInput.setPlaceholderText("搜索学生姓名或学号...")  # 设置搜索输入框的占位提示文字
        self.searchInput.setFixedWidth(500)  # 设置搜索输入框的固定宽度为500
        self.batchDeleteButton = PushButton("批量删除", self)  # 创建一个 "批量删除" 按钮，并将其设置为当前窗口的子组件
        setCustomStyleSheet(self.batchDeleteButton, BATCH_DELETE_BUTTON_STYLE,
                            BATCH_DELETE_BUTTON_STYLE)  # 设置“批量删除”按钮的样式

        buttons_layout.addWidget(self.addButton)  # 将 "新增" 按钮添加到按钮组的水平布局中
        buttons_layout.addWidget(self.searchInput)  # 将搜索输入框添加到按钮组的水平布局中
        buttons_layout.addStretch(1)  # 在布局中间添加一个空白区域，将按钮推向左右两端
        buttons_layout.addWidget(self.batchDeleteButton)  # 将 "批量删除" 按钮添加到按钮组的水平布局中

        layout.addWidget(card_widget)  # 将 card_widget 添加到主布局中

        # 表格(先创建一个空表格,后续会添加内容)
        self.table_widget = TableWidget(self)  # 创建一个表格组件，并将其设置为当前窗口的子组件
        self.table_widget.setBorderVisible(True)  # 设置表格边框为可见
        self.table_widget.setBorderRadius(8)  # 设置表格边框的圆角半径为 8
        self.table_widget.setWordWrap(False)  # 禁用表格内文字换行

        layout.addWidget(self.table_widget)  # 将表格组件添加到主布局中
        self.setStyleSheet("StudentInterface{background: white}")  # 设置当前界面的背景色为白色
        self.resize(1280, 760)  # 设置窗口大小为1280x760


app = QApplication(sys.argv)  # 创建应用程序实例
window = StudentInterface()  # 创建 StudentInterface 窗口实例
window.show()  # 显示窗口
sys.exit(app.exec())  # 进入应用程序主循环，并在退出时返回状态码
