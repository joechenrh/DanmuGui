#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-09 22:58:04
# @Author  : Joe chen (joechenrh@gmail.com)
# @Link    : https://eggtart.icu
# @Version : $Id$

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DanmuServer import DanmuServer

danmu_color = {'1': '#FF0000', '2': '#00CCFF', '3': '#66FF00', '4': "#FF6600", '5': '#CC00FF', '6': '#F6447F'}
fans_color = { }
for i in range(1, 6):
    fans_color[i] = "#5CAAFB"
for i in range(6, 11):
    fans_color[i] = "#43C1C2"
for i in range(11, 16):
    fans_color[i] = "#FFBA00"
for i in range(16, 21):
    fans_color[i] = "#FB7C0e"
for i in range(21, 26):
    fans_color[i] = "#F03B62"
for i in range(26, 100):
    fans_color[i] = "#9E59F5"

##########################################################################

class DanmuViewer(QTextBrowser):
    def __init__(self, parent=None):
        super(DanmuViewer, self).__init__(parent)

        # self.textEdit.setReadOnly(True)
        self.document().setMaximumBlockCount(90 + 1)
        self.setFrameStyle(QFrame.NoFrame)

        textCursor = self.textCursor()
        textBlockFormat = QTextBlockFormat()
        textBlockFormat.setLineHeight(15, QTextBlockFormat.FixedHeight)
        textCursor.setBlockFormat(textBlockFormat);
        self.setTextCursor(textCursor);
        
        self.setViewportMargins(0, 0, 0, 3)
        self.setFont(QFont("Microsoft YaHei", 10))

        # 设置线程
        self.server = DanmuServer()  # no parent!
        self.server_thread = QThread()  # no parent!
        self.server.messageReceived.connect(self.onMessageReceived)
        self.server.moveToThread(self.server_thread)
        self.server_thread.started.connect(self.server.start)
        self.server_thread.finished.connect(self.server.stop)
        self.server_thread.start()

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server_thread.quit()
        self.server.stop()
        self.insertHtml("""<p style="color:#FFFFFF;align:center;">-----------------------------------------------------------------------------</p>""")
        self.append("")

    def set_room_id(self, room_id):
        self.server.room_id = room_id

    def onMessageReceived(self, pack):
        obj, mtype = pack[0], pack[1]

        #                    <td height='16' width='60' align=right>
        #                <p style='font-size:12px;background-image: url(fanslevels/11.png) no-repeat;color:#000000'>__小肚皮</font>
        #            </td>

        html_nobanner = \
            """
            <table>
                <tr>
                    <td valign=middle><img src='levels/{}.png' height='16'></td>
                    <td valign=middle>&nbsp;<font style="color:#2B8EF1;">{}:&nbsp;</font></td>
                    <td valign=middle>{}</td>
                </tr>
            </table>
            """
 
        html_banner = \
            """
            <table>
                <tr>
                    <td valign=middle><img src='levels/{}.png' height='16'></td>
                    <td valign=middle>&nbsp;<font style="font-weight:bold;background-color:{};">{}</font></td>
                    <td valign=middle><font style="color:#2B8EF1;">&nbsp;{}:&nbsp;</font></td>
                    <td valign=middle>{}</td>
                </tr>
            </table>
            """

        enterHtml = """<font style="font-weight:bold;" color=#FFFFFF>{}</font>"""

        if mtype == 'chatmsg':
            # 字体颜色和弹幕颜色一致
            if obj.get('col'):
                font_color = danmu_color[obj.get('col')]
            else:
                font_color = "#FFFFFF"

            # 贵族弹幕加背景
            if obj.get('nl', '') and int(obj.get('nl', '')) > 2:
                txt = "<font style='background:#FFF3DF;color:#000000'>{}</font>".format(obj.get('txt'))
            else:
                txt = "<font style='color:{}'>{}</font>".format(font_color, obj.get('txt'))

            # 牌子等级加背景
            banner_level = int(obj.get('bl'))
            if banner_level:
                bnn = "[{}级{}]".format(banner_level, obj.get('bnn'))
                self.insertHtml(html_banner.format(obj.get('level'), fans_color[banner_level], bnn, obj.get('nn'), txt))
            else:
                self.insertHtml(html_nobanner.format(obj.get('level'), obj.get('nn'), txt))

            
        
        elif mtype == 'uenter':
            str = "欢迎 {} 来到直播间".format(obj.get('nn',''))
            self.insertHtml(enterHtml.format(str))
        
        self.append("")
    
    def mousePressEvent(self, event):
        return
