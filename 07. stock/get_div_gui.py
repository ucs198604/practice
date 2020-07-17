#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:59:44 2020

@author: yukuo
"""

import tkinter as tk
#import requests
#from lxml import html
import bs4
#import selenium
from selenium import webdriver
import re

# headless
from selenium.webdriver.chrome.options import Options
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')

# 指定 chromedriver location, create browser object, add headless option
chromedriver = '/usr/local/bin/chromedriver'
# chromedriver = "C:\webdriver\chromedriver.exe"
browser = webdriver.Chrome(chromedriver, options=chrome_options)




# 對應 text
text_all =[
"股利發放年度",
"股利所屬盈餘期間",
"股東會日期",
"除息交易日",  # 除息日程
"除息參考價", 
"填息完成日", 
"填息花費日數", 
"現金股利發放日", 
"除權交易日", # 除權日程
"除權參考價", 
"填權完成日", 
"填權花費日數", 
"現金股利盈餘",
"現金股利公積",
"現金股利合計",
"股票股利盈餘",
'股票股利公積',
"股票股利合計",
"股利合計"]


def get_div():
    # input position
    #positions = '0050,006208,00692,1216,1402,2317,2832,2887,2888'
    positions = stock_entry_text.get()
    positions = positions.split(',')
    list_dict_info = []  # dict of stock
        # clear
    out_put.delete(1.0, tk.END)
    
    for pos in positions:
        pos = pos.strip()

        try:
            div_url = 'https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID='
            browser.get(div_url+pos)
            htmltext = browser.page_source
            soup = bs4.BeautifulSoup(htmltext,'lxml')
            
            # search for title
            pattern = r'\((\d+)\) (\w*) '
            title_text = soup.title.text[:]
            title_tuple = re.findall(pattern,title_text)[0]
            dict_info = {}
            
            # 內容
            contents = soup.select('#divDetail')[0].select('#row0')[0].select('td')
            
            if contents == []:
                out_put.insert(tk.INSERT, '\n')
                out_put.insert(tk.INSERT, f'查詢 {pos} 時發生錯誤')
            else:
                dict_info = {title:value.text for title, value in zip(text_all,contents)}
                
                # append ticker/name
                dict_info['ticker'] = title_tuple[0]  # 'ticker' = '0050'
                dict_info['name'] = title_tuple[1] # 'name' = '統一'
                
                list_dict_info.append(dict_info)
            
        except:
            #print(f'查尋 {pos} 時發生錯誤')
            out_put.insert(tk.INSERT, '\n')
            out_put.insert(tk.INSERT, f'查詢 {pos} 時發生錯誤')
        

    
    for item in list_dict_info:
        ticker_name = f"[{item['ticker']}/{item['name']}]"
        ticker_name = ticker_name+ chr(12288)*(16-len(ticker_name))
        item['除息交易日']= '20'+item['除息交易日'].replace(r"'",r'/') if item['除息交易日']!='' else item['除息交易日']
        
        out_put_text = f"【{item['股利發放年度']}】{ticker_name} 股利合計 {item['股利合計']}   除息交易日 {item['除息交易日']}"
        #print(out_put_text)
        
        # out put
        out_put.insert(tk.INSERT, '\n')
        out_put.insert(tk.INSERT, out_put_text)
    
    return list_dict_info


window = tk.Tk()
window.title('Get div')

# entry text
stock_entry_text = tk.StringVar()
stock_entry = tk.Entry(window, textvariable=stock_entry_text, width=60)
stock_entry.grid(column=0, row=0)

# search bt
search_b = tk.Button(window, text='搜尋', command=get_div)
search_b.grid(row=0,column=1)

# 先 scrollbar=, 再 text
scrollbar = tk.Scrollbar(window)
scrollbar.grid(column=2, row=1, sticky=tk.N+tk.S+tk.W)

out_put = tk.Text(window,font='黑體 14', width = 65)
out_put.grid(column=0, row=1, sticky = tk.W, columnspan=2)

# 指定 scrollbar command and text command
scrollbar.config(command=out_put.yview)
out_put.config(yscrollcommand=scrollbar.set)

#window.bind('<Control-y>',Main_Window.ctrl_y)  # 寫在 class 外

window.lift()
# let the window be on the top
window.attributes("-topmost", True)

window.mainloop()
