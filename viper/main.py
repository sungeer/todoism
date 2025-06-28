import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt  # 设置对齐方式
from PySide6.QtWidgets import (
    QWidget,  # 窗口部件
    QVBoxLayout,  # 垂直布局
    QHBoxLayout,  # 水平布局
    QApplication,  # 应用程序
    QHeaderView,  # 表格头部视图
    QCheckBox,  # 复选框
    QTableWidgetItem  # 表格项
)
from qfluentwidgets import (
    CardWidget,  # 卡片样式的组件
    PushButton,  # 按钮
    SearchLineEdit,  # 搜索输入框
    TableWidget,  # 表格组件
    setCustomStyleSheet  # 设置自定义样式
)
from loguru import logger
from dotenv import find_dotenv, load_dotenv

from viper.styles import ADD_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE

load_dotenv(find_dotenv())

DEV_MODE = os.getenv('DEBUG') == '1'  # None

if DEV_MODE:
    BASE_DIR = Path(__file__).resolve().parent.parent
else:
    BASE_DIR = Path(sys.executable).parent  # 获取可执行文件所在目录

LOG_DIR = Path(BASE_DIR) / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_DIR = Path(BASE_DIR) / 'dbs'
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DB_DIR.joinpath(f'wutip_{datetime.now().strftime('%Y-%m-%d')}.db')
LOG_FILE = LOG_DIR.joinpath(f'wutip_{datetime.now().strftime('%Y-%m-%d')}.log')

logger.remove()

logger.add(
    LOG_FILE,
    rotation='500MB',
    format='{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,  # 启用异步日志处理
    level='INFO',
    diagnose=False,  # 关闭变量值
    backtrace=False,  # 关闭完整堆栈跟踪
    colorize=False
)

if DEV_MODE:
    logger.add(
        sink=sys.stdout,  # 输出到标准输出流
        format='{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {message}',  # 日志格式
        level='DEBUG',
        diagnose=False,
        backtrace=False,
        colorize=False,
        enqueue=True
    )


class StudentInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('studentInterface')  # 设置当前界面的对象名称
        self.students = []  # 存储学生数据的列表
        self.setup_ui()  # 配置界面布局和组件
        self.load_data()  # 加载学生数据
        self.populate_table()  # 填充表格

    def setup_ui(self):
        layout = QVBoxLayout(self)  # 创建垂直布局，并将其设置为当前窗口的主布局

        # 顶部按钮组
        card_widget = CardWidget(self)  # 创建卡片样式的组件作为按钮组容器，并设置父组件为当前窗口
        buttons_layout = QHBoxLayout(card_widget)  # 创建水平布局，用于放置按钮，并将其设置为 card_widget 的布局
        self.addButton = PushButton("新增", self)  # 创建一个“新增”按钮，并将其设置为当前窗口的子组件
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)  # 应用自定义样式

        # 创建搜索输入框
        self.searchInput = SearchLineEdit(self)  # 创建一个搜索输入框，并将其设置为当前窗口的子组件
        self.searchInput.setPlaceholderText("搜索学生姓名或学号...")  # 设置占位提示文字
        self.searchInput.setFixedWidth(500)  # 设置输入框固定宽度为 500

        # 创建“批量删除”按钮并应用自定义样式
        self.batchDeleteButton = PushButton("批量删除", self)
        setCustomStyleSheet(self.batchDeleteButton, BATCH_DELETE_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE)

        # 将按钮和搜索框添加到按钮组的水平布局中
        buttons_layout.addWidget(self.addButton)  # 添加“新增”按钮
        buttons_layout.addWidget(self.searchInput)  # 添加搜索输入框
        buttons_layout.addStretch(1)  # 添加弹性空间，将按钮推向两端
        buttons_layout.addWidget(self.batchDeleteButton)  # 添加“批量删除”按钮

        # 将按钮组的卡片组件添加到主布局中
        layout.addWidget(card_widget)

        # 表格组件（创建空表格，后续填充内容）
        self.table_widget = TableWidget(self)
        self.table_widget.setBorderVisible(True)  # 设置表格边框可见
        self.table_widget.setBorderRadius(8)  # 设置表格圆角
        self.table_widget.setWordWrap(False)  # 禁用自动换行

        # 设置表头填充模式和列数
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # 表头填充模式为 Stretch，使表头填满整个表格，并实现列宽自适应屏幕缩放的效果
        self.table_widget.setColumnCount(11)  # 设置表格列数为 11 列
        self.table_widget.setHorizontalHeaderLabels(
            ["", "学生ID", "姓名", "学号", "性别", "班级", "语文", "数学", "英语", "总分", "操作"])  # 设置表头名称

        # 将表格组件添加到主布局中
        layout.addWidget(self.table_widget)
        self.setStyleSheet("StudentInterface{background: white}")  # 设置界面背景为白色
        self.resize(1280, 760)  # 设置窗口大小为 1280x760

    @staticmethod
    def create_db():
        sql_str = '''
            CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY,
                student_name TEXT NOT NULL,
                student_number TEXT NOT NULL UNIQUE,
                gender INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                chinese_score REAL,
                math_score REAL,
                english_score REAL
            );
        '''
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(sql_str)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def load_data(self):  # 定义 load_data 方法，用于加载学生数据
        # 使用假数据替换数据库查询
        self.students = [
            {"student_id": 1, "student_name": "张三", "student_number": "2024010101", "gender": 1,
             "class_name": "一年1班", "chinese_score": 85, "math_score": 90, "english_score": 88, "total_score": 260},
            {"student_id": 2, "student_name": "李四", "student_number": "2024010102", "gender": 2,
             "class_name": "一年1班", "chinese_score": 92, "math_score": 88, "english_score": 95, "total_score": 260},
            {"student_id": 3, "student_name": "王五", "student_number": "2024010103", "gender": 1,
             "class_name": "一年1班", "chinese_score": 78, "math_score": 82, "english_score": 80, "total_score": 260},
            {"student_id": 4, "student_name": "赵六", "student_number": "2024010104", "gender": 2,
             "class_name": "一年1班", "chinese_score": 88, "math_score": 95, "english_score": 89, "total_score": 260},
            {"student_id": 5, "student_name": "陈七", "student_number": "2024010105", "gender": 1,
             "class_name": "一年1班", "chinese_score": 90, "math_score": 91, "english_score": 93, "total_score": 260},
        ]

    def populate_table(self):  # 定义 populate_table 方法，用于填充表格数据
        self.table_widget.setRowCount(len(self.students))  # 设置表格行数为学生数据的数量
        for row, student_info in enumerate(self.students):  # 遍历学生数据并设置每行的内容
            self.setup_table_row(row, student_info)  # 调用 setup_table_row 方法，设置每一行的数据

    def setup_table_row(self, row, student_info):  # 定义 setup_table_row 方法，用于设置表格行数据
        checkbox = QCheckBox()  # 创建复选框
        self.table_widget.setCellWidget(row, 0, checkbox)  # 将复选框添加到表格的第一列

        # 遍历学生数据的各个字段并添加到表格中
        for col, key in enumerate(
                ['student_id', 'student_name', 'student_number', 'gender', 'class_name', 'chinese_score', 'math_score',
                 'english_score', 'total_score']):
            value = student_info.get(key, '')  # 获取对应字段的值
            if key == 'gender':  # 若字段为性别，进行性别的转换显示
                value = '男' if value == 1 else '女' if value == 2 else '未知'
            item = QTableWidgetItem(str(value))  # 创建表格项
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置文本居中
            self.table_widget.setItem(row, col + 1, item)  # 将表格项添加到表格中对应的列


app = QApplication(sys.argv)  # 创建应用程序实例
window = StudentInterface()  # 创建 StudentInterface 窗口实例
window.show()  # 显示窗口
sys.exit(app.exec())  # 进入应用程序主循环，并在退出时返回状态码
