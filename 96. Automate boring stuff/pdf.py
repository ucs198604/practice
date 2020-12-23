#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:59:01 2020

@author: yukuo
"""

import PyPDF2
import os

os.chdir('/Users/yukuo/Desktop/practice/96. Automate boring stuff')

pdf1 = open('pdf.pdf','rb')
pdf2 = open('pdf2.pdf','rb')

reader1 = PyPDF2.PdfFileReader(pdf1)
reader2 = PyPDF2.PdfFileReader(pdf2)

writer = PyPDF2.PdfFileWriter()


for pn in range(reader1.numPages):
    page1 = reader1.getPage(pn)
    page2 = reader2.getPage(reader1.numPages-pn-1)
    writer.addPage(page1)       
    writer.addPage(page2)       

with open('combined.pdf','wb') as f:
    writer.write(f)
    
pdf1.close()
pdf2.close()