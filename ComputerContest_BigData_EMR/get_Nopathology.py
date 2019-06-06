import re
import pandas as pd
import jieba
from pandas import DataFrame
path=r'../EMR_result/EMR_df_norm.csv'
EMR_df=pd.read_csv(path,encoding='gb2312')
EMR_df.columns=['索引','文本内容']

pathologies = ['乳头状腺癌', '管状腺癌', '黏液腺癌', '印戒细胞癌', '未分化癌',
               '腺鳞癌', '鳞状细胞癌', '胰腺导管腺癌', '鳞状细胞癌', '神经内分泌癌','浆液性癌'
               '腺癌', '癌疑']

def check_pathology(x):
    for p in pathologies:
        if p in x:
            return True
    return False

EMR_df['bool_pathology']=EMR_df['文本内容'].apply(check_pathology)

EMR_df[EMR_df['bool_pathology']==False]['文本内容'].to_csv(r'../EMR_result/EMR_Nopathology.csv')