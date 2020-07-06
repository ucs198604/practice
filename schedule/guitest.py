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
window.geometry('600x140')


# Duty box
duty_list=[]
def duty_box():
    # duty check
    global duty_list
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
    #print(duty_check, duty_list)

varC = []
for i in range(5):
    varC.append(tk.StringVar())
    varC[i].set(0)

C4 = tk.Checkbutton(window, text='CR班 (類別碼4)', variable=varC[4], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL, font=('Arial', 12))
C3 = tk.Checkbutton(window, text='ER班 (類別碼3)', variable=varC[3], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL, font=('Arial', 12))
C1 = tk.Checkbutton(window, text='CT/MR班 (類別碼1)', variable=varC[1], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL, font=('Arial', 12))
C0 = tk.Checkbutton(window, text='測試班 (類別碼0)', variable=varC[0], onvalue=1, offvalue=0,
                    command=duty_box, state = tk.NORMAL, font=('Arial', 12))

C4.grid(column=0, row=0, padx=10, pady=3, sticky=tk.W)
C3.grid(column=0, row=1, padx=10, pady=3, sticky=tk.W)
C1.grid(column=0, row=2, padx=10, pady=3, sticky=tk.W)
C0.grid(column=0, row=3, padx=10, pady=3, sticky=tk.W)


def print_selection2(scale):
    #l['text'] = scale
    pass

s = tk.Scale(window, label='', from_=50, to=300, orient=tk.HORIZONTAL,
             length=280, showvalue=0, tickinterval=50, 
             resolution=50, command=print_selection2)
s.grid(column=1, row=0, rowspan=2, columnspan =2)


# get filename and directory
#file_label = tk.Label(window, text="", bg='light gray', wraplength=100,
#                      font=('Arial', 10), width=40, height=5)
#file_label.pack()
file_var = tk.StringVar()
file_entry = tk.Entry(window, textvariable= file_var, state = 'disable', 
                      width =22, font=('Arial', 12))
file_entry.grid(column=1, row=2, rowspan=2, padx=3, pady=3)

import os
def get_filename():
    full_path = filedialog.askopenfilename(initialdir = os.getcwd(),title = "請選擇檔案",
                                          filetypes = (("xlsm files","*.xlsm"),("all files","*.*")))
    file_var.set(full_path)
    print(full_path)
    
open_file_bt = tk.Button(window, text='開啟檔案', command=get_filename, font=('Arial', 12))
open_file_bt.grid(column=2, row=2, rowspan=2)


FILE_NAME = ''
FILE_DIR = ''
NUM_TO_RUN = ''
check_start = True
def start_arrange():
    global check_start
    global duty_list
    global FILE_NAME
    global NUM_TO_RUN
    global FILE_DIR
    check_start = True
    check_l = True
    check_f =True
    if duty_list == []:
        check_start = False
        check_l = False
    if file_var.get() =='':
        check_start = False
        check_f = False
    if check_f == False and check_l == False:
        print('請選擇欲執行的值班類別與排班檔案')
    elif check_f == False:
        print('請選擇排班檔案')
    elif check_l == False:
        print('請選擇欲執行的值班類別')
    if check_start == True:
        # main, file path, duty_list, numbers to run
        FILE_NAME = file_var.get()
        NUM_TO_RUN = s.get()
        parsing = [index for index, item in enumerate(FILE_NAME) if item =="/"]
        FILE_DIR = FILE_NAME[0:(parsing[-1]+1)]
        main()
    #print(f"file path={file_var.get()}")
    #print(f"duty list={duty_list}")
    #print(f"num={s.get()}")
start_arrange = tk.Button(window, text='開始排班', command=start_arrange, font=('Arial', 14))
start_arrange.grid(column=3, row=0, columnspan=2, rowspan=4, sticky=tk.N+tk.S, padx=10, pady=20)
window.mainloop() #進入等待處理物件的狀態

# LOAD filename and numbers to run


