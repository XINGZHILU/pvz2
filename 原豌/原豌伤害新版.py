import sys
import os
import math
import pyperclip
import datetime

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.sysfont = QFont('等线',11)
        self.state = 0
        self.witchdmg = 1200
        self.peadmg = 6000
        self.reddmg = 9000
        self.purpledmg = 15000
        self.hpdict={'埃及':(3750,6250,5000),'失落':(3200,4800,8000),'西部':(3835,5900,5310),'功夫':(2550,4250,5950),'未来':(3640,5320,6160),
         '黑暗':(3000,4500,7500),'沙滩':(3000,4500,6000),'冰河':(4000,4000,6400),'天空':(3500,3500,9100),'海盗':(3135,5700,6270),
         '摇滚':(2000,2400,2800,3200,4400),'恐龙':(3000,4500,7500),'摩登埃及':(450,750,600),'摩登海盗':(825,1500,1650),
         '摩登西部':(975,1500,1350),'摩登未来':(3000,4500,7500),'摩登黑暗':(3000,4500,7500)}
        self.bosslist = list(self.hpdict)
        self.tooldict={'魔豆':[0,30],'退化':[30,0],'号角':[0,20],'其他':[0,0]}
        self.witchclockdict={'金属弹弓':[33,0],'魔法书':[0,27],'其他':[0,0]}#0=攻击力，1=属性
        self.peaclockdict={'紫手套':[30,0],'红蜡烛':[0,27],'金属弹弓':[33,0],'其他':[0,0]}
        self.flameboost = 1

        self.calcflag = False

        self.load()

        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.setWindowTitle('原豌boss计算      iOS-独特的萝卜伞')

        self.delegate = ReadOnlyDelegate()

        self.line = QLabel('')
        self.line.setProperty('name','line')
        self.peastack = QWidget()
        self.witchstack = QWidget()
        self.datastack = QStackedWidget(self)      # 2
        self.datastack.addWidget(self.peastack)
        self.datastack.addWidget(self.witchstack)
        self.setmainUI()
        self.setwitchUI()
        self.setpeaUI()
        self.calcflag = True
        self.peacalc()
        self.witchcalc()
        self.setFont(self.sysfont)

    def load(self):
        f=open('data.txt','r')
        family = f.read().split('\n')
        f.close()
        self.peafamilyvalue = eval(family[0])
        self.witchfamilyvalue = eval(family[1])

    def setmainUI(self):
        self.central = QWidget()
        self.totallayout = QVBoxLayout()
        self.mainlayout = QHBoxLayout()

        self.leftlayout = QVBoxLayout()

        self.datalayout = QFormLayout()

        #self.modelayout = QGridLayout()
        self.peabtn = QRadioButton('原豌'+' '*4)
        self.peabtn.setChecked(1)
        self.peabtn.toggled.connect(self.switch)
        self.witchbtn = QRadioButton('金缕梅')
        #self.modelayout.addWidget(self.peabtn,0,0)
        #self.modelayout.addWidget(self.witchbtn,0,1)
        #self.leftlayout.addLayout(self.modelayout)

        self.modebar = QToolBar(self)
        self.modebar.addWidget(self.peabtn)
        self.modebar.addWidget(self.witchbtn)
        self.addToolBar(self.modebar)

        self.tool = QComboBox()
        self.tool.addItems(['魔豆', '号角', '退化', '其他'])
        self.tool.setCurrentText('其他')
        self.tool.currentTextChanged.connect(self.peacalc)
        self.tool.currentTextChanged.connect(self.witchcalc)

        self.datalayout.addRow('神器', self.tool)
        self.datalayout.addRow('', QLabel(''))
        self.datalayout.addRow(self.line)

        self.witchlabel = QLCDNumber()
        self.witchlabel.display(self.witchdmg)
        self.witchlabel.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.witchclock = QComboBox()
        self.witchclock.addItems(['魔法书', '金属弹弓', '其他'])
        self.witchclock.currentTextChanged.connect(self.witchcalc)

        self.witchatkfamily = QDoubleSpinBox()
        self.witchatkfamily.setRange(0.00, 100.00)
        self.witchatkfamily.setSingleStep(0.01)
        self.witchatkfamily.setValue(self.witchfamilyvalue)
        self.witchatkfamily.valueChanged.connect(self.witchcalc)

        '''
        self.witchmagicfamily = QDoubleSpinBox()
        self.witchmagicfamily.setRange(0.00, 100.00)
        self.witchmagicfamily.setSingleStep(0.01)
        self.witchmagicfamily.setValue(0)
        self.witchmagicfamily.valueChanged.connect(self.witchcalc)
        '''

        self.datalayout.addRow('金缕梅家族攻击力', self.witchatkfamily)
        # self.datalayout.addRow('金缕梅家族魔法伤害', self.witchmagicfamily)
        self.datalayout.addRow('金缕梅挂件', self.witchclock)

        self.witchboost = QLabel('')
        self.datalayout.addRow(self.witchboost)

        self.datalayout.addRow(self.line)
        self.datalayout.addRow('金缕梅伤害', self.witchlabel)
        self.datalayout.addRow('', QLabel(''))
        self.datalayout.addRow(self.line)

        self.peafamily = QDoubleSpinBox()
        self.peafamily.setRange(0.00, 100.00)
        self.peafamily.setSingleStep(0.01)
        self.peafamily.setValue(self.peafamilyvalue)
        self.peafamily.valueChanged.connect(self.peacalc)

        self.datalayout.addRow('原豌家族攻击力', self.peafamily)

        self.peaclock = QComboBox()
        self.peaclock.addItems(['紫手套', '红蜡烛', '金属弹弓', '其他'])
        self.peaclock.setCurrentText('红蜡烛')
        self.peaclock.currentTextChanged.connect(self.peacalc)

        self.datalayout.addRow('原豌挂件', self.peaclock)

        self.peagene = QSpinBox()
        self.peagene.setRange(0, 40)
        self.peagene.setSingleStep(4)
        self.peagene.setValue(40)
        self.peagene.valueChanged.connect(self.peacalc)

        self.datalayout.addRow('原豌基因进化', self.peagene)

        self.peaboost = QLabel()
        self.datalayout.addRow(self.peaboost)

        self.peadmgbox = QLCDNumber()
        self.peadmgbox.display(self.peadmg)
        self.peadmgbox.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)


        self.reddmgbox = QLCDNumber()
        self.reddmgbox.display(self.reddmg)
        self.reddmgbox.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.purpledmgbox = QLCDNumber()
        self.purpledmgbox.display(self.purpledmg)
        self.purpledmgbox.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.datalayout.addRow(self.line)
        self.datalayout.addRow('无火炬单发伤害', self.peadmgbox)
        self.datalayout.addRow('红火单发伤害', self.reddmgbox)
        self.datalayout.addRow('紫火单发伤害', self.purpledmgbox)

        self.leftlayout.addLayout(self.datalayout)

        #self.mainlayout.addLayout(self.leftlayout)

        self.rightlayout = QVBoxLayout()

        self.bosslayout = QFormLayout()

        self.BossSelection = QComboBox()
        self.BossSelection.addItems(self.bosslist)
        self.BossSelection.setCurrentText(self.bosslist[self.getcurrent()])
        self.BossSelection.currentTextChanged.connect(self.bosscalc)

        self.bosslayout.addRow('  Boss', self.BossSelection)
        self.bosslayout.addRow(self.datastack)
        self.datastack.setCurrentIndex(self.state)



        self.copyright = QLabel('iOS-独特的萝卜伞')
        self.copyright.setProperty('info', 'copy')

        self.copybtn = QPushButton('拷贝所选区域')
        self.copybtn.setProperty('name', 'copy')
        self.copybtn.clicked.connect(self.copy)

        self.bosslayout.addRow(self.copybtn)
        self.bosslayout.addRow(self.line)
        #self.bosslayout.addRow(self.copyright)

        self.rightlayout.addLayout(self.bosslayout)
        #self.mainlayout.addLayout(self.rightlayout)

        self.left = QWidget()
        self.left.setLayout(self.leftlayout)
        self.right = QWidget()
        self.right.setLayout(self.rightlayout)
        self.splitter = QSplitter()
        self.leftstack = QStackedWidget(self)
        self.leftstack.addWidget(self.left)
        self.rightstack = QStackedWidget(self)
        self.rightstack.addWidget(self.right)
        self.splitter.addWidget(self.leftstack)
        self.splitter.addWidget(self.rightstack)
        self.splitter.setSizes([150,300])
        self.splitter.setHandleWidth(15)
        self.totallayout.addWidget(self.splitter)

        self.central.setLayout(self.totallayout)
        #self.setFont(self.sysfont)
        self.setCentralWidget(self.central)

    def setpeaUI(self):
        self.peabosslayout = QFormLayout()

        self.fire = QComboBox()
        self.fire.addItems(['无','红火','紫火'])
        self.fire.setCurrentText('紫火')
        self.fire.currentTextChanged.connect(self.bosscalc)
        self.peabosslayout.addRow('火炬',self.fire)

        self.showform = QComboBox()
        self.showform.addItems(['大招数', '子弹发数'])
        self.showform.currentTextChanged.connect(self.bosscalc)
        self.peabosslayout.addRow('显示方式',self.showform)

        self.pearesult = QTableWidget(self)
        self.pearesult.setColumnCount(4)
        self.pearesult.setRowCount(29)
        self.pearesult.setHorizontalHeaderLabels(['无原豌', '无火炬', '红火', '紫火'])
        self.pearesult.setVerticalHeaderLabels([f'第{x * 5 + 5}关' for x in range(29)])
        self.pearesult.setItemDelegate(self.delegate)
        self.peabosslayout.addRow(self.pearesult)
        self.pearesult.setFont(self.sysfont)

        self.peastack.setLayout(self.peabosslayout)

    def setwitchUI(self):
        self.witchbosslayout = QVBoxLayout()

        self.witchresult = QTableWidget(self)
        self.witchresult.setColumnCount(4)
        self.witchresult.setRowCount(29)
        self.witchresult.setHorizontalHeaderLabels(['无原豌','无火炬','红火','紫火'])
        self.witchresult.setVerticalHeaderLabels([f'第{x*5+5}关' for x in range(29)])
        self.witchresult.setItemDelegate(self.delegate)
        self.witchbosslayout.addWidget(self.witchresult)
        self.witchresult.setFont(self.sysfont)
        self.witchstack.setLayout(self.witchbosslayout)


    def witchcalc(self):
        if self.calcflag:
            atk = (100 + self.witchatkfamily.value() + self.witchclockdict[self.witchclock.currentText()][0] + self.tooldict[self.tool.currentText()][0]) / 100
            #magic = (100 + self.witchmagicfamily.value() + self.witchclockdict[self.witchclock.currentText()][1]) / 100
            magic = (100 + self.witchclockdict[self.witchclock.currentText()][1]) / 100
            self.witchdmg = math.floor(magic * atk * 3600)
            self.witchboost.setText(f'(攻击力={str(atk)[0:6]}倍      魔法伤害={str(magic)[0:6]}倍)')
            self.witchlabel.display(self.witchdmg)
            self.bosscalc()

    def bosscalc(self):
        if self.calcflag:
            self.paste = ''
            if self.state == 0:
                blood = len(self.hpdict[self.BossSelection.currentText()])
                hplist = list(self.hpdict[self.BossSelection.currentText()])
                hplist.append(hplist[0] + hplist[1])
                self.pearesult.setColumnCount(blood+1)
                if blood == 5:
                    self.pearesult.setHorizontalHeaderLabels(['第一管血','第二管血','第三管血','第四管血','第五管血','前二血'])
                else:
                    self.pearesult.setHorizontalHeaderLabels(['第一管血', '第二管血', '第三管血', '前二血'])
                if self.fire.currentText() == '无':
                    dmg = self.peadmg
                elif self.fire.currentText() == '红火':
                    dmg = self.reddmg
                else:
                    dmg = self.purpledmg
                if self.showform.currentText() == '大招数':
                    dmg*=5
                for column in range(blood+1):
                    for row in range(29):
                        hp = hplist[column] * (3 * row + 1)
                        item = QTableWidgetItem(str(math.ceil(hp/dmg)))
                        self.pearesult.setItem(row, column, item)
            elif self.state == 1:
                basehp = self.hpdict[self.BossSelection.currentText()][0]
                for level in range(29):
                    lvlhp = basehp * (level * 3 + 1)
                    nopea = str(math.ceil(lvlhp / self.witchdmg))
                    withpea = str(math.ceil(max(0,(lvlhp - self.peadmg)) / self.witchdmg))
                    withred = str(math.ceil(max(0,(lvlhp - self.reddmg)) / self.witchdmg))
                    withpurple = str(math.ceil(max(0, (lvlhp - self.purpledmg)) / self.witchdmg))
                    self.witchresult.setItem(level, 0, QTableWidgetItem(nopea))
                    self.witchresult.setItem(level, 1, QTableWidgetItem(withpea))
                    self.witchresult.setItem(level, 2, QTableWidgetItem(withred))
                    self.witchresult.setItem(level, 3, QTableWidgetItem(withpurple))

    def peacalc(self):
        if self.calcflag:
            atkboost = (120 + self.peagene.value() + self.peaclockdict[self.peaclock.currentText()][0] + self.tooldict[self.tool.currentText()][1] + self.peafamily.value()) / 100
            fireboost = (100 + self.peaclockdict[self.peaclock.currentText()][1]) / 100
            self.peaboost.setText(f'(攻击力={str(atkboost)[0:6]}倍      火焰伤害={str(fireboost)[0:6]}倍)')
            self.peadmg = math.floor(6000 * atkboost)
            self.reddmg = math.floor(9000 * atkboost * fireboost)
            self.purpledmg = math.floor(15000 * atkboost * fireboost)
            self.peadmgbox.display(self.peadmg)
            self.reddmgbox.display(self.reddmg)
            self.purpledmgbox.display(self.purpledmg)
            self.bosscalc()

    def switch(self):
        if self.peabtn.isChecked():
            self.state = 0
        else:
            self.state = 1
        self.datastack.setCurrentIndex(self.state)
        self.bosscalc()

    def copy(self):
        self.current = [self.pearesult,self.witchresult][self.state]
        rows = [i.row() for i in self.current.selectedIndexes()]
        columns = [i.column() for i in self.current.selectedIndexes()]
        indexes = [(i.row(), i.column()) for i in self.current.selectedIndexes()]
        items = self.current.selectedItems()
        columnrange = (min(columns),max(columns))
        self.paste = '\t'
        if self.state == 0:
            if self.BossSelection.currentText()=='摇滚':
                self.paste+='\t'.join(['第一管血','第二管血','第三管血','第四管血','第五管血','前二血'][columnrange[0]:columnrange[1]+1])
            else:
                self.paste+='\t'.join(['第一管血','第二管血','第三管血','前二血'][columnrange[0]:columnrange[1]+1])
        else:
            self.paste+='\t'.join(['无原豌','无火炬','红火','紫火'][columnrange[0]:columnrange[1]+1])
        self.paste+='\n'
        for row in range(min(rows),max(rows)+1):
            self.line = f'第{row * 5 + 5}关\t'
            for column in range(columnrange[0],columnrange[1]+1):
                if (row,column) in indexes:
                    self.line+=items[indexes.index((row,column))].text()
                    self.line+='\t'
                else:
                    self.line+='\t'
            self.paste+=self.line[:-1]
            self.paste+='\n'
        self.paste = self.paste[:-1]
        pyperclip.copy(self.paste)

    def getcurrent(self):
        t = datetime.datetime.now()
        self.time = datetime.date(t.year, t.month, t.day)
        year = self.time.year
        date = datetime.date(year, 1, 1)
        date += datetime.timedelta(days=(11 - date.isoweekday()) % 7)
        ind = 0
        while (self.time - date).days >= 7:
            ind += 1
            ind %= 13
            date += datetime.timedelta(days=7)
        if 1 <= self.time.isoweekday() <= 3:
            ind += 1
            ind %= 13
        return (ind + 1) % 13

    def closeEvent(self, QCloseEvent):
        f=open('data.txt','w')
        f.write(str(self.peafamily.value())+'\n'+str(self.witchatkfamily.value()))
        f.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Main()
    fontsize = 16
    qss = '* {font: ' + str(fontsize)+'px}\nQLabel {font: '+str(fontsize)+"px}\nQPushButton[name = 'copy'] {font: "+str(fontsize)+"px}"
    qss += '''QLabel[name='line'] {font: 1px}'''
    #demo.setStyleSheet(qss)
    # set css for app
    demo.show()
    sys.exit(app.exec())