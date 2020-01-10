import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DanmuViewer import DanmuViewer

##########################################################################

class DanmuGui(QWidget):
    def __init__(self, parent=None):
        super(DanmuGui, self).__init__(parent)
        self.setWindowTitle('弹幕抓取')

        # 定义窗口的初始大小
        self.resize(600, 550)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # https://bbs.csdn.net/topics/392012485
        # 设置主窗体的的背景透明好像必须要使用setAttribute(Qt::WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 创建多行文本框
        self.textEdit = DanmuViewer()

        # 设置stylesheet也没用
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0, 188))
        self.textEdit.setPalette(palette)
        self.textEdit.start()
        #self.textEdit.setStyleSheet("Background-color:QColor(255, 255, 255, 120);")

        # 创建连接按钮
        self.connection_button = QPushButton('断开')
        self.connection_button.clicked.connect(self.onConnection)
        self.room_id_editor = QLineEdit()
        self.room_id_editor.textEdited.connect(self.textEdit.set_room_id)

        connection_layout = QHBoxLayout()
        connection_layout.addWidget(self.room_id_editor)
        connection_layout.addWidget(self.connection_button)

        # 实例化垂直布局
        layout = QVBoxLayout()
        
        # 相关控件添加到垂直布局中
        layout.addLayout(connection_layout)
        layout.addWidget(self.textEdit)

        # 设置布局
        self.setLayout(layout)

        self.running = True

    def onConnection(self):
        if self.running:
            self.textEdit.stop()
            self.running = False
            self.connection_button.setText("连接")
            self.room_id_editor.setEnabled(True)
        else:
            self.textEdit.start()
            self.running = True
            self.connection_button.setText("断开")
            self.room_id_editor.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DanmuGui()
    window.show()
    sys.exit(app.exec_())