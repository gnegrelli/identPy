# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:44:01 2017

@author: Gabriel
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


import Tkinter as tk
import ttk

from matplotlib import pyplot as plt

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = Figure()
a = f.add_subplot(212)

exchange = "BTC-e"
DatCounter = 9000
programName = "btce"

resampleSize = "15Min"
dataPace = "1d"
candleWidth = 0.008
topIndicator = "none"
middleIndicator = "none"
bottomIndicator = "none"
EMAs = []
SMAs = []

def addTopIndicator(what):
    global topIndicator
    global DatCounter
    
    if dataPace == "tick":
        popupmsg("indicators in tick not available")
    


def changeTimeFrame(tf):
    global dataPace
    global DatCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data")
    else:
        dataPace = tf
        DatCounter = 9000


def changeSampleSize(size,width):
    global resampleSize
    global DatCounter
    global candleWidth
    if dataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data")
    elif dataPace == "tick":
        popupmsg("You\'re in the wrong view")
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width
        


def changeExchange(toWhat,pn):
    global exchange
    global DatCounter
    global programName
    
    exchange = toWhat
    programName = pn
    DatCounter = 9000



def popupmsg(msg):
    popup = tk.Tk()        
    
    popup.wm_title("!")
    label = ttk.Label(popup, text = msg, font= NORMAL_FONT)
    label.pack(side="top", fill="x",pady=10)
    b1 = ttk.Button(popup, text="OK", command=popup.destroy)
    b1.pack()
    popup.mainloop()

def animate(i):
    pullData = open("sampleData.txt","r").read()
    dataList = pullData.split("\n")
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(",")
            xList.append(int(x))
            yList.append(int(y))
    
    a.clear()
    a.plot(xList,yList)
    

class SeaofBTCapp(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.iconbitmap(self, default="TOP.ico")
        tk.Tk.wm_title(self,"TOPzera")
        
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
                
        menuBar = tk.Menu(container)
        filemenu = tk.Menu(menuBar, tearoff = 0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        
        menuBar.add_cascade(label="File",menu=filemenu)
        
        exchangeChoice = tk.Menu(menuBar,tearoff=1)
        exchangeChoice.add_command(label="BTC-e", command = lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex", command = lambda: changeExchange("Bitfinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command = lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi", command = lambda: changeExchange("Huobi","huobi"))
        
        menuBar.add_cascade(label="Exchange",menu=exchangeChoice)
        
        dataTF= tk.Menu(menuBar,tearoff=1)
        dataTF.add_command(label="Tick",command = lambda:changeTimeFrame("tick"))
        dataTF.add_command(label="1 Day",command = lambda:changeTimeFrame("1d"))
        dataTF.add_command(label="3 Day",command = lambda:changeTimeFrame("3d"))
        dataTF.add_command(label="1 Week",command = lambda:changeTimeFrame("7d"))
        
        menuBar.add_cascade(label="Data Time Frame",menu=dataTF)
        
        OHLCI = tk.Menu(menuBar,tearoff=1)
        OHLCI.add_command(label="Tick",command = lambda:changeTimeFrame("tick"))
        OHLCI.add_command(label="1 minute",command = lambda:changeSampleSize("1Min",0.0005))
        OHLCI.add_command(label="5 minute",command = lambda:changeSampleSize("5Min",0.003))
        OHLCI.add_command(label="15 minute",command = lambda:changeSampleSize("15Min",0.008))
        OHLCI.add_command(label="30 minute",command = lambda:changeSampleSize("30Min",0.016))
        OHLCI.add_command(label="1 Hour",command = lambda:changeSampleSize("1H",0.032))
        OHLCI.add_command(label="3 Hour",command = lambda:changeSampleSize("3H",0.096))
        
        menuBar.add_cascade(label="OHLC Interval",menu = OHLCI)
        
        
        topIndi = tk.Menu(menuBar, tearoff=1)
        topIndi.add_command(label="None",command=lambda: addTopIndicator("None"))
        topIndi.add_command(label="RSI",command=lambda: addTopIndicator("rsi"))
        topIndi.add_command(label="MACD",command=lambda: addTopIndicator("macd"))
        
        menuBar.add_cascade(label="Top Indicator",menu= topIndi)
        
        mainI = tk.Menu(menuBar, tearoff=1)
        mainI.add_command(label="None",command=lambda: addMiddleIndicator("None"))
        mainI.add_command(label="SMA",command=lambda: addMiddleIndicator("sma"))
        mainI.add_command(label="EMA",command=lambda: addMiddleIndicator("ema"))
        
        menuBar.add_cascade(label="Main/Middle Indicator",menu= mainI)
        
        bottomI = tk.Menu(menuBar, tearoff=1)
        bottomI.add_command(label="None",command=lambda: addBottomIndicator("None"))
        bottomI.add_command(label="RSI",command=lambda: addBottomIndicator("rsi"))
        bottomI.add_command(label="MACD",command=lambda: addBottomIndicator("macd"))
        
        menuBar.add_cascade(label="Bottom Indicator",menu= bottomI)
        
        
        
        
        
        
        
        
        
        tk.Tk.config(self,menu=menuBar)
        
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageThree):
            
            frame = F(container,self)
            
            self.frames[F] = frame
            
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self,cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
def qf(string):
    print(string)

class StartPage(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Start Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Visit Page 1",
                            command = lambda: controller.show_frame(PageOne))
        button1.pack()
        
        button2 = ttk.Button(self,text="Visit Page 2",
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self,text="Graph Page",
                            command = lambda: controller.show_frame(PageThree))
        button3.pack()

        
class PageOne(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Page One",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self,text="Page Two",
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()

        
        
class PageTwo(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Page Two",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self,text="Page One",
                            command = lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        



        
app = SeaofBTCapp()
app.geometry("800x600")
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()