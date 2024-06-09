from tkinter import *
from tkinter import Tk,messagebox,scrolledtext
from tkinter.ttk import *
import decimal,math,pyperclip

def roundup(n):
    return math.ceil(n)
def dec(n):
    return decimal.Decimal(n)
def clicked():
    global copy
    btn2.config(state='disabled')
    dmg=dec(30000)
    for i in atkf.get():
        if i not in'1234567890.':
            atkf.delete(0,END)
            messagebox.showinfo('Error','家族攻击力只能输入数字和一个小数点')
            return
        if atkf.get().count('.')!=0 and atkf.get().count('.')!=1:
            atkf.delete(0,END)
            messagebox.showinfo('Error','家族攻击力只能输入数字和一个小数点')
            return
    atkscale=dec(dec(atkf.get())+dec(costume.get()))
    atkscale*=dec(0.01)
    atkscale+=dec(1)
    atkscale=dec(eval(str(atkscale)))
    firescale=dec(1)
    if item.get()==0:
        atkscale+=dec(0.2)
    elif item.get()==1:
        firescale+=dec([0.1,0.12,0.16,0.2,0.24,0.27][eval(lvl.get())])
    else:
        atkscale+=dec([0.12,0.15,0.18,0.2,0.25,0.3][eval(lvl.get())])
        atkscale=dec(atkscale)
    if torch.get()==0:
        dmg=dmg*atkscale
    else:
        dmg=dmg*atkscale*dec([1,1.5,2.5][torch.get()])*dec(firescale)
    dmgshow.config(state='normal')
    dmgshow.delete(0,END)
    dmgshow.insert(0,str(round(dmg)))
    dmgshow.config(state='readonly')
    stats.config(state='normal')
    stats.delete(1.0, END)
    stats.config(state='disabled')
    copy=''
    copy+='伤害：'
    copy+=str(round(dmg))
    copy+='\n'
    if clock.get()=='摇滚':
        first,second,third,fourth,fifth=stamina[clock.get()]
        for i in range(5,149,5):
            hpscale=dec(0.6)*i-2
            text='第'+str(i)+'关：第一格血：'+str(roundup(first*hpscale/dmg))+'次；第二格血：'+str(roundup(second*hpscale/dmg))+'次；第三格血：'+str(roundup(third*hpscale/dmg))+'次；第四格血：'+str(roundup(fourth*hpscale/dmg))+'次；第五格血：'+str(roundup(fifth*hpscale/dmg))+'次；直下二血：'+str(roundup((first+second)*hpscale/dmg))+'次\n'
            stats.config(state='normal')
            stats.insert(END,text)
            stats.config(state='disabled')
            copy+=text
    else:
        first,second,third=stamina[clock.get()]
        for i in range(5,149,5):
            hpscale=dec(0.6)*i-2
            text='第'+str(i)+'关：第一格血：'+str(roundup(first*hpscale/dmg))+'次；第二格血：'+str(roundup(second*hpscale/dmg))+'次；第三格血：'+str(roundup(third*hpscale/dmg))+'次；直下二血：'+str(roundup((first+second)*hpscale/dmg))+'次\n'
            stats.config(state='normal')
            stats.insert(END,text)
            stats.config(state='disabled')
            copy+=text
    btn2.config(state='normal')
def clip():
    pyperclip.copy(copy)
window = Tk()
window.title("原豌伤害计算")
window.geometry("1130x600")
stamina={'埃及':(3750,6250,5000),'失落':(3200,4800,8000),'西部':(3835,5900,5310),'功夫':(2550,4250,5950),'未来':(3640,5320,6160),
         '黑暗':(3000,4500,7500),'沙滩':(3000,4500,6000),'冰河':(4000,4000,6400),'天空':(3500,3500,9100),'海盗':(3135,5700,6270),
         '摇滚':(2000,2400,2800,3200,4400),'恐龙':(3000,4500,7500),'摩登埃及':(450,750,600),'摩登海盗':(825,1500,1650),
         '摩登西部':(975,1500,1350),'摩登未来':(3000,4500,7500),'摩登黑暗':(3000,4500,7500)}
copy=''

lbl1 = Label(window, text="BOSS:")
lbl1.place(x=5,y=0)
clock = Combobox(window,state='readonly')
clock['values'] = ('埃及','失落','西部','功夫','未来','黑暗','沙滩','冰河','天空','海盗','摇滚','恐龙',
               '摩登埃及','摩登海盗','摩登西部','摩登未来','摩登黑暗')
clock.current(0)
clock.place(x=50,y=0)

lbl2 = Label(window, text="挂件:")
lbl2.place(x=5,y=40)
item = IntVar()
item.set(2)
item1 = Radiobutton(window, text="金肥料", value=0, variable=item)
item2 = Radiobutton(window, text="红蜡烛", value=1, variable=item)
item3 = Radiobutton(window, text="紫手套", value=2, variable=item)
item1.place(x=50,y=40)
item2.place(x=150,y=40)
item3.place(x=250,y=40)

lbl3 = Label(window, text="等级（如果需要）:")
lbl3.place(x=5,y=80)
var=IntVar()
var.set(5)
lvl = Spinbox(window, from_=0, to=5, width=10,textvariable=var,state='readonly')
lvl.place(x=120,y=80)

lbl4 = Label(window, text="火炬:")
lbl4.place(x=5,y=120)
torch=IntVar()
torch.set(2)
torch1 = Radiobutton(window, text="无火炬", value=0, variable=torch)
torch2 = Radiobutton(window, text="红火", value=1, variable=torch)
torch3 = Radiobutton(window, text="紫火", value=2, variable=torch)
torch1.place(x=50,y=120)
torch2.place(x=150,y=120)
torch3.place(x=250,y=120)

lbl5 = Label(window, text="家族攻击力:")
lbl5.place(x=5,y=160)
atkf = Entry(window, width=10)
atkf.insert(0,'45.00')
atkf.place(x=100,y=160)
lbl6 = Label(window, text="%")
lbl6.place(x=180,y=160)


lbl6 = Label(window, text="浴帽装扮:")
lbl6.place(x=5,y=200)
costume=IntVar()
costume.set(20)
costume1 = Radiobutton(window, text="有", value=20, variable=costume)
costume2 = Radiobutton(window, text="无", value=0, variable=costume)
costume1.place(x=70,y=200)
costume2.place(x=170,y=200)

btn = Button(window, text="计算",command=clicked,width=20)
btn.place(x=5,y=240)

lbl6 = Label(window, text="计算结果:",font=(None,15))
lbl6.place(x=400,y=0)
lbl7 = Label(window, text="伤害:")
lbl7.place(x=400,y=30)
lbl8 = Label(window, text="（精确到整数）")
lbl8.place(x=525,y=30)
dmgshow = Entry(window, width=10,state='readonly')
dmgshow.place(x=450,y=30)
stats=scrolledtext.ScrolledText(window, width=100, height=30)
stats.config(state='disabled')
stats.place(x=400,y=60)
btn2 = Button(window, text="一键复制",command=clip,width=10,state='disabled')
btn2.place(x=1025,y=30)
lbl9 = Label(window, text="*注意：\n1、考虑到大火球的触发概率不是100%，且有地形限制，\n计算时未将其考虑；\n2、此软件编写于版本2.6.6，后续原豌数值可能有更改。")
lbl9.place(x=5,y=300)
lbl10 = Label(window, text="By iOS-独特的萝卜伞")
lbl10.place(x=1000,y=460)
window.mainloop()
