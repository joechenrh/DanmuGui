#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-09 22:56:15
# @Author  : Joe chen (joechenrh@gmail.com)
# @Link    : https://eggtart.icu
# @Version : $Id$

import websocket
import time 

from PyQt5.QtCore import *

import pystt
import threading

danmu_color = {'1': '#FF0000', '2': '#00CCFF', '3': '#66FF00', '4': "#FF6600", '5': '#CC00FF', '6': '#F6447F'}

def objToMessage(obj):
    content = pystt.dumps(obj)
    content_byte = bytes(content.encode('utf-8'))
    content_length = len(content_byte) + 8 + 1
    length_byte = int.to_bytes(content_length, length=4, byteorder='little')
    
    magic = bytearray([0xb1, 0x02])
    zero_byte = bytearray([0x00])
    return length_byte + length_byte + magic + zero_byte + zero_byte + content_byte + zero_byte 

def messageToInfos(message):
    pos = 0
    infos = [ ]
    while pos < len(message):
        content_length = int.from_bytes(message[pos: pos + 4], byteorder='little')
        content = message[pos + 12: pos + 4 + content_length - 1].decode(encoding='utf-8', errors='ignore')
        obj = pystt.loads(content)
        infos.append(getInfo(obj))
        pos += (4 + content_length)
    # print ("Receive {} messages".format(len(infos)))
    return infos

def getInfo(obj):
    if obj.get('type') == 'chatmsg':
        return obj, 'chatmsg'
    elif obj.get('type') == 'uenter':
        return obj, 'uenter'
    elif obj.get('type') in ['rss', 'loginres', 'dgb', 'wiru', 'rankup', 'actfsts1od_r', 'frank',
                             'rri', 'svsnres', 'newblackres', 'fire_user', 'fire_start',
                             'tsboxb', 'ghz2019arkcalc', 'ghz2019s1info', 'ghz2019s2info', 'fire_real_user',
                             'gbroadcast', 'srres', 'spbc', 'ghz2019s2calc', 'upgrade', 'rquizisn',
                             'anbc', 'wirt', 'ghz2019s1disp', 'blab', 'cthn', 'rnewbc', 'pingreq',
                             'noble_num_info', 'rank_change', 'mrkl', 'synexp', 'fswrank', 'ranklist', 'qausrespond']:
        return None, None
    else:
        #return '*** {} ***'.format(obj.get('type')), 'other'
        pass


class DanmuServer(QObject):
    messageReceived = pyqtSignal(list)

    def __init__(self):
        super(DanmuServer, self).__init__()
        self.ws = websocket.WebSocketApp("wss://danmuproxy.douyu.com:8503/",
                                         on_message=self.on_message,
                                         on_open=self.on_open)
        self.room_id = '957090'
    
    @pyqtSlot()
    def start(self):
        self.ws.run_forever()
    
    @pyqtSlot()
    def stop(self):
        self.ws.close()

    def set_room_id(self, room_id):
        self.room_id = room_id

    def on_message(self, message):
        try:
            for info, mtype in messageToInfos(message):
                if info:
                    self.messageReceived.emit([info, mtype])
        except Exception as err:
            print('** message parse err **')
            print(message, err)

    def on_open(self):
        print('### open ###')
        loginreq = {
            'type': 'loginreq',
            'room_id': self.room_id,
            'dfl': 'sn@A=105@Sss@A=1',
            'username': 'dhchen',
            'uid': '897038',
            'ver': '20190610',
            'aver': '218101901',
            'ct': '0'
        }
        
        joinreq = {
            'type': 'joingroup',
            'rid': self.room_id,
            'gid': '-9999'
        }
        
        self.ws.send(objToMessage(loginreq))
        self.ws.send(objToMessage(joinreq))
        threading.Thread(target=self.keepalive).start()
    
    def keepalive(self):
        binary = objToMessage({'type':'mrkl'})
        try:
            while True:
                self.ws.send(binary)
                time.sleep(45)
        except Exception as err:
            print('** mrkl error **')
