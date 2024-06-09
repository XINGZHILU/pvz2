import sys
import os
import pyperclip
import openpyxl
import datetime
import copy
import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
#from pathlib import Path

def waveconfig(lvl):#返回每两大波之间小波数
    if lvl%5 == 0:
        return 0
    elif 31<=lvl<=99:
        return lvl//10+5
    else:
        return 15

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.endlesslist = ['埃及','失落', '西部', '功夫', '未来', '黑暗', '海滩',
                            '冰河', '天空', '海盗', '摇滚', '恐龙', '摩登']
        self.wavedata = []
        self.comb = []
        self.tablename = '/'
        self.getcurrent()
        self.load()
        self.setWindowTitle('无尽导航')
        self.central = QStackedWidget()
        self.startup = QWidget()
        self.central.addWidget(self.startup)
        self.loading = QWidget()
        self.central.addWidget(self.loading)
        self.main = QSplitter()
        self.main.setSizes([15,300])
        self.main.setHandleWidth(15)
        self.left = QStackedWidget()
        self.leftmain = QWidget()
        self.setCentralWidget(self.central)
        self.sysfont = QFont('等线',12)
        self.setInitial()
        self.setUI()

    def setInitial(self):
        self.initlayout = QFormLayout()
        self.filelabel = QLineEdit('/')
        self.file = QPushButton('选择文件')
        self.file.clicked.connect(self.askfile)
        self.finish = QPushButton('开始')
        self.finish.setEnabled(False)
        self.finish.clicked.connect(self.start)
        self.initlayout.addWidget(self.filelabel)
        self.initlayout.addWidget(self.file)
        self.initlayout.addWidget(self.finish)
        self.startup.setLayout(self.initlayout)
        self.loadlayout = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setMaximum(149)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        self.progresslayout = QHBoxLayout()
        self.loadlayout.addWidget(self.progress)
        self.loadlayout.addWidget(QLabel('正在读取中...'))
        self.loading.setLayout(self.loadlayout)

    def setUI(self):
        self.leftlayout = QFormLayout()
        self.setleft()
        self.leftmain.setLayout(self.leftlayout)
        self.left.addWidget(self.leftmain)
        self.main.addWidget(self.left)
        self.result = QTableWidget(15,5)
        self.main.addWidget(self.result)
        self.central.addWidget(self.main)
        self.setFont(self.sysfont)

    def setleft(self):
        self.endless = QComboBox()
        self.endless.addItems(self.endlesslist)
        self.endless.setCurrentText(self.endlesslist[self.current])
        self.endless.currentTextChanged.connect(self.change)
        self.leftlayout.addRow('无尽：',self.endless)
        self.zombieselection = QStackedWidget()
        self.addzombies()
        self.zombieselection.setCurrentIndex(self.current)
        self.leftlayout.addWidget(self.zombieselection)

    # noinspection PyUnresolvedReferences
    def addzombies(self):
        self.selectionlist = []
        self.states = []
        for zlist in self.zombies:
            self.widget = QWidget()
            self.selectionlayout = QVBoxLayout()
            self.buttons = []
            self.states.append([])
            for z in zlist:
                self.btn = QCheckBox(z[0])
                self.btn.stateChanged.connect(self.checkzombies)
                self.buttons.append(self.btn)
                self.selectionlayout.addWidget(self.btn)
                self.states[-1].append(False)
            self.selectionlist.append(self.buttons)
            self.widget.setLayout(self.selectionlayout)
            self.zombieselection.addWidget(self.widget)

    def getcurrent(self):
        t = datetime.datetime.now()
        self.time = datetime.date(t.year,t.month,t.day)
        year = self.time.year
        date = datetime.date(year, 1, 1)
        date+=datetime.timedelta(days=(11 - date.isoweekday()) % 7)
        ind = 0
        while (self.time-date).days>=7:
            ind+=1
            ind%=13
            date += datetime.timedelta(days=7)
        if 1<=self.time.isoweekday()<=3:
            ind+=1
            ind%=13
        self.current = (ind+1)%13

    def load(self):
        self.zombies = []
        f = open('zombies.txt','r', encoding='utf-8')
        lines = [i.strip('\n') for i in f.readlines()]
        f.close()
        z=[]
        for i in lines:
            if i == '/':
                self.zombies.append(z)
                z = []
            else:
                z.append(i.split('\t'))

    def change(self):
        self.current = self.endlesslist.index(self.endless.currentText())
        self.zombieselection.setCurrentIndex(self.current)

    def checkzombies(self):
        old = copy.deepcopy(self.states[self.current])
        self.states[self.current] = []
        for i in self.selectionlist[self.current]:
            self.states[self.current].append(i.isChecked())
        print(self.selectionlist[0][0].checkState())
        if self.states[self.current].count(True)>5:
            for i in range(len(old)):
                if old[i]!=self.states[self.current][i]:
                    index = i
                    break
            self.selectionlist[self.current][index].setChecked(False)

    def askfile(self):
        self.newname = QFileDialog.getOpenFileName(self, '选择卡波表',filter = 'xlsx文件 (*.xlsx)')[0]
        if self.newname != '':
            self.tablename = self.newname
            self.filelabel.setText(self.tablename)
            self.finish.setEnabled(True)

    def start(self):
        self.central.setCurrentIndex(1)
        self.progress.setValue(10)
        print(self.tablename)
        #self.wb = openpyxl.load_workbook(self.tablename)
        #self.worksheet = self.wb.worksheets[0]
        self.progress.setValue(30)

    def next(self):
        self.central.setCurrentIndex(self.central.currentIndex()+1)



if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Main()
    demo.show()
    sys.exit(app.exec())