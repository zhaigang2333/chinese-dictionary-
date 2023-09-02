import pymysql
import pandas as pd
import re
from sqlalchemy import create_engine
import find_elements as FE
import utils as UT


    
db_data = UT.getdata_from_db("SELECT * FROM xhzd_surnfu ", 'dict')



for idx, data in db_data.iterrows():
    
    try:
        print('id：----', data[0], data[1])
        results = re.split(r'<br>', data[8])
        
        p_data = UT.replace_element_with_empty(results, results[0])
        
        m_data = FE.find_elements_with_symbol(p_data)
        
        c_data = FE.combin_elements_with_symbol(m_data)
        #print('处理前的结果：', c_data)
        final_data = []
        
        for i in range(len(c_data)):
            temp_arr = c_data[i].split('|')
            pre_temp_arr = c_data[i-1].split('|')
            #print('合并数据---------1：',pre_temp_arr)
            # print('合并数据---------2：',temp_arr)
            # print('合并数据---------3：',UT.is_contain_same_element(temp_arr, pre_temp_arr))
            if UT.is_contain_same_element(pre_temp_arr,temp_arr):
                temp_arr=UT.merge_two_array(pre_temp_arr,temp_arr)
                c_data[i]='|'.join(temp_arr[:])
                #print('重复合并_______：', UT.extract_and_count(temp_arr),temp_arr)
            if UT.extract_and_count(temp_arr) > 1:
                temp = '|'.join(temp_arr[2:])
                del temp_arr[2:]
                temp_arr.append(temp)
            elif UT.extract_and_count(temp_arr) == 1:
                temp = '|'.join(temp_arr[1:])
                del temp_arr[1:]
                temp_arr.append(temp)
                temp_arr.insert(0, '*')
            else:
                temp = '|'.join(temp_arr[:])
                del temp_arr[:]
                temp_arr.append(temp)
                temp_arr.insert(0, '*')
                temp_arr.insert(0, '*')
            
            temp_arr.insert(0, data[0])
            #print('最终数据——————————————', temp_arr)
            final_data.append(UT.convert_to_custom_dict(temp_arr))
        #print('插入的数据---：', final_data)

        UT.insert_data_into_db(final_data,'dict')

    except Exception as e:

        error_message = f"An exception occurred: {e}"
        print(error_message)
        UT.write_to_txt_file("error_log.txt", error_message)

    finally:
        # 这里可以添加一些无论是否发生异常都需要执行的代码
        pass


