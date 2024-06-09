import sys
import os
import math
import pyperclip

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.paste = ''
        self.peadmg = 6000
        self.reddmg = 9000
        self.purpledmg = 15000
        self.hpdict={'埃及':(3750,6250,5000),'失落':(3200,4800,8000),'西部':(3835,5900,5310),'功夫':(2550,4250,5950),'未来':(3640,5320,6160),
         '黑暗':(3000,4500,7500),'沙滩':(3000,4500,6000),'冰河':(4000,4000,6400),'天空':(3500,3500,9100),'海盗':(3135,5700,6270),
         '摇滚':(2000,2400,2800,3200,4400),'恐龙':(3000,4500,7500),'摩登埃及':(450,750,600),'摩登海盗':(825,1500,1650),
         '摩登西部':(975,1500,1350),'摩登未来':(3000,4500,7500),'摩登黑暗':(3000,4500,7500)}
        self.bosslist = list(self.hpdict)
        self.tooldict={'魔豆':30,'号角':20,'其他':0}
        self.peaclockdict={'紫手套':[30,0],'红蜡烛':[0,27],'金属弹弓':[33,0],'其他':[0,0]}
        self.flameboost = 1

        self.calcflag = False

        #self.setWindowIcon(QIcon(resource_path('wh.png')))
        self.setWindowTitle('原豌Boss计算      iOS-独特的萝卜伞')

        self.line = QLabel('')
        self.line.setProperty('name','line')

        self.setUI()



    def setUI(self):
        self.totallayout = QVBoxLayout()
        self.mainlayout = QHBoxLayout()

        self.leftlayout = QVBoxLayout()

        self.datalayout = QFormLayout()
        self.tool = QComboBox()
        self.tool.addItems(['魔豆','号角','其他'])
        self.tool.setCurrentText('其他')
        self.tool.currentTextChanged.connect(self.peacalc)

        self.datalayout.addRow('神器',self.tool)
        self.datalayout.addRow('',QLabel(' '*35))
        self.datalayout.addRow(self.line)

        self.peafamily = QDoubleSpinBox()
        self.peafamily.setRange(0.00, 60.00)
        self.peafamily.setSingleStep(0.01)
        self.peafamily.setValue(50)
        self.peafamily.valueChanged.connect(self.peacalc)

        self.datalayout.addRow('<b>原豌家族攻击力</b>', self.peafamily)

        self.peaclock = QComboBox()
        self.peaclock.addItems(['紫手套','红蜡烛','金属弹弓','其他'])
        self.peaclock.setCurrentText('红蜡烛')
        self.peaclock.currentTextChanged.connect(self.peacalc)

        self.datalayout.addRow('原豌挂件', self.peaclock)

        self.peagene = QSpinBox()
        self.peagene.setRange(0,40)
        self.peagene.setSingleStep(4)
        self.peagene.setValue(40)
        self.peagene.valueChanged.connect(self.peacalc)

        self.datalayout.addRow('原豌基因进化',self.peagene)

        self.peaboost = QLabel()
        self.datalayout.addRow(self.peaboost)

        self.peadmgbox = QLCDNumber()
        self.peadmgbox.display(self.peadmg)

        self.reddmgbox = QLCDNumber()
        self.reddmgbox.display(self.reddmg)

        self.purpledmgbox = QLCDNumber()
        self.purpledmgbox.display(self.purpledmg)
        self.datalayout.addRow(self.line)
        self.datalayout.addRow('无火炬单发伤害',self.peadmgbox)
        self.datalayout.addRow('红火单发伤害', self.reddmgbox)
        self.datalayout.addRow('紫火单发伤害', self.purpledmgbox)


        self.leftlayout.addLayout(self.datalayout)

        self.mainlayout.addLayout(self.leftlayout)

        self.rightlayout = QVBoxLayout()

        self.bosslayout = QFormLayout()

        self.BossSelection = QComboBox()
        self.BossSelection.addItems(self.bosslist)
        self.BossSelection.currentTextChanged.connect(self.bosscalc)

        self.bosslayout.addRow('Boss:', self.BossSelection)

        self.bosslayout.addRow(QLabel(''))

        self.result = QStandardItemModel(30, 5, self)
        self.result.setProperty('type','result')
        self.resultshow = QTableView()
        self.resultshow.setModel(self.result)
        self.resultshow.horizontalHeader().hide()
        self.resultshow.verticalHeader().hide()
        self.resultshow.setProperty('type','result')
        self.bosslayout.addRow(self.resultshow)

        self.rightlayout.addLayout(self.bosslayout)

        self.mainlayout.addLayout(self.rightlayout)

        self.totallayout.addLayout(self.mainlayout)

        self.copyright = QLabel('iOS-独特的萝卜伞')
        self.copyright.setProperty('info','copy')

        self.copybtn = QPushButton('拷贝结果')
        self.copybtn.setProperty('name','copy')
        self.copybtn.clicked.connect(self.copy)

        self.bosslayout.addRow('',self.copybtn)
        self.bosslayout.addRow(self.line)
        self.bosslayout.addRow(self.copyright)

        self.setLayout(self.totallayout)

        self.calcflag = True

        self.peacalc()

    def bosscalc(self):
        blood = len(self.hpdict[self.BossSelection.currentText()])
        hplist = list(self.hpdict[self.BossSelection.currentText()])
        hplist.append(hplist[0]+hplist[1])
        self.result = QStandardItemModel(30, 1, self)
        self.result.setColumnCount(blood+2)
        for r in range(1,30):
            self.result.setItem(r,0,QStandardItem(f"第{r*5}关"))
        for c in range(1,blood+1):
            self.result.setItem(0, c, QStandardItem(f"{['一','二','三','四','五'][c-1]}血"))
        self.result.setItem(0, blood+1, QStandardItem('前二血'))
        for column in range(1,blood+2):
            for row in range(1,30):
                hp = hplist[column-1]*3*row-2
                amount = f'{math.ceil(hp/self.purpledmg)}发 / {math.ceil(hp/self.purpledmg/5)}大招'
                #amount = amount.center(12)
                item = QStandardItem(amount)
                self.result.setItem(row,column, item)
        self.resultshow.setModel(self.result)

    def peacalc(self):
        if self.calcflag:
            atkboost = round((120 + self.peagene.value() + self.peaclockdict[self.peaclock.currentText()][0] + self.tooldict[self.tool.currentText()] + self.peafamily.value()) / 100, 4)
            fireboost = round((100 + self.peaclockdict[self.peaclock.currentText()][1]) / 100, 4)
            self.peaboost.setText(f'(攻击力={str(atkboost)}倍\t火焰伤害={str(fireboost)}倍)')
            self.peadmg = math.floor(6000 * atkboost)
            self.reddmg = math.floor(9000 * atkboost * fireboost)
            self.purpledmg = math.floor(15000 * atkboost * fireboost)
            self.peadmgbox.display(self.peadmg)
            self.reddmgbox.display(self.reddmg)
            self.purpledmgbox.display(self.purpledmg)
            self.bosscalc()

    def copy(self):
        pyperclip.copy(self.paste)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Main()
    fontsize = 50
    qss = '* {font: ' + str(fontsize)+'px}\nQLabel {font: bold '+str(fontsize)+"px}\nQPushButton[name = 'copy'] {font: bold 50px}"
    qss += "QLabel[name='line'] {font: 15px}"
    demo.setStyleSheet(qss)
    demo.show()
    sys.exit(app.exec_())