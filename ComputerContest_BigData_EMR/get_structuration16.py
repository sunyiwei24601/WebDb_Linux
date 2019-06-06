import re
import pandas as pd
import jieba
from pandas import DataFrame
path=r'../EMR_result/EMR_df_norm.csv'
EMR_df=pd.read_csv(path,encoding='gb2312')
EMR_df.columns=['索引','文本内容']

def check_struct(x):
    if '标本类型:' in x:
        return True
    else:
        return False

EMR_df['bool_struct']=EMR_df['文本内容'].apply(check_struct)

EMR_df[EMR_df['bool_struct']==True]['文本内容'].to_csv(r'../EMR_result/EMR_struct16.csv')