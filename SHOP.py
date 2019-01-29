# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 16:02:06 2017
GUI
University of Sao Paulo
@author: Gabriel
"""

import Tkinter as tk
import ttk

from numpy import *
import copy

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

counter = 0

p = array([0., 0., 0., 0., 0., 0., 0., 0.])

u = 0.165

x0 = array([[1.0750, -0.3689,364.381]])

u0 = 1




dp = .001
delta_p = dp*ones_like(p)

init_time = 0.

final_time = .5

step = .0005

tolerance = .0005   #Error tolerance

err = []

evolution = None

op_real = array([])
fo = open("myFile.dat","r")
pullData = fo.read()
dataList = pullData.split("\n")
for eachLine in dataList:
    if len(eachLine) > 1:
        t, P, Q= eachLine.split(",")
        op_real = vstack((op_real, array([float(t), float(P), float(Q)]))) if op_real.size else array([float(t), float(P), float(Q)])
fo.close()
#fo.flush()

Step = None
Figs = None
TwoSteps = None
Conv = False

f = Figure(figsize=(0,0),dpi=100)

#f = Figure()
axarr0, axarr1 = None, None

dict1 = {'u0': [u"u\u2080 = %.3f", u0, 0], 'u': [u"\u0394u = %.3f", u, 1],
         'dp': [u"\u0394p = %.3f", dp,0], 't0': ["initial time = %.2f s", init_time,2],
        'tf': ["final time = %.2f s", final_time,3], 'step': ["step = %.4f s", step,4],
        'tol': ["tolerance = %.4f", tolerance,5]}
    

print dict1['u0'][0] %dict1['u0'][1]
print dict1['u'][0] %dict1['u'][1]
print dict1['dp'][0] %dict1['dp'][1]
print dict1['t0'][0] %dict1['t0'][1]
print dict1['tf'][0] %dict1['tf'][1]
print dict1['step'][0] %dict1['step'][1]
print dict1['tol'][0] %dict1['tol'][1]
print "\n\n\n"
#print op_real

def popupmsg(msg):
    popup = tk.Tk()        
    
    popup.wm_title("!")
    label = ttk.Label(popup, text = msg, font= ("Verdana", 10))
    label.pack(side="top", fill="x",pady=10)
    b1 = ttk.Button(popup, text="OK", command=popup.destroy)
    b1.pack()
    popup.mainloop()
    
def refresh(menu, option):
    popup = tk.Tk()
    popup.wm_title("!")
    
    label = ttk.Label(popup, text = "New Value: ", font= ("Verdana", 10))
    label.pack(side="top", fill="x",pady=10)
    
    entry = ttk.Entry(popup,width = 10)
    entry.pack()
    
    b2 = ttk.Button(popup, text="OK", command=lambda: click(menu, option, entry.get(), popup))
    b2.pack()
    
    popup.mainloop()

def click(menu,option,k,popup):
    global dict1
    flag = 0
    try:
        # Check conditions and try to make it a float
        if option == 't0' and float(k)>dict1['tf'][1]:
            popupmsg("Value must be smaller than %.2f" %dict1['tf'][1])
        elif option == 'tf' and float(k)<dict1['t0'][1]:
            popupmsg("Value must be greater than %.2f" %dict1['t0'][1])
        elif option == 'step' and float(k)>dict1['tf'][1]-dict1['t0'][1]:
            popupmsg("Value must be smaller than %.2f" %(dict1['tf'][1]-dict1['t0'][1]))
        else:
            dict1[option][1] = float(k)
            flag = 1
    except ValueError:
        # Print this if the input cannot be made a float
        popupmsg("Value must be a number!")
    
    if flag:
        print dict1[option][0] %dict1[option][1]
        menu.entryconfigure(dict1[option][2], label=dict1[option][0] %dict1[option][1])
        popup.destroy()

    

class SeaofBTCapp(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.iconbitmap(self, default="TOP.ico")
        tk.Tk.wm_title(self,"TOPzera")
#        tk.Tk.geometry(self,"971x600")
        
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        
        self.menuBar = tk.Menu(container)
        self.filemenu = tk.Menu(self.menuBar, tearoff = 0)
        self.filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported yet"))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=quit)
        
        self.menuBar.add_cascade(label="File",menu=self.filemenu)

        
        global u0, u
        self.inputs = tk.Menu(self.menuBar, tearoff = 0)
        self.inputs.add_command(label= u"u\u2080 = %.3f" %u0, command = lambda: refresh(self.inputs,'u0'))
        self.inputs.add_command(label= u"\u0394u = %.3f" %u, command = lambda: refresh(self.inputs,'u'))

        self.menuBar.add_cascade(label="Input Value",menu=self.inputs)
        
        global dp, init_time, final_time, step, tolerance
        self.settings = tk.Menu(self.menuBar, tearoff = 0)
        self.settings.add_command(label= u"\u0394p = %.3f" %dp, command = lambda: refresh(self.settings,'dp'))
        self.settings.add_separator()
        self.settings.add_command(label= "initial time = %.2f s" %init_time, command = lambda: refresh(self.settings,'t0'))
        self.settings.add_command(label= "final time = %.2f s" %final_time, command = lambda: refresh(self.settings,'tf'))
        self.settings.add_command(label= "step = %.4f s" %step, command = lambda: refresh(self.settings,'step'))
        self.settings.add_command(label= "tolerance = %.4f" %tolerance, command = lambda: refresh(self.settings,'tol'))

        self.menuBar.add_cascade(label="Settings",menu=self.settings)
        
        tk.Tk.config(self,menu=self.menuBar)
        
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageThree, PageThreeNotStep):
            
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
        
        label = tk.Label(self,text="Start Page",font=("Verdana", 12))
        label.pack(pady=10,padx=10)
        
        nxtBtn = tk.Button(self,text="Start",
                            command = lambda: controller.show_frame(PageOne))
        nxtBtn.pack()


class PageOne(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        name_lbl = tk.Label(self, text = "Parameters")
        name_lbl.grid(row = 0)
        
        self.x = tk.StringVar(value='0.21')
        self.xl = tk.StringVar(value='0.05')
        self.To = tk.StringVar(value='0.1')
        self.M = tk.StringVar(value='0.01')
        self.Gs = tk.StringVar(value='4')
        self.Bs = tk.StringVar(value='3')
        self.E0 = tk.StringVar(value='1.1')
        self.del0 = tk.StringVar(value='-0.37')
        
        x_lbl = tk.Label(self, text = "X")
        x_lbl.grid(row = 1, column = 0)
        x_val = tk.Entry(self, width = 10, textvariable = self.x)
        x_val.grid(row = 1, column = 1)
        
        xl_lbl = tk.Label(self, text = "X'")
        xl_lbl.grid(row = 2, column = 0)
        xl_val = tk.Entry(self, width = 10, textvariable = self.xl)
        xl_val.grid(row = 2, column = 1)

        To_lbl = tk.Label(self, text = u"T\u2080")
        To_lbl.grid(row = 3, column = 0)
        To_val = tk.Entry(self, width = 10, textvariable = self.To)
        To_val.grid(row = 3, column = 1)

        
        M_lbl = tk.Label(self, text = "M")
        M_lbl.grid(row = 4, column = 0)
        M_val = tk.Entry(self, width = 10, textvariable = self.M)
        M_val.grid(row = 4, column = 1)
        
        Gs_lbl = tk.Label(self, text = u"G\u209B")
        Gs_lbl.grid(row = 5, column = 0)
        Gs_val = tk.Entry(self, width = 10, textvariable = self.Gs)
        Gs_val.grid(row = 5, column = 1)
        
        Bs_lbl = tk.Label(self, text = u"B\u209B")
        Bs_lbl.grid(row = 6, column = 0)
        Bs_val = tk.Entry(self, width = 10, textvariable = self.Bs)
        Bs_val.grid(row = 6, column = 1)
        
        E0_lbl = tk.Label(self, text = u"E'\u2080")
        E0_lbl.grid(row = 7, column = 0)
        E0_val = tk.Entry(self, width = 10, textvariable = self.E0)
        E0_val.grid(row = 7, column = 1)
        
        del0_lbl = tk.Label(self, text = u"\u03B4\u2080")
        del0_lbl.grid(row = 8, column = 0)
        del0_val = tk.Entry(self, width = 10, textvariable = self.del0)
        del0_val.grid(row = 8, column = 1)
        
        
        button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.grid(row = 9, column = 0)
        
        button2 = ttk.Button(self,text="Next",
                            command = lambda: self.click(controller))
        button2.grid(row = 9, column = 1)

        
    def click(self,controller):
        self.flg = 0
        
        global evolution
        
        try:
            # Try to make it a float
            p[0] = float(self.x.get())
            p[1] = float(self.xl.get())
            p[2] = float(self.To.get())
            p[3] = float(self.M.get())
            p[4] = float(self.Gs.get())
            p[5] = float(self.Bs.get())
            p[6] = float(self.E0.get())
            p[7] = float(self.del0.get())
            evolution = copy.copy(p)
            self.flg = 1
        except ValueError:
            # Print this if the input cannot be made a float
            popupmsg("Parameters must be numbers")
        
        if self.flg == 1:            
            controller.show_frame(PageTwo)


class PageTwo(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.flags = tk.Label(self, text = "Flags")
        self.flags.pack(side = "top")
        
        
        self.PntFigs = tk.BooleanVar()
        self.Step = tk.BooleanVar()
        self.MS = tk.BooleanVar()
        self.TwoSteps = tk.BooleanVar()
        
        
        self.chk_step = tk.Checkbutton(self, text = "Step by Step", variable = self.Step, command = self.cb)
        self.chk_step.pack(side = "top")
        
        self.chk_fig = tk.Checkbutton(self, text = "Print Figures",variable = self.PntFigs, state="disabled")
        self.chk_fig.pack(side = "top")
        
#        self.chk_MS = tk.Checkbutton(self, text = "Master-Slave Coupling", variable = self.MS, command = self.MScmd)
#        self.chk_MS.pack(side = "top")
        
        self.chk_2S = tk.Checkbutton(self, text = "2-Step Ident.", variable = self.TwoSteps)
        self.chk_2S.pack(side = "top")
        
        
        self.button1 = ttk.Button(self,text="Back",
                            command = lambda: controller.show_frame(PageOne))
        self.button1.pack()

        self.button2 = ttk.Button(self,text="Next",
                            command = lambda: self.suma(controller))
        self.button2.pack()

    def suma(self, controller):
        
        global Step, Figs, TwoSteps
        global axarr0, axarr1
        global u,u0,dp,init_time,final_time,step,tolerance,dict1,delta_p
        print "PRIMEIRA ETAPA\n"        
        print u, u0
        
        u,u0,dp,init_time,final_time,step,tolerance = array([[dict1['u'][1]]]),array([dict1['u0'][1]]),dict1['dp'][1],dict1['t0'][1],dict1['tf'][1],dict1['step'][1],dict1['tol'][1]
        delta_p = dp*ones_like(p)
        print "\n\nSEGUNDA ETAPA\n"
        print u, u0
        
        Step = self.Step.get()
        Figs = self.PntFigs.get()
        TwoSteps = self.TwoSteps.get()
        
        controller.inputs.entryconfig(u"u\u2080 = %.3f" %u0, state="disabled")
        controller.inputs.entryconfig(u"\u0394u = %.3f" %u, state="disabled")
        controller.settings.entryconfig(u"\u0394p = %.3f" %dp, state="disabled")
        controller.settings.entryconfig("initial time = %.2f s" %init_time, state="disabled")
        controller.settings.entryconfig("final time = %.2f s" %final_time, state="disabled")
        controller.settings.entryconfig("step = %.4f s" %step, state="disabled")
        controller.settings.entryconfig("tolerance = %.4f" %tolerance, state="disabled")
        
        if Figs:
            axarr0 = f.add_subplot(211)
            axarr1 = f.add_subplot(212)
        
        runfile('Precalc.py')
        Precalc()
        if Step:
            controller.show_frame(PageThree)
        else:
            runfile('LoadModel2.py')
            LoadModel2()
            controller.show_frame(PageThreeNotStep)

        
    def cb(self):
        
        if self.Step.get():
            self.chk_fig.config(state="normal")
        else:
            self.chk_fig.deselect()
            self.chk_fig.config(state="disabled")
            
    
    def MScmd(self):
        popupmsg("Not implemented yet!")
            
            
class PageThree(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Page",font=("Verdana", 12))
        label.pack(pady=10,padx=10)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self.button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: self.backHome(controller))
        self.button1.pack()
        
        self.button2 = ttk.Button(self,text="Iterate",
                            command = lambda: self.iterate())
        self.button2.pack()
        
        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
    
    def iterate(self):
        global Conv
        runfile('LoadModel2.py')
        LoadModel2()
        if Conv:
            self.button2.config(state = "disabled")
    
    def backHome(self, controller):
        global Conv, err, counter
        Conv = False
        err = []
        counter = 0
        self.button2.config(state = "normal")
        
        controller.inputs.entryconfig(u"u\u2080 = %.3f" %u0, state="normal")
        controller.inputs.entryconfig(u"\u0394u = %.3f" %u, state="normal")
        controller.settings.entryconfig(u"\u0394p = %.3f" %dp, state="normal")
        controller.settings.entryconfig("initial time = %.2f s" %init_time, state="normal")
        controller.settings.entryconfig("final time = %.2f s" %final_time, state="normal")
        controller.settings.entryconfig("step = %.4f s" %step, state="normal")
        controller.settings.entryconfig("tolerance = %.4f" %tolerance, state="normal")
        
        controller.show_frame(StartPage)
        
        
class PageThreeNotStep(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.button1 = ttk.Button(self,text="Back to Home",
                            command = lambda: self.backHome(controller))
        self.button1.pack()
        
    def backHome(self, controller):
        global Conv, err, counter, p
        Conv = False
        err = []
        counter = 0
        print p
        
        controller.inputs.entryconfig(u"u\u2080 = %.3f" %u0, state="normal")
        controller.inputs.entryconfig(u"\u0394u = %.3f" %u, state="normal")
        controller.settings.entryconfig(u"\u0394p = %.3f" %dp, state="normal")
        controller.settings.entryconfig("initial time = %.2f s" %init_time, state="normal")
        controller.settings.entryconfig("final time = %.2f s" %final_time, state="normal")
        controller.settings.entryconfig("step = %.4f s" %step, state="normal")
        controller.settings.entryconfig("tolerance = %.4f" %tolerance, state="normal")
            
        controller.show_frame(StartPage)


app = SeaofBTCapp()
app.mainloop()