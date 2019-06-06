import re
import pandas as pd
path=r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'
EMR_df=pd.read_csv(path,header=None,encoding='gb2312')
EMR_df.columns=['文本内容']



# 存在左右引号使用不规范，把左右引号都换为英文的
def replace_quotation_mark(x):
    str=re.sub('“|”','"',x)
    return str
EMR_df['文本内容']=EMR_df['文本内容'].apply(replace_quotation_mark)












def get_specimen(x):
    # ?表示非贪婪模式
    # 标本类型:(.*)标本
    pattern = re.compile('^\u6807\u672c\u7c7b\u578b\u003a(.*)\u6807\u672c')
    specimen = re.findall(pattern, x)
    if specimen:
        return specimen[0]
    else:
        pattern = re.compile('“(.*?)”')
        specimen=re.findall(pattern,x)
        if specimen:
            return specimen[0]
        else:
            # （(.*?)）
            pattern = re.compile('\uff08(.*?)\uff09')
            specimen = re.findall(pattern, x)
            if specimen:
                return specimen[0]
            else:
                pattern = re.compile('“(.*)”')
                specimen = re.findall(pattern, x)
                if specimen:
                    return specimen[0]
                else:
                    # ^(.*)标本
                    pattern = re.compile('^(.*)\u6807\u672c')
                    specimen = re.findall(pattern, x)
                    if specimen:
                        return specimen[0]
                    else:
                        pattern = re.compile('^(.*?)：')
                        specimen = re.findall(pattern, x)
                        if specimen:
                            return specimen[0]
                        else:
                            return specimen
# specimen_df=EMR_df['文本内容'].apply(get_specimen)
# specimen_df.to_csv('../EMR_result/specimen_df.csv',index=False)







# import jieba
# def get_jieba_split(x):
