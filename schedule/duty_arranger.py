#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:25:04 2020

@author: yukuo
@email: ucs198604@gmail.com
"""
VERSION = 0.1

# need installation
import pandas as pd  #
import numpy as np  #
import xlwings as xw  #  also pip install xlrd
import datetime #

import random
import copy # for deep copy
import os
import warnings
warnings.filterwarnings("ignore")  
# there was UserWarning: Boolean Series key will be reindexed to match DataFrame index.


def export_to_excel(first_choice, other_choice):
    global FILE_DIR
    
    print('正在開啟Excel並輸出排班資料...')
    wb = xw.Book()
    sht = wb.sheets[0]  


    # 輸出到 excel
    sht.range('A1').value = '建議班表'
    sht.range('A2').expand().value = first_choice
    sht.autofit()
    # 定義最後一行
    last_row = wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row
    
    # 如果有 other choices, 輸出其他排班
    if other_choice!=[]:
        sht.range('A'+str(last_row+2)).value = '其他排班建議'
        for items in other_choice:
            last_row = wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row
            sht.range('A'+str(last_row+1)).expand().value = items

    now = datetime.datetime.now().strftime("%m%d%H%M%S")  # now time
    #wb.save(f'排班資料_{now}.xlsx')
    #wb.save(os.path.join(os.getcwd(), f'排班資料_{now}.xlsx'))
    wb.save(os.path.join(FILE_DIR, f'排班資料_{now}.xlsx'))

    print('儲存完成')


def formatting_for_output_31_34(optimized_31_34, tp):

    """
    input: optimized 31_34, (31 or 34), tp = 31 or 34 
    output: list of first_choices_decompose, other_choices_decompose
    formatting for 31 34 combination, not for other choices or combinations
    """
    output_list_opt = [optimized_31_34[i][0] for i in range(len(optimized_31_34))]
    final_decompose = []
    dates = ['']+[str(i) for i in range(1,len(optimized_31_34[0][0])+1)]
    for items in output_list_opt:
        temp_list = []
        if tp == 31:
        # ER/CT/MR
            ER = ['ER']+[item[0] for item in items]
            CT = ['CT']+ [item[1] for item in items]
            MR = ['MR']+ [item[2] for item in items]
            temp_list.append(dates)
            temp_list.append(ER)
            temp_list.append(CT)
            temp_list.append(MR)
        if tp == 34:
            CR = ['CR']+[item[0] for item in items]
            ER = ['ER']+ [item[1] for item in items]
            temp_list.append(dates)
            temp_list.append(CR)
            temp_list.append(ER)
        final_decompose.append(temp_list)
    
    return final_decompose[0], final_decompose[1:]


def formatting_for_output(optimized_list):
    """
    input: optimized list as a list
    output: list of first_choices_decompose, other_choices_decompose
    """
    print('正在調整格式資料格式...')
    output_list = copy.deepcopy(optimized_list)
    for i,item in enumerate(output_list):
        if item[0]!=1:
            output_list[i][0] = TYPES_OF_DUTY[item[0]]

    first_choices = [[item[0],item[1][0][0]] for item in output_list]
    other_choices = []
    for item in output_list:
        if len(item[1])>1:
            for i in range(1, len(item[1])):
                other_choices.append([item[0], item[1][i][0]])
    # 處理 duties 1, eg CT/MR, first item-> CT, second item -> MR


    for index, item in enumerate(first_choices):
        if item[0] == 1:
            CT = ['CT', [ct[0] for ct in item[1]]]
            MR = ['MR', [mr[1] for mr in item[1]]]
            #index_of_type1 = index
            first_choices[index] = MR
            first_choices.insert(index, CT)

    for index, item in enumerate(other_choices):
        if item[0] == 1:
            CT = ['CT', [ct[0] for ct in item[1]]]
            MR = ['MR', [mr[1] for mr in item[1]]]
            #index_of_type1 = index
            other_choices[index] = MR
            other_choices.insert(index, CT)

    first_choices_decompose=[]
    for item in first_choices:
        templist = []
        templist.append(item[0])
        templist.extend(data for data in item[1])
        first_choices_decompose.append(templist)
    other_choices_decompose=[]
    for item in other_choices:
        templist = []
        templist.append(item[0])
        templist.extend(data for data in item[1])
        other_choices_decompose.append(templist)
        
    # 加上日期
    first_choices_decompose.insert(0, ['']+[str(i) for i in range(1,len(first_choices_decompose[0]))])
    if other_choices_decompose!=[]:
        other_choices_decompose.insert(0, ['']+[str(i) for i in range(1,len(other_choices_decompose[0]))])

    return first_choices_decompose, other_choices_decompose


def cross_validation_31(preliminary_list):

    # cross validation for 13
    # if type1, 3 in the list

    """
    input: preliminary_list(a dictionary containing each type), get 1/3 and process
    output: filtered_full_combination_of_13, list of combination list, as a combination form
        for further optimization "optimization_for_13
    """

    print('正在進行 [ER/CT/MR班] 交叉比對')
    preliminary_df_type3 = pd.DataFrame(preliminary_list[3])
    #preliminary_df_type1 = pd.DataFrame(preliminary_list[1])
    preliminary_df_type1 = preliminary_list[1]  # 直接提取，不轉換



    # rename the index all to 1, 3, for data processing
    preliminary_df_type3.rename(index=lambda x: '3', inplace=True)
    #preliminary_df_type1.rename(index=lambda x: '1', inplace=True)

    # full list combined df, type 1 and 3 (eg. size of 500x500)
    combined3_1=[]
    no_violation_list31 = []

    for i in range(len(preliminary_df_type3)):
        t3 = pd.DataFrame(preliminary_df_type3.iloc[i])
        for j in range(len(preliminary_df_type1)):
            #t1 = pd.DataFrame(preliminary_df_type1[j], columns=['1-1','1-2'])
            t1 = pd.DataFrame(preliminary_df_type1[j], columns=['1-1','1-2'])
            flagg = False
            #cb = pd.concat([t3, t1], axis=1)
            if True in list(t3['3'].shift(1)==t1['1-1']):
#            if len(set(t3['3'].shift(1)==t1['1-1'])) == 2:  # containing True and False
                flagg = True
            elif True in list(t3['3']==t1['1-1']):
                flagg = True
            elif True in list(t3['3'].shift(-1)==t1['1-1']):
                flagg = True
            elif True in list(t3['3'].shift(1)==t1['1-2']):  # containing True and False
                flagg = True
            elif True in list(t3['3']==t1['1-2']):
                flagg = True
            elif True in list(t3['3'].shift(-1)==t1['1-2']):
                flagg = True
            if flagg == False:
                no_violation_list31.append(pd.concat([t3, t1], axis=1))
    
    if no_violation_list31 == []:
        raise ValueError("\n目前無解，請嘗試以下解決方法：\n 1.重新執行\n 2.調整排班條件\n 3.增加排班組合的產生數量")
    #print(no_violation_list31)
    
    # 資料整合
    filtered_full_combination_of_31 = [] #最後輸出 3合一，for optimization
    days_of_month = len(no_violation_list31[0])
    for filtered_items in no_violation_list31:
        one_combination_of_31 = []
        for i in range(days_of_month):
            # ie. 某組合 filtered item 的第 i 天 combination
            combination_of_each_day = filtered_items.iloc[i].tolist()
            one_combination_of_31.append(combination_of_each_day)
        filtered_full_combination_of_31.append(one_combination_of_31)

    print('已完成 [ER/CT/MR班] 交叉比對')

    return filtered_full_combination_of_31


def cross_validation_34(preliminary_list):
    # if type 3, 4 in list
    """
    input: preliminary_list(a dictionary containing each type), get 3/4 and process
    output: filtered_full_combination_of_34, list of combination list, as a form of type 1 like
        for further optimization "optimization_for_34"
    """
    
    print('正在進行 [CR/ER班] 交叉比對')
    preliminary_df_type3 = pd.DataFrame(preliminary_list[3])
    preliminary_df_type4 = pd.DataFrame(preliminary_list[4])

    # rename the index all to 3, 4, for data processing
    preliminary_df_type3.rename(index=lambda x: '3', inplace=True)
    preliminary_df_type4.rename(index=lambda x: '4', inplace=True)

    # full combine type 3 and 4 (eg. size of 500x500)
    combined3_4 = [pd.concat([preliminary_df_type3.iloc[i],preliminary_df_type4.iloc[j]], axis=1) \
                   for i in range(len(preliminary_df_type3)) for j in range(len(preliminary_df_type4))]

    # list of index for no violation
    no_violation_list34 = []
    for i in range(len(combined3_4)):
        flagg = False
        # 如果當天/前一天/後一天有值班 -> report true
        if True in list(combined3_4[i]['3'].shift(1)==combined3_4[i]['4']):
            flagg = True
        elif True in list(combined3_4[i]['3']==combined3_4[i]['4']):
            flagg = True
        elif True in list(combined3_4[i]['3'].shift(-1)==combined3_4[i]['4']):
            flagg = True
        if flagg == False:
            no_violation_list34.append(i)
    if no_violation_list34 == []:
        raise ValueError("\n目前無解，請嘗試以下解決方法：\n 1.重新執行\n 2.調整排班條件\n 3.增加排班組合的產生數量")

    filtered_full_combination_of_34 = []
    days_of_month = len(combined3_4[0])

    for filtered_num in no_violation_list34:  # filtered num of combo without violation
        one_combination_of_34 = []
        for i in range(days_of_month):
            combination_of_each_day = combined3_4[filtered_num].iloc[i].tolist()
            combination_of_each_day.reverse()
            one_combination_of_34.append(combination_of_each_day)
        filtered_full_combination_of_34.append(one_combination_of_34)
    print('已完成 [CR/ER班] 交叉比對')
    #return filtered_full_combination_of_34
    return filtered_full_combination_of_34


def data_cleansing(df):
    """
    input: df, whole data
    return: df after cleansing, define type_to_generate, sorted
    """
    #df=pd.DataFrame(df)
    #df[df['Unnamed: 2']==4]  # select Unnamed: 2 value ==4 
    # rename columns and index
    df = df.rename(columns={df.columns[0]:'Name',
                            df.columns[1]:'Code',
                            df.columns[2]:'Type',
                            df.columns[3]:'Holiday',
                            df.columns[4]:'Weekday'})
    df = df.rename(index={0:'Weekday_ch',1:'Weekday_num',2:'is_holiday'})
    # unselect unnamned coluns
    unselect_unnamed = [col for col in df if 'Unnamed' not in str(col)]  # 注意 有些還是 date type, 所以用 str
    df = df[unselect_unnamed]  

    # 有哪些班要運算，determine type_to_generate, [0-9, except 2]
    type_to_generate = sorted([int(i) for i in str(df['Name'].loc['is_holiday']) if i in '134567890'], reverse= True)
    df['Name'].loc['is_holiday'] = np.nan  # set value as NaN, not to interfere with count of hollidays


    # 將住院醫師簡碼 (iloc[4] and below)以下 code 轉為 str
    # 使用 loc 賦值不會出現  SettingWithCopyWarning: 
    # A value is trying to be set on a copy of a slice from a DataFrame 
    for i in range(4,len(df.index)):
        df.loc[i]['Code'] = str(df.loc[i]['Code'])

    # 將所有大寫轉為小寫
    lower_text = lambda item: str(item).lower() if type(item) ==str else item
    #def lower_text(item): str(item).lower() if type(item) ==str else item
    df.iloc[4:,5:len(df.columns)] = df.iloc[4:,5:len(df.columns)].applymap(lower_text)
        
    # 選擇這個範圍內，數值等於 0 者 ，轉換為 x （make compatible with CR excel sheet）
    df[df.iloc[4:,5:len(df.columns)]==0]='x'
        
    # rename date index from 1 to date
    # start from 5
    for i in range(5,len(df.columns)):
        df = df.rename(columns={df.columns[i]:str(i-4)}) 
    
    return df #,  type_to_generate # GUI, no need to define types here


def is_violation(df, duty_type_array):
    """
    input = dataframe after clensing
    output = if there's no day violation
    print where is the violation
    True -> have violation
    False -> no violation
    """
    
    print('檢查輸入資料...')
    
    # 檢查欲執行項目是否為空白, 如果空白，則 raise assertion
    if duty_type_array == []:
        raise AssertionError('請輸入要執行的班別，再執行程式')
            
    # TYPES_OF_DUTY = {1:'CT/MR', 3:'ER', 4:'CR', 5:'VS', 6:'Other', 7:'Other', 8:'Other', 9:'Other', 0:'Test'}
    is_violation = False
    days_in_month = df.loc['Weekday_num'].notnull().sum()
    num_of_holiday = df.loc['is_holiday'].notnull().sum()
    num_of_weekday = days_in_month - num_of_holiday
    
    # iterate through every duty types
    for duty_type in duty_type_array:
        # Weekday_num 非零的欄位代表當月日數
        
        # 檢查是否有重複的 簡碼 code or 空白的簡碼，either situation -> num_of_code < num_of_people
        #這個 duty type應該要有幾個人
        num_of_code = len(df[df['Type']==duty_type])  
        # 這個 duty type之下的code，不重複的有幾個
        num_of_this_type_wo_blank = len([ele for ele in df[df['Type']==duty_type]['Code'].tolist() if ele !='nan']) 
        num_of_this_type_wo_repeat = len(set([ele for ele in df[df['Type']==duty_type]['Code'].tolist() if ele !='nan'])) 
        if (num_of_this_type_wo_blank!=num_of_this_type_wo_repeat) and (num_of_code>num_of_this_type_wo_repeat):
            print(f'{TYPES_OF_DUTY[duty_type]} 班有重複的人員簡碼，請修正')
            is_violation = True
        if num_of_this_type_wo_blank<num_of_code:
            print(f'{TYPES_OF_DUTY[duty_type]} 班尚有人員簡碼未填，請修正')
            is_violation = True
        
        # if CT/MR, type1 -> doubles the days of duties
        num_of_holiday_duty = num_of_holiday *2 if duty_type ==1 else num_of_holiday
        num_of_weekday_duty = num_of_weekday *2 if duty_type ==1 else num_of_weekday

        # 假日及平日值班數
        num_of_duties_h = df[df['Type']==duty_type]['Holiday'].sum()
        num_of_duties_w = df[df['Type']==duty_type]['Weekday'].sum()

        
        # 檢查預約要值班的數目是否超過分配的值班數
        r_list = df[df['Type']==duty_type].index.tolist() # 符合 duty_type 的人員在的位置，為 iloc 的 index
        for row_num in r_list:
            # 這個人預約值班有幾項
            holiday_reserve = int((df[df['Type']==duty_type].loc[:,df.loc['is_holiday']=='v']==1).sum(axis =1)[row_num])
            holiday_assigned = df[df['Type']==duty_type]['Holiday'][row_num]
            weekday_reserve = int(df[df['Type']==duty_type][df.loc[:,df.loc['is_holiday']!='v']==1].iloc[:,5:-1].sum(axis=1)[row_num])
            weekday_assigned = df[df['Type']==duty_type]['Weekday'][row_num]
            code_of_r = df.iloc[row_num]['Code']
            
            # 如果預約要的假日值班 > 目標值班數： report error
            if holiday_reserve>holiday_assigned:
                print(f'{TYPES_OF_DUTY[duty_type]} 班代碼{code_of_r}假日班預約數為{holiday_reserve}班，超過分配上限')
                is_violation = True
            if weekday_reserve>weekday_assigned:
                print(f'{TYPES_OF_DUTY[duty_type]} 班代碼{code_of_r}平日班預約數為{weekday_reserve}班，超過分配上限')
                is_violation = True


        # 檢查值班總數是否不足， report error message and violation
        if num_of_duties_h < num_of_holiday_duty:
            print(f'{TYPES_OF_DUTY[duty_type]} 班假日值班總數不足，缺少{num_of_holiday_duty-num_of_duties_h}班')
            is_violation = True
        if num_of_duties_w < num_of_weekday_duty:
            print(f'{TYPES_OF_DUTY[duty_type]} 班平日值班總數不足，缺少{num_of_weekday_duty-num_of_duties_w}班')
            is_violation = True
            
        # 預約值班前後兩天無法值班，避免 qd，並 update 新表，以利接下來亂數產生
        # 4 to len(df.index) 會指到最後一項列
        # 5 to len(df.columns)-1 會指到最後一欄
        # 處理第一欄
        for i in range(4,len(df.index)):
            if df.iloc[i,5] == 1:
                df.iloc[i,6]='x'
        # 處理中間欄
        for i in range(4,len(df.index)):
            for j in range(6,len(df.columns)-1):
                if df.iloc[i,j]==1:
                    df.iloc[i,(j+1)]='x'
                    df.iloc[i,(j-1)]='x'
        # 處理最後一欄
        for i in range(4,len(df.index)):
            if df.iloc[i,len(df.columns)-1] == 1:
                df.iloc[i,len(df.columns)-2]='x'
        
            
        # 檢查是否有某日所有人都無法值班
        # iterate from '1' to 'end'
        for i in range(1,days_in_month+1):
            # any repeated reservation 
            # 已經在 data_cleasing 中間將 大寫轉為小寫了
            # 符合的 duty type 中 5至end處的值，有多少x or X
            # 使用 map 
            #lower_text = lambda item: str(item).lower()
            # num_of_exclude = (df[df['Type']==duty_type].iloc[:,5:][str(i)].map(lower_text)=='x').sum()
            num_of_exclude = (df[df['Type']==duty_type].iloc[:,5:][str(i)]=='x').sum()

            # 該班 R 人數
            num_of_r = len(df[df['Type']==duty_type].index)
            if num_of_exclude >= num_of_r:
                print(f'{TYPES_OF_DUTY[duty_type]} 班{i}號所有人均無法值班')
                is_violation = True       
        
        # 檢查是否有某日有兩個以上的人預約要值班
        # type 1 duty 同時兩個人值班
        if duty_type==1:
            # iterate from '1' to 'end'
            for i in range(1,days_in_month+1):
                # any repeated reservation 
                # 符合的 duty type 中 5至end處的值，是1的有多少個
                num_of_reservation = (df[df['Type']==duty_type].iloc[:,5:][str(i)]==1).sum()
                if num_of_reservation>2:
                    print(f'{TYPES_OF_DUTY[duty_type]} 班{i}號有超過2人預約要值班')
                    is_violation = True
        else:
            # iterate from '1' to 'end'
            for i in range(1,days_in_month+1):
                # any repeated reservation 
                # 符合的 duty type 中 5至end處的值，是1的有多少個
                num_of_reservation = (df[df['Type']==duty_type].iloc[:,5:][str(i)]==1).sum()
                if num_of_reservation>1:
                    print(f'{TYPES_OF_DUTY[duty_type]} 班{i}號有超過1人預約要值班')
                    is_violation = True
                
    if is_violation == False:
        print('檢查輸入資料...OK')
    else: 
        print('請修正以上資料後再執行程式')
        
    return is_violation, df


def preliminary_gen3(df_updated, duty_type, count_start):
    """
    input: df_updated or df
    generate: preliminary_list

    """
    def remove_when_not_available(added_items):
        if type(added_items) == str:
            if TODAY_IS_HOLIDAY == True:
                num_holiday_gen[add_item]-=1
                if num_holiday_gen[add_item] == 0: # if == 0, remove item
                    for holiday in LIST_OF_HOLIDAY:
                        if add_item in available_code_gen[holiday]:
                            #if add_item not in reservation_dict[holiday]: # 不必 check，因為總數可以check
                            available_code_gen[holiday].remove(add_item)
            else:
                num_weekday_gen[add_item]-=1
                if num_weekday_gen[add_item] == 0:
                    for weekday in LIST_OF_WEEKDAY:
                        if add_item in available_code_gen[weekday]:
                            #if add_item not in reservation_dict[weekday]:
                            available_code_gen[weekday].remove(add_item)
        elif type(added_items) == list:
            for itm in added_items:
                if TODAY_IS_HOLIDAY == True:
                    num_holiday_gen[itm]-=1
                    if num_holiday_gen[itm] == 0:   
                        for holiday in LIST_OF_HOLIDAY:
                            if itm in available_code_gen[holiday]:
                                #if itm not in reservation_dict[holiday]:
                                available_code_gen[holiday].remove(itm)
                else:
                    num_weekday_gen[itm]-=1
                    if num_weekday_gen[itm] == 0:
                        for weekday in LIST_OF_WEEKDAY:
                            if itm in available_code_gen[weekday]:
                                #if itm not in reservation_dict[weekday]:
                                available_code_gen[weekday].remove(itm)
            
    #sys_random = random.SystemRandom()
    # TYPES_OF_DUTY = {1:'CT/MR', 3:'ER', 4:'CR', 5:'VS', 6:'Other', 7:'Other', 8:'Other', 9:'Other', 0:'Test'}

    print('')
    print(f'正在建立 [type{duty_type},{TYPES_OF_DUTY[duty_type]}班] 初步清單...')

    # for check of holiday
    IS_HOLIDAY = df_updated.iloc[2,5:].tolist()  # list of holiday 'v' [nan, 'v'...]
    HOLIDAY_CHECK = {}
    for index,item in enumerate(IS_HOLIDAY):
        if str(item).lower() == 'v':
            HOLIDAY_CHECK[str(index+1)] = True
        else:
            HOLIDAY_CHECK[str(index+1)] = False
    LIST_OF_HOLIDAY = [key for key,item in HOLIDAY_CHECK.items() if item==True]
    LIST_OF_WEEKDAY = [key for key,item in HOLIDAY_CHECK.items() if item==False]
    holiday_index = [int(index)-1 for index in LIST_OF_HOLIDAY]
    weekday_index = [int(index)-1 for index in LIST_OF_WEEKDAY] 
    
    DAYS = len(IS_HOLIDAY) # 這個月有幾天, eg 30
    DAY_LIST = [str(i+1) for i in range(DAYS)] # 這個月的號碼 eg ['1'...'28']
    df_work = df_updated[df['Type']==duty_type]

    # 建立 int day, str day 對照表
    # combinding 2 dictionaries: z = {**x, **y}, {1:'1', '1':1}
    DAY_TABLE = {**{(i+1):str(i+1) for i in range(DAYS)}, **{str(i+1):(i+1) for i in range(DAYS)}}

    # 在 duty_type 下，的住院醫師的 code
    CODE_LIST = df_work['Code'].tolist() # code list, ['31','32']

    # 每個住院醫師有幾個假日/平日班
    num_holiday = {}
    num_weekday = {}
    available_code ={}  # dictionary

    # how many holiday/weekday for each resident
    for code in CODE_LIST:
        num_holiday[code] = df_work[df_work['Code']==code]['Holiday'].item()
        num_weekday[code] = df_work[df_work['Code']==code]['Weekday'].item()
    
    # construct available days:
    # process 預約不值班
    # note: 預約值班的前後已在 is_violation 裡面標記 'x'，所以這裡就可以直接從 available code list 裡面去掉該員，不會遺漏
    for day in DAY_LIST:
        available_code[day]= copy.deepcopy(CODE_LIST)  # 一定要使用完整拷貝，不然會變成參照，後面會全部都錯誤
        for code in CODE_LIST:
            if df_work[df_work['Code']==code][day].item()=='x':  # 如果預約不值班 == 'x'，則從 available 中移除
                available_code[day].remove(code)

    # process 如果該員沒有假日班/平日班，則從 avaliable code中間移除
    for code in CODE_LIST:
        if num_holiday[code] == 0:
            for hday in LIST_OF_HOLIDAY:
                if code in available_code[hday]:
                    available_code[hday].remove(code)
        if num_weekday[code] == 0:
            for wday in LIST_OF_WEEKDAY:
                if code in available_code[wday]:
                    available_code[wday].remove(code)
                
                
    # process 預約值班
    reservation_dict = {day:[] for day in DAY_LIST}  
    # 一天1人值班：
    if duty_type !=1:
        for day in DAY_LIST:
            for code in CODE_LIST:
                if df_work[df_work['Code']==code][day].item()==1: # 如果預約值班，則移除其他
                    available_code[day]=[code]
                    reservation_dict[day].append(code)
    else:
    # type1 duty, 一天2人值班，建立 reservation_dict 讓之後程式抓取：
        # reference for reservation numbers in the date
        #'3':2 -> 2 people want duty at 3rd, already cleanse condition>2
        for day in DAY_LIST:
            # reservation_dict[day] = 0  # assign value, 
            for code in CODE_LIST:
                if df_work[df_work['Code']==code][day].item()==1: # 如果預約值班，則增加到 reservation dict
                    reservation_dict[day].append(code)
    
    # 產生 count_start個 符合所有排班規則的 candidate
    preliminary_list = []

    count = count_start
    
    # for progress bar
    total_step = 12  # set 12 intervals
    interval = int(count_start/total_step) 
    progress = [i*interval for i in range(1,total_step+1)]
    
    
    while count >0:  # generate till count = count_start candidates
        stopper = False  # 加速脫離迴圈
        #progress bar
        if progress !=[]:
            if (count_start-count-1)>progress[0]:
                del progress[0]
                prefix = '='*(total_step-len(progress)-1) + '>'
                prefix = "{:-<12}".format(prefix)
                print("{s} {r:0.1%}".format(s=prefix,r=(1-count/count_start)))

        candidate_list = []
        available_code_gen = copy.deepcopy(available_code)  # not alter original list
        num_holiday_gen = copy.deepcopy(num_holiday)
        num_weekday_gen = copy.deepcopy(num_weekday)
        
        for day in DAY_LIST:
        #for day in DAY_LIST_SORTED:
            if stopper == True: # 加速脫離迴圈
                break
            TODAY_IS_HOLIDAY = HOLIDAY_CHECK[day]                
            day_next = str(int(day)+1)  # next day in string
            day_previous = str(int(day)-1)
            
            # 如果今天已經沒有可以用的天數
            for code in CODE_LIST:
            #for code in available_code_gen[day]:
                if TODAY_IS_HOLIDAY == True:
                    #if num_holiday_gen[code] <= 0:
                    if num_holiday_gen[code] == 0:
                        if code in available_code_gen[day]:
                            available_code_gen[day].remove(code)
                    if num_holiday_gen[code] < 0:
                        stopper =True
                        break
                else:
                    #if num_weekday_gen[code] <= 0:
                    if num_weekday_gen[code] == 0:
                        if code in available_code_gen[day]:
                            available_code_gen[day].remove(code)
                    if num_weekday_gen[code] <0:
                        stopper = True
                        break
            if stopper == True: # 加速脫離迴圈
                break            
            
                    
            # type 1 duty
            if duty_type == 1:
                add_item = []
                # type 1 要 check reservation dict
                if len(available_code_gen[day]) <2: # not enough item can be choosed
                    stopper ==True
                    #print('stopped', day)
                    break
                else:
                    if len(reservation_dict[day]) ==0:
                        # 如果沒有人預約值班，那亂數選兩個人
                        add_item = random.sample(available_code_gen[day],2)  # sample 2 in type 1 duty
                    elif len(reservation_dict[day]) == 1: 
                        # 如果只有一人預約值班，那先選他，從available code list 中移除掉，之後再亂數
                        add_item = reservation_dict[day] # 先指定 eg. ['31']
                        try:
                            available_code_gen[day].remove(add_item[0]) # remove the first item
                        except:
                            stopper=True
                            break
                        add_item.append(random.choice(available_code_gen[day])) # 一開始有 check len>=2
                    elif len(reservation_dict[day]) == 2:  
                        # 如果兩人預約這天值班，那就都給他們
                        add_item = reservation_dict[day] # add item 即是這兩個
                    candidate_list.append(add_item)  # add ['X','Y'] to candidiate list  
                    
                    #if (DAY_TABLE[day]+1)> DAYS:
                    #    # 到最後一天的話，就不用移除了
                    #    break
                    #else:
                        # 如果不是最後一天，則依序移除
                    if (DAY_TABLE[day])<DAYS:
                        for itm in add_item:
                            if itm in available_code_gen[day_next]:
                                available_code_gen[day_next].remove(itm)
                    remove_when_not_available(add_item) 
                    
                #if stopper == True:
                #    break
            else:
                # other types ofduty
                if available_code_gen[day] == []: # no item can be choosed
                    #print(day)
                    stopper = True
                    break
                else:
                    add_item = random.choice(available_code_gen[day])   # choice is faster than sample 1[0]
                    candidate_list.append(add_item)
                    remove_when_not_available(add_item)
                    
                    if int(day_next)<=DAYS and add_item in available_code_gen[day_next]:
                        available_code_gen[day_next].remove(add_item)
            if stopper == True:
                break
        # check if QD exist
        if duty_type == 1:
            flag_qd = True
            #flaq_count = True
            for idx in range(len(candidate_list)-1):
                for itm in candidate_list[idx]:
                    if itm in candidate_list[idx+1]:
                        flag_qd = False
                    
            if flag_qd ==True:
                if len(candidate_list)==DAYS:  # 其實不需要這句，因為都篩選到了最後一天，但速度幾乎無差別
                    # check if holiday count or weekday count is overflowed
                    flag_count = True
                    holiday_r = [candidate_list[index][0] for index in holiday_index] + [candidate_list[index][1] for index in holiday_index]
                    weekday_r = [candidate_list[index][0] for index in weekday_index] + [candidate_list[index][1] for index in weekday_index]
                    #print(holiday_r)
                    #print(weekday_r)
                    for codes in CODE_LIST:
                        if holiday_r.count(codes)>num_holiday[codes]:
                            flag_count = False
                            #print('holiday', code, holiday_r.count(codes))
                        if weekday_r.count(codes)>num_weekday[codes]:
                            flag_count = False
                            #print('weekday', code, weekday_r.count(codes))
                    if flag_count == True:
                        preliminary_list.append(candidate_list)
                        count-=1 
        else:
            if len(candidate_list)==DAYS:  # 其實不需要這句，因為都篩選到了最後一天，但速度幾乎無差別
                preliminary_list.append(candidate_list)
                #print(candidate_list)
                count-=1 

    print(f'[type{duty_type},{TYPES_OF_DUTY[duty_type]}班] 初步清單已建立完成')
    #print(num_holiday_gen)
    #print(num_weekday_gen)
    return preliminary_list


def optimization_for_31_2(filtered_full_combination_of_31, df_updated):
    # optimization for 31
    # v2 -> add optimization for mr/ct combination
    """
    input: filtered_full_combination_of_31 (格式像 type1),  df_updated
    output: list_location_std_sorted of combination of 3/1 after optimization
    """
    print(f'正在尋找 [ER/CT/MR] 班最佳排班組合...')
    DAYS = len(filtered_full_combination_of_31[0])  # 這個月有幾天
    df_work = df_updated[(df['Type']==3)|(df['Type']==1)] # type 3 or 4
    CODE_LIST = df_work['Code'].tolist() # code list, ['31','32']
    num_of_qod_dict = {code:0 for code in CODE_LIST}  # 紀錄每個人的 QOD情況
    qod = []  # 每個組合每天的 qod 情況

    for n in range(len(filtered_full_combination_of_31)):  # iterate through list size
        day_count = 0
        for i in range(DAYS-2):
            #possible_qod = [] # to store possible qod in
            for item in filtered_full_combination_of_31[n][i]:  # iterate through duty code in a day
                if item in filtered_full_combination_of_31[n][i+2]: # if qod happens
                    day_count+=1
                    #possible_qod.append(item)  # add to possible_qod       
        qod.append(day_count)
    # 尋找最少 qod 的組合的 index
    min_qod = min(qod)
    min_qod_index = [index for index,value in enumerate(qod) if value==min_qod]

    # 2. 每個人分布的標準差 之間的標準差 最小化，取三個
    min_qod_list = []   # 有最少 qod 組合的list
    for index in min_qod_index:
        min_qod_list.append([index, filtered_full_combination_of_31[index]])  # store index, list with the minimal qods

    # 由 CODE_LIST 內容依序提出資訊
    #error = 0
    list_location_std = []
    for i in range(len(min_qod_list)):  # how many items
        list_location = []
        std_value = []
        for code in CODE_LIST:
            list_location = [location for location,item in enumerate(min_qod_list[i][1]) if code in item]
            std_value.append(np.std(list_location,ddof=0))
        list_location_std.append([min_qod_list[i][1],
                                 min_qod_index[i],
                                 np.std(std_value, ddof=0)]) # form a list, of [list, location, std value]

    # 依照 standard deviation 大小排序
    list_location_std_sorted = sorted(list_location_std, key=lambda x:x[2]) 

    # 最多取三個
    if len(list_location_std_sorted)>3:
        list_location_std_sorted=list_location_std_sorted[0:3]

        
    # 處理 list_location_std_sorted 中的 CT/MR
    # 讓平日班，假日班的 CT/MR平均一些，by 在生成之後的排班下做交換，找出最佳解。所以無法保證大家絕對平均
    # construct holiday/weekday check and holiday/weekday index
    # CT = list_location_std_sorted[0][0][0-3][1]
    # MR = list_location_std_sorted[0][0][0-3][2]
    print(f'正在分配CT/MR排班...')
    IS_HOLIDAY = df_updated.iloc[2,5:].tolist()  # list of holiday 'v' [nan, 'v'...]
    HOLIDAY_CHECK = {}
    for index,item in enumerate(IS_HOLIDAY):
        if str(item).lower() == 'v':
            HOLIDAY_CHECK[str(index+1)] = True
        else:
            HOLIDAY_CHECK[str(index+1)] = False
    LIST_OF_HOLIDAY = [key for key,item in HOLIDAY_CHECK.items() if item==True]
    LIST_OF_WEEKDAY = [key for key,item in HOLIDAY_CHECK.items() if item==False]
    holiday_index = [int(index)-1 for index in LIST_OF_HOLIDAY]
    weekday_index = [int(index)-1 for index in LIST_OF_WEEKDAY]
    
    # count_ct_std for 31 combination, notice the location of CT/MR is at [1] and [2]
    def count_ct_std(input_list, holiday_or_weekday_index):
        temp_list_pd = pd.DataFrame(input_list)
        count_ct_days_list= []
        for code in CODE_LIST:
            # count ct(at templist pd [1] location, each)
            count_ct_days_list.append(temp_list_pd.iloc[holiday_or_weekday_index][temp_list_pd[1]==code][1].count())
        #count std
        std_value = np.array(count_ct_days_list).std()
        #print(count_ct_days_list, std_value)
        return std_value

    # iterate through all the given type 1 list, top 3
    for i in range(len(list_location_std_sorted)):
        # process weekday index and holiday index respectively
        for wh_index in [weekday_index,holiday_index]:
            keep_continue = True
            processing_list = list_location_std_sorted[i][0]
            while keep_continue:
                for loc, indx in enumerate(wh_index):
                    # count std
                    previous_std = count_ct_std(processing_list, wh_index)
                    # exchange CT/MR duty, at process_list[holiday/weekday index] [1](CT) and[2](MR)
                    processing_list[indx][1], processing_list[indx][2] = processing_list[indx][2], processing_list[indx][1]
                    new_std = count_ct_std(processing_list, wh_index)
                    # if new is not better, then change back
                    if new_std>=previous_std:
                        processing_list[indx][1], processing_list[indx][2] = processing_list[indx][2], processing_list[indx][1]
                    else:
                    # if new is better, the break the for loop, start counting from beginning
                        break
                    # if it's at the end, then stop
                    if loc == (len(wh_index)-1):  
                        keep_continue = False
            list_location_std_sorted[i][0] = processing_list
        
    print(f'已完成 [ER/CT/MR班] 最佳排班組合')
    return list_location_std_sorted
    

def optimization_for_34(filtered_full_combination_of_34, df_updated):
    #optimization_for_34
    """
    input: filtered_full_combination_of_34 (格式像 type1),  df_updated
    output: list_location_std_sorted of combination of 3/4 after optimization
    """
    
    print(f'正在尋找 [CR/ER班] 班最佳排班組合...')
    DAYS = len(filtered_full_combination_of_34[0])  # 這個月有幾天
    df_work = df_updated[(df['Type']==3)|(df['Type']==4)] # type 3 or 4
    CODE_LIST = df_work['Code'].tolist() # code list, ['31','32']
    num_of_qod_dict = {code:0 for code in CODE_LIST}  # 每個人的 QOD情況
    qod = []  # 各組每天的 qod 情況

    for n in range(len(filtered_full_combination_of_34)):  # iterate through list size
        day_count = 0
        for i in range(DAYS-2):
            #possible_qod = [] # to store possible qod in
            for item in filtered_full_combination_of_34[n][i]:  # iterate through duty code in a day
                if item in filtered_full_combination_of_34[n][i+2]: # if qod happens
                    day_count+=1
                    #possible_qod.append(item)  # add to possible_qod       
        qod.append(day_count)
    # 尋找最少 qod 的組合的 index
    min_qod = min(qod)
    min_qod_index = [index for index,value in enumerate(qod) if value==min_qod]

    # 2. 每個人分布的標準差 之間的標準差 最小化，取三個
    min_qod_list = []   # 有最少 qod 組合的list
    for index in min_qod_index:
        min_qod_list.append([index, filtered_full_combination_of_34[index]])  # store index, list with the minimal qods


    # 由 CODE_LIST 內容依序提出資訊
    #error = 0
    list_location_std = []
    for i in range(len(min_qod_list)):  # how many items
        list_location = []
        std_value = []
        for code in CODE_LIST:
            list_location = [location for location,item in enumerate(min_qod_list[i][1]) if code in item]
            std_value.append(np.std(list_location,ddof=0))
        list_location_std.append([min_qod_list[i][1],
                                 min_qod_index[i],
                                 np.std(std_value, ddof=0)]) # form a list, of [list, location, std value]

    # 依照 standard deviation 大小排序
    list_location_std_sorted = sorted(list_location_std, key=lambda x:x[2]) 

    # 最多取三個
    if len(list_location_std_sorted)>3:
        list_location_std_sorted=list_location_std_sorted[0:3]

    print(f'已完成 [CR/ER班] 最佳排班組合')

    return list_location_std_sorted


def optimization3(preliminary_list, df_updated, duty_type):
    # optimization 3 -> 新增MR/CT班平均的功能
    #np.seterr(divide='ignore', over='ignore', under='ignore', invalid='ignore')  # 忽略計算問題
    #np.seterr(all='raise')
    """
    input: preliminary_list, updated df, what type of duty
    output: list_location_std_sorted, after optimization
    """
    # Optimizing the list
    # 1. minimize the total days of QOD in everyone (如果只選標準差多少人不夠)
    # find min() of days  -> 這幾乎是最好的了，因為幾乎<3，所以 2 不需要

    # 2. minimize standard deviation of days of QOD among others
    #np.array([2,2,2,1]).std(ddof=0)
    # 計算個人值班分散程度（標準差） 的標準差，依照順序排列 （大家分散程度要差不多）
    # 在這個情況下，不可能大家同時標準差都很高，導致標準差的標準差值很小
    
    # 3. count CT/MR numbers of each person and get std values, try to minimize std values by exchange
    # 

    DAYS = len(preliminary_list[0])  # 這個月有幾天
    df_work = df_updated[df['Type']==duty_type]
    CODE_LIST = df_work['Code'].tolist() # code list, ['31','32']
    
    
    print(f'正在尋找 [type{duty_type},{TYPES_OF_DUTY[duty_type]}班] 最佳排班...')
    
    if duty_type==1:
        num_of_qod_dict = {code:0 for code in CODE_LIST}
        qod = []  # 各組每天的 qod 情況
        #days_of_duty = {code:[] for code in CODE_LIST}
        #for code in CODE_LIST
        for n in range(len(preliminary_list)):
            day_count = 0
            for i in range(DAYS-2):
                #possible_qod = [] # to store possible qod in
                
                for item in preliminary_list[n][i]:  # iterate through duty code in a day
                    if item in preliminary_list[n][i+2]: # if qod happens
                        day_count+=1
                        #possible_qod.append(item)  # add to possible_qod       
            qod.append(day_count)
        # 尋找最少 qod 的組合
        min_qod = min(qod)
        min_qod_index = [index for index,value in enumerate(qod) if value==min_qod]
    
    else:
        qod = []  # 各組 qod 的情況
        for n in range(len(preliminary_list)):
            # search for qod (value of location i == value of location i+2)
            list_temp = [preliminary_list[n][i] for i in range(DAYS-2) if preliminary_list[n][i]==preliminary_list[n][i+2]] 
            qod.append(list_temp)
        qod_pd = pd.DataFrame(qod)

        # 1. 找到 QOD 人次最少的組合
        # num of qods in each candidate
        num_of_qod = []
        for i in range(len(preliminary_list)):
            num_of_qod.append(qod_pd.iloc[i].notnull().sum())  # 非0個數 = qod 個數
        min_qod = min(num_of_qod)
        # create index of candidates with minimal qod days in total
        #eg [7376, 11732, 15383, 18130, 20990, 28528, 28785]
        min_qod_index = [index for index,value in enumerate(num_of_qod) if value==min_qod]
        
        
    # 2. 每個人分布的標準差 之間的標準差 最小化，取三個
    min_qod_list = []  
    for index in min_qod_index:
        min_qod_list.append([index, preliminary_list[index]])  # store index, list with the minimal qods
    
    # 由 CODE_LIST 內容依序提出資訊
    #error = 0
    list_location_std = []
    for i in range(len(min_qod_list)):  # how many items
        list_location = []
        std_value = []
        for code in CODE_LIST:
            list_location = [location for location,item in enumerate(min_qod_list[i][1]) if code in item]
            # min_qod_list = index, list with minimal qod value
            # 如果空白班，會有無法計算的問題，所以加上忽略
            # 填入每個人的 std value, to a list
            std_value.append(np.std(list_location,ddof=0))

        list_location_std.append([min_qod_list[i][1],
                                 min_qod_index[i],
                                 np.std(std_value, ddof=0)]) # form a list, of [list, location, std value]

    # 根據 std value (list_location_std[2]) 來排序
    # sorted_a = sorted(a, key=lambda x: x[1])
    list_location_std_sorted = sorted(list_location_std, key=lambda x:x[2]) 
    # list_location_std[2] is the std value

    
    # 最多取三個
    if len(list_location_std_sorted)>3:
        list_location_std_sorted=list_location_std_sorted[0:3]
        
    
    # 如果為 CT/MR 班，type1
    # 讓平日班，假日班的 CT/MR平均一些，by 在生成之後的排班下做交換，找出最佳解。所以無法保證大家絕對平均
    # construct holiday/weekday check and holiday/weekday index
    if duty_type == 1:
        print(f'正在分配CT/MR排班...')
        
        IS_HOLIDAY = df_updated.iloc[2,5:].tolist()  # list of holiday 'v' [nan, 'v'...]
        HOLIDAY_CHECK = {}
        for index,item in enumerate(IS_HOLIDAY):
            if str(item).lower() == 'v':
                HOLIDAY_CHECK[str(index+1)] = True
            else:
                HOLIDAY_CHECK[str(index+1)] = False
        LIST_OF_HOLIDAY = [key for key,item in HOLIDAY_CHECK.items() if item==True]
        LIST_OF_WEEKDAY = [key for key,item in HOLIDAY_CHECK.items() if item==False]
        holiday_index = [int(index)-1 for index in LIST_OF_HOLIDAY]
        weekday_index = [int(index)-1 for index in LIST_OF_WEEKDAY]        
        
        def count_ct_std(input_list, holiday_or_weekday_index):
            temp_list_pd = pd.DataFrame(input_list)
            count_ct_days_list= []
            for code in CODE_LIST:
                # count ct(at templist pd [0] location, each)
                count_ct_days_list.append(temp_list_pd.iloc[holiday_or_weekday_index][temp_list_pd[0]==code][0].count())
            #count std
            std_value = np.array(count_ct_days_list).std()
            #print(count_ct_days_list, std_value)
            return std_value

        # iterate through all the given type 1 list, top 3
        for i in range(len(list_location_std_sorted)):
            # process weekday index and holiday index respectively
            for wh_index in [weekday_index,holiday_index]:
                keep_continue = True
                processing_list = list_location_std_sorted[i][0]
                while keep_continue:
                    for loc, indx in enumerate(wh_index):
                        # count std
                        previous_std = count_ct_std(processing_list, wh_index)
                        # exchange CT/MR duty
                        processing_list[indx][0], processing_list[indx][1] = processing_list[indx][1], processing_list[indx][0]
                        new_std = count_ct_std(processing_list, wh_index)
                        # if new is not better, then change back
                        if new_std>=previous_std:
                            processing_list[indx][0], processing_list[indx][1] = processing_list[indx][1], processing_list[indx][0]
                        else:
                        # if new is better, the break the for loop, start counting from beginning
                            break
                        # if it's at the end, then stop
                        if loc == (len(wh_index)-1):  
                            keep_continue = False
                list_location_std_sorted[i][0] = processing_list
        
        
    print(f'已完成 [type{duty_type},{TYPES_OF_DUTY[duty_type]}班] 最佳排班排序')
    return list_location_std_sorted


def main():
        
    global df
    global TYPES_OF_DUTY
    global FILE_NAME
    global NUM_TO_RUN
    global DUTY_LIST  # from GUI
    df = pd.read_excel(FILE_NAME)

    # define types of duties
    TYPES_OF_DUTY = {0:'Test', 1:'CT/MR', 3:'ER', 4:'CR', 5:'VS', 
                     6:'Other6', 7:'Other7', 8:'Other8', 9:'Other9'}  # no type 2

    # cleanse the data, determine if there is violation
    type_to_generate = sorted(DUTY_LIST, reverse=True)
    
    #df, type_to_generate = data_cleansing(df)
    df = data_cleansing(df)
    violation, df_updated = is_violation(df,type_to_generate)

    if len(type_to_generate)>2:
        print('同時超過三組排班，請依序執行')
        violation = True

    # if no violation, then start generating list into optimized list
    optimized_list = []
    optimized_34 = []
    optimized_31 = []

    preliminary_list = {}
    if violation == False:
        # create preliminary list for each duty type
        for duty_type in type_to_generate:
            preliminary_list[duty_type] = preliminary_gen3(df_updated, duty_type, NUM_TO_RUN)
            #optimized_list[duty_type] = optimization2(preliminary_list, df_updated, duty_type)
        # corss check if violation (duty on the same day, +/-1 qd)

        if 3 in type_to_generate and 4 in type_to_generate:
            # for 3 4 combination
            filtered_combination_34 = cross_validation_34(preliminary_list)
            # generate optimized list
            optimized_34 = optimization_for_34(filtered_combination_34, df_updated)
            first_choice, other_choice = formatting_for_output_31_34(optimized_34, 34)
        elif 1 in type_to_generate and 3 in type_to_generate:
            # for 3 1 combination
            filtered_combination_31 = cross_validation_31(preliminary_list)
            optimized_31 = optimization_for_31_2(filtered_combination_31, df_updated)    
            first_choice, other_choice = formatting_for_output_31_34(optimized_31, 31)
        else:
            for duty_type in type_to_generate:
                #optimized_list.append([duty_type, optimization2(preliminary_list[duty_type], df_updated, duty_type)])
                optimized_list.append([duty_type, optimization3(preliminary_list[duty_type], df_updated, duty_type)])
            # prepare list for output
                first_choice, other_choice = formatting_for_output(optimized_list)
        # export_to_excel
        export_to_excel(first_choice, other_choice)


# GUI 介面，不用
#if __name__ == "__main__":
#    main()
        
#
#
#   GUI 介面
#
#        

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

window = tk.Tk() #一個叫做window的新視窗
window.title('Duty arranger')
window.geometry('600x140')


# Duty box
global DUTY_LIST
DUTY_LIST=[]
def duty_box():
    # duty check
    global DUTY_LIST
    duty_check = [int(varC[i].get()) for i in range(5)]
    # make duty list
    DUTY_LIST = [[0,1,2,3,4][i] for i,val in enumerate(duty_check) if val ==1]
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
file_var = tk.StringVar()
file_entry = tk.Entry(window, textvariable= file_var, state = 'disable', 
                      width =22, font=('Arial', 12))
file_entry.grid(column=1, row=2, rowspan=2, padx=3, pady=3)

# import os
def get_filename():
    full_path = filedialog.askopenfilename(initialdir = os.getcwd(),title = "請選擇檔案",
                                          filetypes = (("xlsm files","*.xlsm"),("all files","*.*")))
    file_var.set(full_path)
    print(full_path)
    
open_file_bt = tk.Button(window, text='開啟檔案', command=get_filename, font=('Arial', 12))
open_file_bt.grid(column=2, row=2, rowspan=2)


# 定義 檔案完整路徑，檔案資料夾位置，
FILE_NAME = ''
FILE_DIR = ''
NUM_TO_RUN = 0


# 檢查是否都完成開始前的條件：選擇要執行的 duty type，選擇檔案位置
check_start = True
def start_arrange():
    global check_start
    global DUTY_LIST
    global FILE_NAME
    global NUM_TO_RUN
    global FILE_DIR
    check_start = True
    check_l = True
    check_f =True
    if DUTY_LIST== []:
        check_start = False
        check_l = False
    if file_var.get() =='':
        check_start = False
        check_f = False
    if check_f == False and check_l == False:
        messagebox.showwarning('','請選擇 [欲執行的值班類別] 與 [排班檔案]')
        #print('請選擇欲執行的值班類別與排班檔案')
    elif check_f == False:
        messagebox.showwarning('','請選擇 [排班檔案]')
        #print('請選擇排班檔案')
    elif check_l == False:
        messagebox.showwarning('','請選擇 [欲執行的值班類別]')
        #print('請選擇欲執行的值班類別')
    if check_start == True:
        # main, file path, duty_list, numbers to run
        FILE_NAME = file_var.get()
        NUM_TO_RUN = s.get()
        parsing = [index for index, item in enumerate(FILE_NAME) if item =="/"]
        FILE_DIR = FILE_NAME[0:(parsing[-1]+1)]
        main()  # start running main function



start_arrange = tk.Button(window, text='開始排班', command=start_arrange, font=('Arial', 14))
start_arrange.grid(column=3, row=0, columnspan=2, rowspan=4, sticky=tk.N+tk.S, padx=10, pady=20)
window.mainloop() #進入等待處理物件的狀態



