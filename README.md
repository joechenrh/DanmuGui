# DanmuGui

抓取斗鱼弹幕

![Screenshot](https://github.com/joechenrh/DanmuGui/blob/master/Screenshot.png)

## Usage

启动 `DanmuGui.py` 会自动开始爬取弹幕并显示

可以手动断开并更换房间号

目前是通过 `QTextBrowser` 配合 html 来显示弹幕，但是html的功能比较弱，所以很难有好的显示效果

（不过如果不要添加图片的话，那就什么问题都没有了）

## Dependence

- websocket-client
- PyQt5
- pystt

## 问题

理论上哪个平台都可以

但是，似乎在Windows平台上显示相比Linux有些问题（其实Linux也有，就是看上去小一点）

由于没法对元素进行垂直对齐，同时显示图片和文本时，文本无法垂直居中，导致看上去不太好看。
