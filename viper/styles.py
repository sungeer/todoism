# 通用按钮样式
BUTTON_STYLE = """
QPushButton {
    border: none; /* 无边框 */
    padding: 5px 10px; /* 内边距，顶部和底部5px，左右10px */
    font-family: 'Segoe UI', 'Microsoft YaHei'; /* 字体为 Segoe UI 或微软雅黑 */
    font-size: 14px; /* 字体大小为14px */
    color: white; /* 字体颜色为白色 */
    border-radius: 5px; /* 圆角半径为5px */
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1); /* 悬停时背景颜色 */
}
QPushButton:pressed {
    background-color: rgba(255, 255, 255, 0.2); /* 按下时背景颜色 */
}
"""

# 新增按钮样式
ADD_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #0d6efd; /* 默认背景颜色为蓝色 */
}
QPushButton:hover {
    background-color: #0b5ed7; /* 悬停时背景颜色为深蓝 */
}
QPushButton:pressed {
    background-color: #0a58ca; /* 按下时背景颜色为更深的蓝色 */
}
"""

# 删除按钮样式
DELETE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #dc3545; /* 默认背景颜色为红色 */
}
QPushButton:hover {
    background-color: #bb2d3b; /* 悬停时背景颜色为深红 */
}
QPushButton:pressed {
    background-color: #b02a37; /* 按下时背景颜色为更深的红色 */
}
"""

# 批量删除按钮样式
BATCH_DELETE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #fd7e14; /* 默认背景颜色为橙色 */
}
QPushButton:hover {
    background-color: #e96b10; /* 悬停时背景颜色为深橙 */
}
QPushButton:pressed {
    background-color: #dc680f; /* 按下时背景颜色为更深的橙色 */
}
"""

# 更新按钮样式
UPDATE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #198754; /* 默认背景颜色为绿色 */
}
QPushButton:hover {
    background-color: #157347; /* 悬停时背景颜色为深绿 */
}
QPushButton:pressed {
    background-color: #146c43; /* 按下时背景颜色为更深的绿色 */
}
"""

# 导入按钮样式
IMPORT_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #6f42c1; /* 默认背景颜色为紫色 */
}
QPushButton:hover {
    background-color: #5936a2; /* 悬停时背景颜色为深紫 */
}
QPushButton:pressed {
    background-color: #4a2d8e; /* 按下时背景颜色为更深的紫色 */
}
"""

# 导出按钮样式
EXPORT_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #20c997; /* 默认背景颜色为青绿色 */
}
QPushButton:hover {
    background-color: #1aa179; /* 悬停时背景颜色为深青绿色 */
}
QPushButton:pressed {
    background-color: #198b6d; /* 按下时背景颜色为更深的青绿色 */
}
"""
