import re
import pandas as pd
import jieba
jieba.load_userdict('my_dict.txt')
from pandas import DataFrame
path=r'D:\SUFE\ComputerContest_BigData\EMR_result\split_df.csv'
EMR_df=pd.read_csv(path,encoding='gb2312')


def remove_list(x):
    if pd.isnull(x):
        return
    x = x.replace("'", '')
    if x == '[]':
        return
    else:
        x = x[1:-1]
        x = x.split(',')
    for i in range(len(x)):
        x[i] = x[i].replace('（', '')
        x[i] = x[i].replace('）', '')
    x = list(set(x))
    # 去掉list的形式
    str = x[0]
    if len(x) > 1:
        for i in range(len(x)):
            if i == 0:
                continue
            str += '，'
            str += x[i]
    return str
infiltration=EMR_df['浸润'].apply(remove_list)

for i in infiltration:
    if pd.isnull(i):
        continue
    i=i.replace('”','')
    i = i.replace(' ', '')
    l=i.split('，')
    # print (l)
    for j in l:
        print(jieba.lcut(j))