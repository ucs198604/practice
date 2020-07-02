#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 20:25:16 2020

@author: yukuo
"""

import Schedule

Schedule.main()

#%%

print(df.loc['Weekday_ch'].iloc[5:].tolist())

WEEK_DAY_LIST = df.loc['Weekday_ch'].iloc[5:].tolist()
DAYS = len(WEEK_DAY_LIST)
DAY_LIST = [str(i+1) for i in range(DAYS)]
WEEK_DAY_DICT = {date:weekday for date,weekday in zip(DAY_LIST,WEEK_DAY_LIST)}
print(WEEK_DAY_DICT)