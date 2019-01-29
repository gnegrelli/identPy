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

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5),dpi=100)
a = f.add_subplot(111)

#pf = tk.IntVar()
nparame = 0
parameters = []


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
#        tk.Tk.geometry(self,"971x600")
        
#        nparame = tk.IntVar()
#        nparam = 0
        
        container = tk.Frame(self)
        
        container.pack(side="top",fill="both",expand=True)
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            
            frame = F(container,self)
            
            self.frames[F] = frame
            
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self,cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Start Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        nxtBtn = tk.Button(self,text="Start",
                            command = lambda: controller.show_frame(PageOne))
        nxtBtn.pack()
        
#        container = tk.Frame(self)
#        
#        self.pans = {}
#        count = 0
#        
#        for P in (tl,tr,ml,mr,b):
#            pan = P(container,self)
#            self.pans[P] = pan
#            pan.grid(row = count/2, column = count%2, sticky = "nsew")
#            count += 1
            
class ml(tk.PanedWindow):
    
    def __init__(self,parent,controller):
        tk.PanedWindow.__init__(self,parent)
        
        param = tk.Label(self, text = "Parameters")
        param.pack()
        pframe = tk.Frame(self)
        pframe.pack()
        p1_lbl = tk.Label(pframe, text = "p1: ")
        p1_lbl.grid(row = 0, column = 0)
        p1_nm = tk.Entry(pframe,width = 15)
        p1_nm.grid(row = 0, column = 1)
        p1_vl = tk.Entry(pframe,width = 15)
        p1_vl.grid(row = 0, column = 2)
        
        p2_lbl = tk.Label(pframe, text = "p2: ")
        p2_lbl.grid(row = 1, column = 0)
        p2_nm = tk.Entry(pframe,width = 15)
        p2_nm.grid(row = 1, column = 1)
        p2_vl = tk.Entry(pframe,width = 15)
        p2_vl.grid(row = 1, column = 2)
        
class mr(tk.PanedWindow):
    
    def __init__(self,parent,controller):
        tk.PanedWindow.__init__(self,parent)
        
        matr = tk.Label(self, text = "Matrices")
        matr.pack()
        
        
class b(tk.PanedWindow):
    
    def __init__(self,parent,controller):
        tk.PanedWindow.__init__(self,parent)
        
        go_btn = tk.Button(self, text = "GO!", activebackground = "green",command = lambda: controller.show_frame(PageOne))
        go_btn.pack()
             
"""
        param = tk.Label(mid_left, text = "Parameters")
        param.pack()
        pframe = tk.Frame(mid_left)
        pframe.pack()
        p1_lbl = tk.Label(pframe, text = "p1: ")
        p1_lbl.grid(row = 0, column = 0)
        p1_nm = tk.Entry(pframe,width = 15)
        p1_nm.grid(row = 0, column = 1)
        p1_vl = tk.Entry(pframe,width = 15)
        p1_vl.grid(row = 0, column = 2)
        
        p2_lbl = tk.Label(pframe, text = "p2: ")
        p2_lbl.grid(row = 1, column = 0)
        p2_nm = tk.Entry(pframe,width = 15)
        p2_nm.grid(row = 1, column = 1)
        p2_vl = tk.Entry(pframe,width = 15)
        p2_vl.grid(row = 1, column = 2)
        
"""
"""
        matr = tk.Label(mid_right, text = "Matrices")
        matr.pack()
        
        
        
        go_btn = tk.Button(btm, text = "GO!", activebackground = "green",command = lambda: controller.show_frame(PageOne))
        go_btn.pack()
        
    def enable_step(self,var):
        if var:
            self.chk_step.toggle()
"""
        
        
        
        
        
"""

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

"""
        
        
class PageOne(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.nstate = tk.IntVar()
        self.nexit = tk.IntVar()
        self.nparam = tk.IntVar()
        
        
        name_lbl = tk.Label(self, text = "Name: ")
        name_lbl.grid(row = 0, column = 0)
        name = tk.Entry(self,width = 30)
        name.grid(row = 0, column = 1)
        
        x_lbl = tk.Label(self, text = "Number of states: ")
        x_lbl.grid(row = 1, column = 0)
        x = tk.Spinbox(self, from_=0, to=10,width = 10, textvariable = self.nstate)
        x.grid(row = 1, column = 1)
        
        y_lbl = tk.Label(self, text = "Number of exits: ")
        y_lbl.grid(row = 2, column = 0)
        y = tk.Spinbox(self, from_=0, to=10,width = 10, textvariable = self.nexit)
        y.grid(row = 2, column = 1)
        
        p_lbl = tk.Label(self, text = "Number of parameters: ")
        p_lbl.grid(row = 3, column = 0)
        self.p = tk.Spinbox(self, from_=0, to=50, width = 10, textvariable = self.nparam, command = lambda: self.kk(parent,controller))
        self.p.grid(row = 3, column = 1)
        
        
        button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.grid(row = 4, column = 0)
        
        button2 = ttk.Button(self,text="Next",
                            command = lambda: controller.show_frame(PageTwo))
        button2.grid(row = 4, column = 1)
    
    
    def kk(self, parent, controller):
        global nparame
#        nparame = self.nparam.get()
        nparame = int(self.p.get())
#        controller.frames[PageThree] = PageThree(parent, controller)
        print nparame + self.nstate.get() + self.nexit.get()
        
        

class PageTwo(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.flags = tk.Label(self, text = "Flags")
        self.flags.pack(side = "top")
        
        
        self.var = tk.IntVar()
        self.chk_fig = tk.Checkbutton(self, text = "Print Figures", variable = self.var, command = self.cb)
        self.chk_fig.pack(side = "top")
        
        self.chk_step = tk.Checkbutton(self, text = "Step by Step",state="disabled")
        self.chk_step.pack(side = "top")
        
        self.chk_MS = tk.Checkbutton(self, text = "Master-Slave Method")
        self.chk_MS.pack(side = "top")
        
        
        self.button1 = ttk.Button(self,text="Back",
                            command = lambda: controller.show_frame(PageOne))
        self.button1.pack()

        self.button2 = ttk.Button(self,text="Next",
                            command = lambda: controller.show_frame(PageThree))
        self.button2.pack()


    def cb(self):
        if self.var.get():
            self.chk_step.config(state="normal")
        else:
            self.chk_step.deselect()
            self.chk_step.config(state="disabled")
            

class PageThree(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        param = tk.Label(self, text = "Parameters")
        param.pack()
#        
#        global parameters, nparame
#        print nparame
#        
#        for i in range(0,nparame):
#            self.param = tk.Label(self, text = "p%d" %(i))
#            self.param.pack(side = "top")
#            
#            self.pvalue = tk.Entry(self)
#            self.pvalue.pack()
        
        button1 = ttk.Button(self,text="Back",
                            command = lambda: controller.show_frame(PageTwo))
        button1.pack()
        
        button2 = ttk.Button(self,text="Next",
                            command = lambda: controller.show_frame(PageFour))
        button2.pack()





class PageFour(tk.Frame):
    
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
#ani = animation.FuncAnimation(f, animate, interval = 1000)
nparam = tk.IntVar()
app.mainloop()

print nparame