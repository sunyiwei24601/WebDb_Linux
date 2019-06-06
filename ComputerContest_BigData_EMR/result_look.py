# -*- coding:utf-8 -*-
import re
import pandas as pd
from pandas import DataFrame



import re
import pandas as pd
import jieba
from pandas import DataFrame

path1=r'../EMR_result/value_df.csv'
value_df=pd.read_csv(path1,encoding='gb2312')

path2=r'../EMR_result/labeled_df0527.csv'
labeled_df=pd.read_csv(path2,encoding='gb2312')

def get_new_labeld_df():
    labeled_df526 = pd.read_csv(r'../EMR_result/labeled_df0526.csv', encoding='gb2312')
    df=pd.concat([labeled_df526[['样本']],labeled_df],axis=1)
    df.to_csv(r'../EMR_result/labeled_df0527.csv',index=False, encoding='gb2312')
    pass

# 病理
def get_pathology_contrast():

    df=pd.concat([labeled_df[['样本','病理']],value_df[['病理']]],axis=1)
    df.columns=['样本','标注病理','提取病理']

    def my_replace(column):
        if pd.isnull(column):
            return
        return column.replace('、','，')
    df['标注病理']=df['标注病理'].apply(my_replace)
    def contrast(row):
        if row['标注病理']==row['提取病理']:
            return True
        return False
    df['比较']=df.apply(contrast,axis=1)
    df.to_csv(r'../EMR_result/pathology_contrast.csv',encoding='gb2312',index=False)
    pass

def get_upCut_contrast():
    df = pd.concat([labeled_df[['样本', '上切端是否累及']], value_df[['上切端是否累及']]], axis=1)
    df.columns = ['样本', '标注上切端是否累及', '提取上切端是否累及']


    def contrast(row):
        if pd.isnull(row['标注上切端是否累及']) and pd.isnull(row['提取上切端是否累及']):
            return True
        if row['标注上切端是否累及'] == row['提取上切端是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/upCut_contrast.csv', encoding='gb2312', index=False)
    pass
def get_downCut_contrast():
    df = pd.concat([labeled_df[['样本', '下切端是否累及']], value_df[['下切端是否累及']]], axis=1)
    df.columns = ['样本', '标注下切端是否累及', '提取下切端是否累及']


    def contrast(row):
        if pd.isnull(row['标注下切端是否累及']) and pd.isnull(row['提取下切端是否累及']):
            return True
        if row['标注下切端是否累及'] == row['提取下切端是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/downCut_contrast.csv', encoding='gb2312', index=False)
    pass
def get_baseCut_contrast():
    df = pd.concat([labeled_df[['样本', '基底切端是否累及']], value_df[['基底切端是否累及']]], axis=1)
    df.columns = ['样本', '标注基底切端是否累及', '提取基底切端是否累及']


    def contrast(row):
        if pd.isnull(row['标注基底切端是否累及']) and pd.isnull(row['提取基底切端是否累及']):
            return True
        if row['标注基底切端是否累及'] == row['提取基底切端是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/baseCut_contrast.csv', encoding='gb2312', index=False)
    pass

# 转移比例
def get_TransferRatio_contrast():
    df = pd.concat([labeled_df[['样本', '转移比例']], value_df[['转移比例']]], axis=1)
    df.columns = ['样本', '标注转移比例', '提取转移比例']


    def contrast(row):
        if pd.isnull(row['标注转移比例']) and pd.isnull(row['提取转移比例']):
            return True
        if row['标注转移比例'] == row['提取转移比例']:
            return True
        try:
            label=row['标注转移比例'].split()
            extract=row['提取转移比例'].split()

            label=label.sort()
            extract=extract.sort()

            if label==extract:
                return True
        except:
            pass
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/TransferRatio_contrast.csv', encoding='gb2312', index=False)
    pass

# 回肠
def get_ileumCut_contrast():
    df = pd.concat([labeled_df[['样本', '回肠切端是否累及']], value_df[['回肠切端是否累及']]], axis=1)
    df.columns = ['样本', '标注回肠切端是否累及', '提取回肠切端是否累及']


    def contrast(row):
        if pd.isnull(row['标注回肠切端是否累及']) and pd.isnull(row['提取回肠切端是否累及']):
            return True
        if row['标注回肠切端是否累及'] == row['提取回肠切端是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/ileumCut_contrast.csv', encoding='gb2312', index=False)
    pass
# 结肠
def get_colonCut_contrast():
    df = pd.concat([labeled_df[['样本', '结肠切端是否累及']], value_df[['结肠切端是否累及']]], axis=1)
    df.columns = ['样本', '标注结肠切端是否累及', '提取结肠切端是否累及']


    def contrast(row):
        if pd.isnull(row['标注结肠切端是否累及']) and pd.isnull(row['提取结肠切端是否累及']):
            return True
        if row['标注结肠切端是否累及'] == row['提取结肠切端是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/colonCut_contrast.csv', encoding='gb2312', index=False)
    pass
# 网膜
def get_omentum_contrast():
    df = pd.concat([labeled_df[['样本', '网膜是否累及']], value_df[['网膜是否累及']]], axis=1)
    df.columns = ['样本', '标注网膜是否累及', '提取网膜是否累及']


    def contrast(row):
        if pd.isnull(row['标注网膜是否累及']) and pd.isnull(row['提取网膜是否累及']):
            return True
        if row['标注网膜是否累及'] == row['提取网膜是否累及']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/omentum_contrast.csv', encoding='gb2312', index=False)
    pass


# 淋巴结个数
def get_numberLymph_contrast():
    df = pd.concat([labeled_df[['样本', '肠旁淋巴结个数']], value_df[['肠旁淋巴结个数']]], axis=1)
    df.columns = ['样本', '标注肠旁淋巴结个数', '提取肠旁淋巴结个数']


    def contrast(row):
        if pd.isnull(row['标注肠旁淋巴结个数']) and pd.isnull(row['提取肠旁淋巴结个数']):
            return True
        if ("%.0f" % row['标注肠旁淋巴结个数']) == row['提取肠旁淋巴结个数']:
            return True
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/numberLymph_contrast.csv', encoding='gb2312', index=False)
    pass

# 浸润
def get_infiltration_contrast():
    df = pd.concat([labeled_df[['样本', '浸润']], value_df[['浸润']]], axis=1)
    df.columns = ['样本', '标注浸润', '提取浸润']

    def contrast(row):
        if pd.isnull(row['标注浸润']) and pd.isnull(row['提取浸润']):
            return True
        if row['标注浸润'] == row['提取浸润']:
            return True
        try:
            label=row['标注浸润'].split()
            extract=row['提取浸润'].split()

            label=label.sort()
            extract=extract.sort()

            if label==extract:
                return True
        except:
            pass
        return False

    df['比较'] = df.apply(contrast, axis=1)
    df.to_csv(r'../EMR_result/infiltration_contrast.csv', encoding='gb2312', index=False)
    pass

get_omentum_contrast()