import Tkinter as tk

top = tk.Tk()
top.title("TOPzera")
top.geometry("971x600")
top.wm_iconbitmap("TOP.ico")

#Frames
top_left = tk.PanedWindow(top)
top_left.place(relx=0, rely=0,relheight=.2, relwidth=.5)

top_right = tk.PanedWindow(top)
top_right.place(relx = .5, rely = 0, relheight=.2, relwidth=.5)

mid_left = tk.PanedWindow(top)
mid_left.place(relx=0, rely=0.2,relheight=.7, relwidth=.5)

mid_right = tk.PanedWindow(top)
mid_right.place(relx=0.5, rely=0.2,relheight=.7, relwidth=.5)

btm = tk.PanedWindow(top)
btm.place(relx=0, rely=0.9,relheight=.1, relwidth=1)

#Frame 1

name_lbl = tk.Label(top_left, text = "Name: ")
name_lbl.grid(row = 0, column = 0)
name = tk.Entry(top_left,width = 30)
name.grid(row = 0, column = 1)

x_lbl = tk.Label(top_left, text = "Number of states: ")
x_lbl.grid(row = 1, column = 0)
x = tk.Entry(top_left,width = 30)
x.grid(row = 1, column = 1)

y_lbl = tk.Label(top_left, text = "Number of exits: ")
y_lbl.grid(row = 2, column = 0)
y = tk.Entry(top_left,width = 30)
y.grid(row = 2, column = 1)

p_lbl = tk.Label(top_left, text = "Number of parameters: ")
p_lbl.grid(row = 3, column = 0)
p = tk.Entry(top_left,width = 30)
p.grid(row = 3, column = 1)


#Frame 2

flags = tk.Label(top_right, text = "Flags")
flags.pack()

chk_fig = tk.Checkbutton(top_right, text = "Print Figures")
chk_fig.pack()

chk_step = tk.Checkbutton(top_right, text = "Step by Step",state="disabled")
chk_step.pack()

chk_MS = tk.Checkbutton(top_right, text = "Master-Slave Method")
chk_MS.pack()


#Frame 3

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


#Frame 4

matr = tk.Label(mid_right, text = "Matrices")
matr.pack()


#Frame 5

go_btn = tk.Button(btm, text = "GO!", activebackground = "green")
go_btn.pack()





top.mainloop()




"""




f = tk.Button(top, text = "Monty", activebackground = "green")
w = tk.Button(top, text = "SPAM", activeforeground = "cyan")
f.pack(fill = tk.X)
w.pack()
top.mainloop()

"""