# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:55:23 2020

@author: User
"""

#from tkinter import * #引入tkinter
import tkinter as tk
from tkinter import filedialog

window = tk.Tk() #一個叫做window的新視窗
window.title('Duty arranger')
window.geometry('600x400')

var = tk.StringVar()
l = tk.Label(window, text="variables", bg='grey', font=('Arial', 12), width=15, height=2 )
var.set('this is a test')
l.pack()


def hit_me():
    l['text'] = e.get()
    #var.set(e.get())

b = tk.Button(window,text='Change', width=15, height=2,command=hit_me)
b.pack()   

e = tk.Entry(window, show = '*')
e.pack()

def print_selection():
    l.config(text=var2.get())

var2 = tk.StringVar()

r1 = tk.Radiobutton(window, text='Option A', variable=var2, value='A',
                    command=print_selection)
r1.pack()

def print_selection2(scale):
    l['text'] = scale

s = tk.Scale(window, label='生成組數', from_=50, to=300, orient=tk.HORIZONTAL,
             length=200, showvalue=0, tickinterval=50, 
             resolution=50, command=print_selection2)
s.pack()



# Duty box
def duty_box():
    for i in range(5):
        if int(varC[i].get())==1:
            print(f'var{i} is checked')
    # duty check
    duty_check = [int(varC[i].get()) for i in range(5)]
    # make duty list
    duty_list = [[0,1,2,3,4][i] for i,val in enumerate(duty_check) if val ==1]
    if sum(duty_check)==2:
        if int(varC[0].get()) ==0:
            C0.configure(state='disabled')
        if int(varC[1].get()) ==0:
            C1.configure(state='disabled')
        if int(varC[3].get()) ==0:
            C3.configure(state='disabled')
        if int(varC[4].get()) ==0:
            C4.configure(state='disabled')
    if sum(duty_check)<2:
        C0.configure(state='normal')
        C1.configure(state='normal')
        C3.configure(state='normal')
        C4.configure(state='normal')
    print(duty_check, duty_list)

varC = []
for i in range(5):
    varC.append(tk.StringVar())
    varC[i].set(0)

C4 = tk.Checkbutton(window, text='CR班 (類別碼4)', variable=varC[4], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL)
C3 = tk.Checkbutton(window, text='ER班 (類別碼3)', variable=varC[3], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL)
C1 = tk.Checkbutton(window, text='CT/MR班 (類別碼1)', variable=varC[1], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL)
C0 = tk.Checkbutton(window, text='測試班 (類別碼0)', variable=varC[0], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL)

C4.pack()
C3.pack()
C1.pack()
C0.pack()


# get filename and directory
#file_label = tk.Label(window, text="", bg='light gray', wraplength=100,
#                      font=('Arial', 10), width=40, height=5)
#file_label.pack()
file_var = tk.StringVar()
file_entry = tk.Entry(window, textvariable= file_var, state = 'disable', 
                      width = 40, font=('Arial', 11))
file_entry.pack()

import os
def get_filename():
    full_path = filedialog.askopenfilename(initialdir = os.getcwd(),title = "請選擇檔案",
                                          filetypes = (("xlsm files","*.xlsm"),("all files","*.*")))
    file_var.set(full_path)
    print(full_path)
    
open_file_bt = tk.Button(window, text='開啟檔案', command=get_filename)
open_file_bt.pack()


window.mainloop() #進入等待處理物件的狀態