#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 22:18:42 2020

@author: yukuo
"""

#from tkinter import *
import tkinter as tk


window = tk.Tk()
window.title('Web9 inquiry')

window.geometry('600x400')
window.resizable(0, 0)



lab = tk.Label(window, text='this is a test', relief='sunken', font='times 30 bold').pack(pady=30)
lab2 = tk.Label(window, text='this is a test', relief='sunken', font='Helvetica 18 italic bold').pack()

def change_color(color='lightblue'):
    window.config(bg=color)


# butt = Button(window, text='change', command=lambda:change_color('red')).pack()
butt = tk.Button(window, text='change', command=lambda:window.config(bg='red')).pack()

var1 = tk.StringVar()
var1.set('test')
e1 = tk.Entry(window, textvariable=var1)
e1.pack()

# 先 scrollbar=, 再 text
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

t1 = tk.Text(window,font='time 50')
t1.pack(side=tk.LEFT, fill=tk.Y)
t1.insert(tk.END, 'take me\n')
t1.insert(tk.END, "baby\n don't \n go \n away \n")

# 指定 scrollbar command and text command
scrollbar.config(command=t1.yview)
t1.config(yscrollcommand=scrollbar.set)

from tkinter import messagebox
messagebox.showinfo('test', 'testmessage')


window.mainloop()
