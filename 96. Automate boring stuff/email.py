#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 15:11:35 2020

@author: yukuo
"""

import smtplib

# connection obj
conn = smtplib.SMTP('smtp.gmail.com', 587)
# connect to server
conn.ehlo()
conn.starttls() # encrypt
psw = input('Enter password: ')
conn.login('ucs198604@gmail.com', psw)
text = 'Subject: hello \n\nDear Yu, this is the test message'
# conn.sendmail('ucs198604@gmail.com','ucs198604@gmail.com',text)

conn.send_message(text)
conn.quit()