# -*- coding:utf-8 -*-
import re
import pandas as pd
from pandas import DataFrame



import re
import pandas as pd
import jieba
from pandas import DataFrame
path=r'../EMR_result/EMR_df_norm.csv'
# EMR_df=pd.read_csv(path,encoding='gb2312')
# EMR_df.columns=['索引','文本内容']


x="['肿瘤局限于胰腺内']"

# 获取浸润的值
def get_infiltration(x):
    x=x.replace("'",'')
    if x=='[]':
        return
    else:
        x=x[1:-1]
        x=x.split(',')

    infiltrations=[]
    for i in range(len(x)):
        str=x[i]
        str = str.replace('另送', '')
        str = str.replace('另', '')
        str=str.replace(' ', '')
        if '伴' in str:
            index=str.index('伴')
            str=str[:index]
        pattern=re.compile('均?可?见.*浸润')
        if re.search(pattern,str):
            # 取前面的
            index=re.search(pattern,str).span()[0]
            infilt=str[:index]
            infiltrations.append(infilt)
        else:
            pattern = re.compile('浸润至')
            if re.search(pattern,str):
                # 取后面的
                index=re.search('浸润至',str).span()[1]
                infilt=str[index:]
                infiltrations.append(infilt)
            else:
                str=str.strip()
                if str[:4]=='肿瘤侵犯':
                    continue
                str_splits=jieba.lcut(str)
                str_splits=list(filter(None, str_splits))
                if str_splits:
                    if str_splits[0]=='浸润':
                        infiltrations.append("".join(str_splits[1:]))
                    else:
                        # or (str[:4]=='肿瘤侵犯')
                        if (str[:4]=='局部浸润')  or (str[:4]=='肿瘤浸润') or (str[:4]=='局灶浸润') :
                            infilt=str[4:]
                            infiltrations.append(infilt)
                        else:
                            pattern=re.compile('局限于.*内')
                            result=re.search(pattern,str)
                            if result:
                                index1=result.span()[0]
                                index2=result.span()[1]
                                infilt=str[index1+3:index2-1]
                                infiltrations.append(infilt)
                            else:
                                if str[:5]=='癌组织浸润':
                                    infilt = str[5:]
                                    infiltrations.append(infilt)
                                else:
                                    pattern=re.compile('受.*浸润')
                                    result = re.search(pattern, str)
                                    if result:
                                        index = re.search(pattern, str).span()[0]
                                        infilt = str[:index]
                                        infiltrations.append(infilt)
                                    else:
                                        pattern = re.compile('”(.*)”')
                                        result=re.findall(pattern,str)
                                        if result:
                                            infiltrations+=result
                                        else:
                                            pass
                                            # print(str)
                                            # infiltrations.append(str)

    # return x
    x=infiltrations
    x = list(filter(None, x))
    x=list(set(x))
    if not x:
        return
    # 改变list形式
    str = x[0]
    if len(x) > 1:
        for i in range(len(x)):
            if i == 0:
                continue
            str += '，'
            str += x[i]
    return str

str=get_infiltration(x)