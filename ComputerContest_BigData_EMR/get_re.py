import re
import pandas as pd
path=r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'
EMR_df=pd.read_csv(path,header=None,encoding='gb2312')
EMR_df.columns=['文本内容']

def get_specimen(x):
    records=[]

    splits = re.split(pattern='，|。|：|；|\s|:', string=x)
    for j in splits:
        pattern=re.compile('.*?标本')
        records+=pattern.findall(j)

        pattern=re.compile('“.*?标本”')
        records += pattern.findall(j)

        pattern=re.compile('“.* ?活检”')
        records += pattern.findall(j)

        if splits.index(j)<3:
            pattern = re.compile('“.*?”')
            records += pattern.findall(j)


    # if records:
    #     pattern = re.compile('[^\u4e00-\u9fa5]')
    #     for i in range(len(records)):
    #         # records[i]=records[i].replace('“','')
    #         # records[i] = records[i].replace('”', '')
    #         # records[i] = records[i].replace('：', '')
    #         if pattern.search(records[i]):
    #             records[i]=pattern.sub('',records[i])
    records=list(set(records))

    cur_list = records
    # 需要先去重
    out_list = list()
    for cur_str1 in cur_list:
        contian_flag = 0
        for cur_str2 in cur_list:
            if (cur_str1 in cur_str2):
                contian_flag = contian_flag + 1
        if (contian_flag == 1):
            out_list.append(cur_str1)
    records=out_list


    return records




specimen_df = EMR_df['文本内容'].apply(get_specimen)
specimen_df.to_csv('../EMR_result/specimen_df0530.csv',encoding='GB2312')
pass

# 存在左右引号使用不规范，把左右引号都换为英文的
# def replace_quotation_mark(x):
#     str=re.sub('“|”','"',x)
#     return str
# EMR_df['文本内容']=EMR_df['文本内容'].apply(replace_quotation_mark)





# def get_specimen(x):
#     # ?表示非贪婪模式
#     # 标本类型:(.*)标本
#     pattern = re.compile('^\u6807\u672c\u7c7b\u578b\u003a(.*)\u6807\u672c')
#     specimen = re.findall(pattern, x)
#     if specimen:
#         return specimen[0]
#     else:
#         pattern = re.compile('“(.*?)”')
#         specimen=re.findall(pattern,x)
#         if specimen:
#             return specimen[0]
#         else:
#             # （(.*?)）
#             pattern = re.compile('\uff08(.*?)\uff09')
#             specimen = re.findall(pattern, x)
#             if specimen:
#                 return specimen[0]
#             else:
#                 pattern = re.compile('“(.*)”')
#                 specimen = re.findall(pattern, x)
#                 if specimen:
#                     return specimen[0]
#                 else:
#                     # ^(.*)标本
#                     pattern = re.compile('^(.*)\u6807\u672c')
#                     specimen = re.findall(pattern, x)
#                     if specimen:
#                         return specimen[0]
#                     else:
#                         pattern = re.compile('^(.*?)：')
#                         specimen = re.findall(pattern, x)
#                         if specimen:
#                             return specimen[0]
#                         else:
#                             return specimen
# specimen_df=EMR_df['文本内容'].apply(get_specimen)
#







# import jieba
# def get_jieba_split(x):
