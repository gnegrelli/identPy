# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 02:45:13 2017

@author: Gabriel
"""

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x

class ButtonForLoop():
    def __init__(self, top):
        self.top=top
        self.but_1=tk.Button(top, text="Start for()", command=self.start_for)
        self.but_1.grid(row=0, column=0)

        self.num_for=0
        ## for simplicity, assume 3 iterations through the loop
        self.max_num=3

    def next_pass(self):
        ## create button again
        self.but_1=tk.Button(top, text="Pass # %d" % (self.num_for),
                             command=self.start_for)
        self.but_1.grid(row=0, column=0)

    def start_for(self):
        """ button clicked so call next_pass() the correct
            number of iterations
        """
        ## destroy whatever button is showing
        self.but_1.destroy()
        if self.num_for < self.max_num:
            self.num_for += 1
            self.top.after(500, self.next_pass)
        else:
            self.top.quit()

top=tk.Tk()
BF=ButtonForLoop(top)
top.mainloop()

