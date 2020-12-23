#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:14:06 2020

@author: yukuo
"""

import pyautogui

corr = pyautogui.locateCenterOnScreen('/Users/yukuo/Desktop/practice/96. Automate boring stuff/open.png')
print(corr)
pyautogui.click(int(corr[0]/2),int(corr[1]/2))