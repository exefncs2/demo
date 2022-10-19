# -*- coding: utf-8 -*-
### Create 20221019 by Felix ###
### 多向連線 & 減少連線次數   ###
### 資料來源 可看參考檔  ###

from link_DB import commit
from WriteFile import xlsx_builder
import pathlib
import os
import time
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

DATES = time.strftime('%Y%m%d')
MAIN_DIR = pathlib.Path(__file__).parent.absolute()
OUT_PUT_DIR = f"{MAIN_DIR}/OUTPUT_FILE"
OUT_PUT_DATES_DIR = f"{OUT_PUT_DIR}/{DATES}"

def main():
    ### 創建資料夾 ###
    if not os.path.exists(OUT_PUT_DIR):
        os.mkdir(OUT_PUT_DIR)
    
    if not os.path.exists(OUT_PUT_DATES_DIR):
        os.mkdir(OUT_PUT_DATES_DIR)
    
    ### 寫入檔案 ###
    sheet_name = 'sheet1'
    file_writer = xlsx_builder.xlsx_builder(file_name = '檔案名稱')
    xlsx_path = file_writer.build_blank_xlsx(path = OUT_PUT_DATES_DIR,sheet_name = sheet_name)# 回傳 檔案位置
    
    ### 假設依照使用sql分檔xlsx也能用資料庫Table ###
    DB_dict = pd.read_excel('./source/demo_Psql.xlsx')
    DB_list = DB_dict['db'].unique()
    
    ### 同DB只使用一次連線 ###
    DB_link_list = {}
    for DB in DB_list:
        DB_link_list[DB] = commit.COMMIT()
        DB_link_list[DB].link(use_DB = 'PSQL', DB = DB)
        
    ### 取用資料 ###
    for cell_data in dataframe_to_rows(DB_dict, index = False, header =False):
        DB = cell_data[0]
        schema = cell_data[1]
        table = cell_data[2]
        column = cell_data[3]
        
        data = DB_link_list[DB].query_base(schema = schema,
                                                      table = table,
                                                      column = column)
        
        ### 寫入資料 ###
        for row in dataframe_to_rows(data, index = False, header =False):
            # 因我的資料型態特別[['AAAA'],2] 做特殊處理
            if type(row[0]).__name__ == 'list':
                row[0] = row[0][0]
            # 一行一行寫入
            file_writer.insert_row(file_path = xlsx_path,
                                sheet_name = sheet_name,
                                row = row)
        
        
        
    ### 關閉連線 ###
    for DB in DB_list:
        DB_link_list[DB].close()
    
    

if __name__=='__main__':
    main()