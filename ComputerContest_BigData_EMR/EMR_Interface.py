import os
import sys
import pandas as pd

from preprocess import get_EMR_df_norm
from get_split import get_split_df
from get_value import get_value_df

# current_path=os.path.dirname(os.path.abspath(__file__))
# sys.path.append(current_path+'\ChineseNER_master')
# sys.path.append(current_path+'\ChineseNER_master2')
# from ChineseNER_master.main_Interface import get_infiltration_model
# from ChineseNER_master2.main_Interface import get_spe_model


if __name__=='__main__':
    initial_EMR_path=r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'

    # 官方所给病历文件的编码
    read_encoding='gb2312'

    # 输出结构化文本文件的编码
    to_encoding='gb2312'

    # 数据清洗与预处理
    get_EMR_df_norm(initial_EMR_path,read_encoding)

    # 截取属性对应分句
    get_split_df()

    # 获取值
    get_value_df(to_encoding)

    # 用模型获取浸润值
    # get_infiltration_model()
    os.system('python ChineseNER_master\main_Interface.py')

    # 用模型获取浸标本值
    # get_spe_model()
    os.system('python ChineseNER_master2\main_Interface.py')

    value_df =pd.read_csv('value_df.csv', encoding='gb2312')

    pass