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
        self.witchdmg = 1200
        self.peadmg = 6000
        self.reddmg = 9000
        self.purpledmg = 15000
        self.bosslist = ['埃及', '失落', '西部', '未来', '海盗', '摩登埃及',
                         '摩登海盗', '摩登西部', '摩登未来', '摩登黑暗']
        self.hpdict={'埃及':3750,'失落':3200,'西部':3835,'未来':3640,'海盗':3135,'摩登埃及':450,'摩登海盗':825,
                     '摩登西部':975,'摩登未来':3000,'摩登黑暗':3000}
        self.tooldict={'魔豆':[0,30],'退化':[30,0],'号角':[0,20],'其他':[0,0]}
        self.witchclockdict={'金属弹弓':[33,0],'魔法书':[0,27],'其他':[0,0]}#0=攻击力，1=属性
        self.peaclockdict={'紫手套':[30,0],'红蜡烛':[0,27],'金属弹弓':[33,0],'其他':[0,0]}
        self.flameboost = 1

        self.calcflag = False

        self.setWindowIcon(QIcon(resource_path('wh.png')))
        self.setWindowTitle('金缕梅Boss计算      iOS-独特的萝卜伞')

        self.line = QLabel('')
        self.line.setProperty('name','line')

        self.setUI()



    def setUI(self):
        self.totallayout = QVBoxLayout()
        self.mainlayout = QHBoxLayout()

        self.leftlayout = QVBoxLayout()

        self.datalayout = QFormLayout()

        self.tool = QComboBox()
        self.tool.addItems(['魔豆','号角','退化','其他'])
        self.tool.setCurrentText('其他')
        self.tool.currentTextChanged.connect(self.peacalc)
        self.tool.currentTextChanged.connect(self.witchcalc)

        self.datalayout.addRow('神器',self.tool)
        self.datalayout.addRow('',QLabel(''))
        self.datalayout.addRow(self.line)

        self.witchlabel = QLCDNumber()
        self.witchlabel.display(self.witchdmg)

        self.witchclock = QComboBox()
        self.witchclock.addItems(['魔法书','金属弹弓','其他'])
        self.witchclock.currentTextChanged.connect(self.witchcalc)

        self.witchatkfamily = QDoubleSpinBox()
        self.witchatkfamily.setRange(0.00, 60.00)
        self.witchatkfamily.setSingleStep(0.01)
        self.witchatkfamily.valueChanged.connect(self.witchcalc)

        self.witchmagicfamily = QDoubleSpinBox()
        self.witchmagicfamily.setRange(0.00, 60.00)
        self.witchmagicfamily.setSingleStep(0.01)
        self.witchmagicfamily.setValue(0)
        self.witchmagicfamily.valueChanged.connect(self.witchcalc)

        self.datalayout.addRow('<b>金缕梅家族攻击力</b>', self.witchatkfamily)
        #self.datalayout.addRow('<b>金缕梅家族魔法伤害</b>', self.witchmagicfamily)
        self.datalayout.addRow('<b>金缕梅挂件</b>', self.witchclock)

        self.witchboost = QLabel('')
        self.datalayout.addRow(self.witchboost)

        self.datalayout.addRow(self.line)
        self.datalayout.addRow('<b>金缕梅伤害</b>', self.witchlabel)
        self.datalayout.addRow('', QLabel(''))
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

        self.bosslayout.addRow('', QLabel(''))

        self.labellvl5 = QLabel('')
        self.labellvl10 = QLabel('')
        self.labellvl15 = QLabel('')
        self.labellvl20 = QLabel('')
        self.labellvl25 = QLabel('')
        self.labellvl30 = QLabel('')
        self.labellvl35 = QLabel('')
        self.labellvl40 = QLabel('')
        self.labellvl45 = QLabel('')
        self.labellvl50 = QLabel('')
        self.labellvl55 = QLabel('')

        self.resultList = [
self.labellvl5,
self.labellvl10,
self.labellvl15,
self.labellvl20,
self.labellvl25,
self.labellvl30,
self.labellvl35,
self.labellvl40,
self.labellvl45,
self.labellvl50,
self.labellvl55
                           ]

        self.bosslayout.addRow('', QLabel('无原豌单发    计入原豌单发    红火    紫火'))
        lvlnum = 5
        for label in self.resultList:
            self.bosslayout.addRow('第'+str(lvlnum)+'关:',label)
            lvlnum+=5

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

        self.witchmagicfamily.setValue(0)
        self.witchatkfamily.setValue(0)

        self.peacalc()
        self.witchcalc()


    def witchcalc(self):
        if self.calcflag:
            atk = (100 + self.witchatkfamily.value() + self.witchclockdict[self.witchclock.currentText()][0] + self.tooldict[self.tool.currentText()][0]) / 100
            #magic = (100 + self.witchmagicfamily.value() + self.witchclockdict[self.witchclock.currentText()][1]) / 100
            magic = (100 + self.witchclockdict[self.witchclock.currentText()][1]) / 100
            self.witchdmg = math.floor(magic * atk * 3600)
            self.witchboost.setText(f'(攻击力={str(atk)[0:6]}倍\t魔法伤害={str(magic)[0:6]}倍)')
            self.witchlabel.display(self.witchdmg)
            self.bosscalc()

    def bosscalc(self):
        if self.calcflag:
            self.paste = ''
            lvl = 5
            basehp = self.hpdict[self.BossSelection.currentText()]
            for lbl in self.resultList:
                lvlhp = basehp * (lvl * 0.6 - 2)
                nopea = str(math.ceil(lvlhp / self.witchdmg))
                withpea = str(math.ceil(max(0,(lvlhp - self.peadmg)) / self.witchdmg))
                withred = str(math.ceil(max(0,(lvlhp - self.reddmg)) / self.witchdmg))
                withpurple = str(math.ceil(max(0, (lvlhp - self.purpledmg)) / self.witchdmg))
                outputtxt = nopea + (14-len(nopea)) * ' ' + withpea + (16-len(withpea)) * ' ' + withred + (8-len(withred)) * ' ' + withpurple
                self.paste += str(lvl) + '\t' + str(nopea) + '\t' + str(withpea) + '\t' + str(withred) + '\t' + str(withpurple) + '\n'
                lbl.setText(outputtxt)
                lvl+=5

    def peacalc(self):
        if self.calcflag:
            atkboost = (120 + self.peagene.value() + self.peaclockdict[self.peaclock.currentText()][0] + self.tooldict[self.tool.currentText()][1] + self.peafamily.value()) / 100
            fireboost = (100 + self.peaclockdict[self.peaclock.currentText()][1]) / 100
            self.peaboost.setText(f'(攻击力={str(atkboost)[0:6]}倍\t火焰伤害={str(fireboost)[0:6]}倍)')
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