import re
import pandas as pd
path=r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'
EMR_df=pd.read_csv(path,header=None,encoding='gb2312')
EMR_df.columns=['文本内容']

# 查看双引号中间的内容有哪些
def look1():
    for row in EMR_df['文本内容']:
        row=re.sub('“|”','"',row)
        pattern = re.compile('“(.*?)”')
        quote_text=re.findall(pattern,row)
        for q in quote_text:
            print(q)
look1()