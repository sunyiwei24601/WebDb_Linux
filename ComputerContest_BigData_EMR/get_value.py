import re
import pandas as pd
import jieba
from pandas import DataFrame
# path=r'../EMR_result/split_df.csv'

def get_value_df(to_encoding,split_df_path='split_df.csv',value_df_path='value_df.csv'):
    split_df = pd.read_csv(split_df_path, encoding='gb2312')

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
            x[i] = x[i].replace('（','')
            x[i] = x[i].replace('）', '')
        x=list(set(x))
        # for i in range(len(x)):
        #     if '，' in x[i]:
        #         splits=x[i].split('，')
        #         x[i]=splits[1]

        # 去掉list的形式
        str = x[0]
        if len(x) > 1:
            for i in range(len(x)):
                if i == 0:
                    continue
                str += '，'
                str += x[i]
        return str
    # split_df['其他'] = split_df['其他'].apply(remove_list)

    # 获取标本属性的值
    def get_specimen(x):
        if pd.isnull(x):
            return
        #str转list
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')

        specimen=[]
        for i in range(len(x)):
            x[i]=x[i].strip()
            # 只取'见'前面的字
            if '见' in x[i]:
                result = re.search('见', x[i])
                index = re.search('见', x[i]).regs[0][1]
                x[i] = x[i][:index]
            # 只取标本前面的字
            if '标本' in x[i]:
                result = re.search('标本', x[i])
                index = re.search('标本', x[i]).regs[0][1]
                spm=x[i][:index]
                # specimen.append(x[i][:index])
            else:
                # 括号匹配
                pattern = re.compile('（?(.*?)）')
                result = re.findall(pattern, x[i])
                if result:
                    spm=result[0]
                    # specimen.append(result[0])
                else:
                    spm=x[i]
                    # specimen.append(x[i])
                # try:
                #     if specimen[-4:]=='肿瘤部位':
                #         specimen= specimen[:-4]
                # except:
                #     pass
                # try:
                #     if specimen[-5:] == '组织学类型':
                #         specimen = specimen[:-5]
                # except:
                #     pass
            if spm[-2:] != '标本':
                spm = spm + '标本'
            specimen.append(spm)
        x=specimen
        x=list(set(x))

        # return specimen
        # 去掉list的形式
        str = x[0]
        if len(x) > 1:
            for i in range(len(x)):
                if i == 0:
                    continue
                str += '，'
                str += x[i]
        return str

    # 返回list
    def get_specimen2(x):
        if pd.isnull(x):
            return
        else:
            # 用两个双引号去找标本，防止标本不出现在最前面的情况
            pattern = re.compile('”(.*?)”')
            result=re.findall(pattern,x)
            if result:
                specimen=result
            else:
                # 括号匹配
                pattern = re.compile('（?(.*?)）')
                result = re.findall(pattern, x)
                if result:
                    specimen = result
                else:
                    # 只取标本前面的字
                    result=re.search('标本',x)
                    if result:
                        index = re.search('标本', x).regs[0][1]
                        specimen=[x[:index]]
                    else:
                        specimen=[x]
            for i in range(len(specimen)):
                try:
                    if specimen[i][-4:]=='肿瘤部位':
                        specimen[i] = specimen[i] [:-4]
                except:
                    pass
                try:
                    if specimen[i][-5:] == '组织学类型':
                        specimen[i] = specimen[i][:-5]
                except:
                    pass
                if specimen[i][-2:] != '标本':
                    specimen[i] = specimen[i] + '标本'
        return specimen
    # split_df['标本']=split_df['标本'].apply(get_specimen)


    # 获取病理属性的值
    def get_pathology(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        if not x:
            return
        for i in range(len(x)):
            x[i]=x[i].replace(' ','')

        # #去掉list中子集
        # cur_list = x
        # # 需要先去重
        # out_list = list()
        # for cur_str1 in cur_list:
        #     contian_flag = 0
        #     for cur_str2 in cur_list:
        #         if (cur_str1 in cur_str2):
        #             contian_flag = contian_flag + 1
        #     if (contian_flag == 1):
        #         out_list.append(cur_str1)
        # x=out_list

        if not x:
            return
        str=x[0]
        if len(x)>1:
            for i in range(len(x)):
                if i==0:
                    continue
                str+='，'
                str+=x[i]
        str=str.replace(' ','')
        return str

    split_df['病理']=split_df['病理'].apply(get_pathology)

    # 获取瘤体大小的值
    def get_tumour_size(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        records=[]
        for i in range(len(x)):
            #只取‘直径’或‘大小’后面的字
            # if '直径' in x[i]:
            #     sep = '直径'
            #     index = x[i].find(sep) +2
            #     x[i]=x[i][index:]
            # if '大小' in x[i]:
            #     sep = '大小'
            #     index = x[i].find(sep) +2
            #     x[i]=x[i][index:]
            pattern=re.compile(r'\d[^\u4e00-\u9fa5]*cm')
            tumour_size=pattern.findall(x[i])
            if tumour_size:
                records+=tumour_size
                # x[i]=tumour_size.group()
        # 只保留数字、×、cm、小数点.、-、x
        for i in range(len(records)):
            records[i] = "".join(filter(lambda ch: ch in '0123456789.cm×x-*', records[i]))
            if ('×' not in records[i]) and ('*' not in records[i]) and ('x' not in records[i]):
                records[i]='直径'+records[i]
        x=records
        if not x:
            return
        str = x[0]
        if len(x) > 1:
            for i in range(len(x)):
                if i == 0:
                    continue
                str += '，'
                str += x[i]
        return str

    split_df['肿瘤大小']=split_df['肿瘤大小'].apply(get_tumour_size)

    # 获取浸润的值
    # def get_infiltration(x):
    #     x=x.replace("'",'')
    #     if x=='[]':
    #         return
    #     else:
    #         x=x[1:-1]
    #         x=x.split(',')
    #
    #     infiltrations=[]
    #     for i in range(len(x)):
    #         if '未见' in x[i]:
    #             continue
    #         str=x[i]
    #         str = str.replace('另送', '')
    #         str = str.replace('另', '')
    #         str=str.replace(' ', '')
    #         if '伴' in str:
    #             index=str.index('伴')
    #             str=str[:index]
    #         pattern=re.compile('均?可?见.*浸润')
    #         if re.search(pattern,str):
    #             # 取前面的
    #             index=re.search(pattern,str).span()[0]
    #             infilt=str[:index]
    #             infiltrations.append(infilt)
    #         else:
    #             pattern = re.compile('浸润至')
    #             if re.search(pattern,str):
    #                 # 取后面的
    #                 index=re.search('浸润至',str).span()[1]
    #                 infilt=str[index:]
    #                 infiltrations.append(infilt)
    #             else:
    #                 str=str.strip()
    #                 if str[:4]=='肿瘤侵犯':
    #                     continue
    #                 str_splits=jieba.lcut(str)
    #                 str_splits=list(filter(None, str_splits))
    #                 if str_splits:
    #                     if str_splits[0]=='浸润':
    #                         infiltrations.append("".join(str_splits[1:]))
    #                     else:
    #                         # or (str[:4]=='肿瘤侵犯')
    #                         if (str[:4]=='局部浸润')  or (str[:4]=='肿瘤浸润') or (str[:4]=='局灶浸润') :
    #                             infilt=str[4:]
    #                             infiltrations.append(infilt)
    #                         else:
    #                             pattern=re.compile('局限于.*内')
    #                             result=re.search(pattern,str)
    #                             if result:
    #                                 index1=result.span()[0]
    #                                 index2=result.span()[1]
    #                                 infilt=str[index1+3:index2-1]
    #                                 infiltrations.append(infilt)
    #                             else:
    #                                 if str[:5]=='癌组织浸润':
    #                                     infilt = str[5:]
    #                                     infiltrations.append(infilt)
    #                                 else:
    #                                     pattern=re.compile('受.*浸润')
    #                                     result = re.search(pattern, str)
    #                                     if result:
    #                                         index = re.search(pattern, str).span()[0]
    #                                         infilt = str[:index]
    #                                         infiltrations.append(infilt)
    #                                     else:
    #                                         pattern = re.compile('”(.*)”')
    #                                         result=re.findall(pattern,str)
    #                                         if result:
    #                                             infiltrations+=result
    #                                         else:
    #                                             pass
    #                                             # print(str)
    #                                             # infiltrations.append(str)
    #
    #     # return x
    #     x=infiltrations
    #     x = list(filter(None, x))
    #     x=list(set(x))
    #     if not x:
    #         return
    #     # 改变list形式
    #     str = x[0]
    #     if len(x) > 1:
    #         for i in range(len(x)):
    #             if i == 0:
    #                 continue
    #             str += '，'
    #             str += x[i]
    #     return str
    #
    # split_df['浸润']=split_df['浸润'].apply(get_infiltration)

    # 放到splits中去做
    # 获取病理等级的值
    # def get_pathological_grade(x):
    #     if pd.isnull(x):
    #         return
    #     else:
    #         pattern=re.compile('(Ⅰ|Ⅱ|Ⅲ|Ⅳ|II)(.*)级')
    #         pathological_grade=re.search(pattern,x)
    #         if pathological_grade:
    #             return pathological_grade.group()
    #         else:
    #             return x
    split_df['病理等级']=split_df['病理等级'].apply(remove_list)

    # 获取转移比例的值
    def get_Transfer_ratio(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')

        # 无需去重，文本中本身有可能重复出现
        # 去重并保留原来顺序
        # x_sort=list(set(x))
        # x_sort.sort(key=x.index)
        # x=x_sort

        x=[i.replace(' ','') for i in x]
        return '，'.join(x)

        # str = x[0]
        # if len(x) > 1:
        #     for i in range(len(x)):
        #         if i == 0:
        #             continue
        #         str += '，'
        #         str += x[i]
        # return str

    split_df['转移比例']=split_df['转移比例'].apply(get_Transfer_ratio)

    # 获取脉管侵犯的值
    def get_Vascular_invasion(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        records=[]
        for i in range(len(x)):
            if ('未见' in x[i]) or('-' in x[i]):
                # return '无'
                records.append(False)
            elif ('见' in x[i]) or ('+' in x[i]) or ('癌栓' in x[i]) or ('瘤栓' in x[i])or ('存在' in x[i])or('侵犯' in x[i])or('创' in x[i]):
                records.append(True)
                # return '有'
        if not records:
            return
        elif True in records:
            return '有'
        elif False in records:
            return '无'
        else:
            return records

    split_df['脉管侵犯']=split_df['脉管侵犯'].apply(get_Vascular_invasion)

    # 获取神经侵犯的值
    def get_Nerve_invasion(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        records = []
        for i in range(len(x)):
            if ('未见' in x[i]) or('-' in x[i]):
                # return '无'
                records.append(False)
            elif ('见' in x[i]) or ('侵犯' in x[i]) or ('存在' in x[i])\
                    or('侵及' in x[i])or('包绕' in x[i])or('累及' in x[i])or ('+' in x[i]):
                # return '有'
                records.append(True)
        if not records:
            return
        elif True in records:
            return '有'
        elif False in records:
            return '无'
        else:
            return records


    split_df['神经侵犯']=split_df['神经侵犯'].apply(get_Nerve_invasion)

    # 获得 三种切端是否累及 的值
    def get_Cut(x):
        if pd.isnull(x):
            return
        if x[0]!='[':
            return x
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        result=[]
        for i in x:
            if ('均未见') in i or('未见' in i)or('阴性' in i):
                # return '否'
                result.append(False)
            elif ('均见' in i) or('见' in i)or('阳性' in i):
                # return '是'
                result.append(True)
        if result:
            if True in result:
                return '是'
            return '否'
        # return x
        return
    split_df['上切端是否累及'] = split_df['上切端是否累及'].apply(get_Cut)
    split_df['下切端是否累及'] = split_df['下切端是否累及'].apply(get_Cut)
    split_df['基底切端是否累及'] = split_df['基底切端是否累及'].apply(get_Cut)
    split_df['回肠切端是否累及'] = split_df['回肠切端是否累及'].apply(get_Cut)
    split_df['结肠切端是否累及'] = split_df['结肠切端是否累及'].apply(get_Cut)
    split_df['网膜是否累及'] = split_df['网膜是否累及'].apply(get_Cut)
    split_df['阑尾是否累及'] = split_df['阑尾是否累及'].apply(get_Cut)

    # # 获得 下切端是否累及 的值
    # def get_downCut(x):
    #     if pd.isnull(x):
    #         return
    #     elif ('均未见' in x) or('未见' in x):
    #         return '否'
    #     else:
    #         return '是'
    # split_df['下切端是否累及'] = split_df['下切端是否累及'].apply(get_downCut)
    #
    #
    # # 获得 基底切端是否累及 的值
    # def get_baseCut(x):
    #     if pd.isnull(x):
    #         return
    #     elif ('均未见' in x) or ('未见' in x):
    #         return '否'
    #     else:
    #         return '是'
    # split_df['基底切端是否累及'] = split_df['基底切端是否累及'].apply(get_baseCut)

    # 获得 分化等级 的值
    def get_differentiation(x):
        if pd.isnull(x):
            return
        # 来自结构化样本的，非list
        if x[0]!='[':
            return x
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        for i in range(len(x)):
            x[i]=x[i].replace(' ','')
        x=list(set(x))
        #去掉list的形式
        str = x[0]
        if len(x) > 1:
            for i in range(len(x)):
                if i == 0:
                    continue
                str += '，'
                str += x[i]
        return str
    split_df['分化等级'] = split_df['分化等级'].apply(get_differentiation)

    def get_character(x):
        if pd.isnull(x):
            return
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        for i in range(len(x)):
            if '（' in x[i]:
                x[i] = x[i].split('（')[1]
            if '）' in x[i]:
                x[i] = x[i].split('）')[0]
            x[i] = x[i].replace(' ', '')
        x=list(set(x))
        for i in range(len(x)):
            x[i]=x[i].replace(' ','')
            if '，' in x[i]:
                splits=x[i].split('，')
                x[i]=splits[1]
        x = list(set(x))
        if '结合免疫表型' in x:
            x.remove('结合免疫表型')
        if '免疫表型' in x:
            x.remove('免疫表型')
        if '轻度异型' in x:
            x.remove('轻度异型')
        # 去掉list的形式
        if not x:
            return
        str = x[0]
        if len(x) > 1:
            for i in range(len(x)):
                if i == 0:
                    continue
                str += '，'
                str += x[i]
        return str

        # if pd.isnull(x):
        #     return
        # else:
        #     pattern=re.compile('(、|（|\()(.*?)型')
        #     result=re.search(pattern,x)
        #     if result:
        #         return result.group()[1:]
        #     else:
        #         return x
    split_df['性状'] = split_df['性状'].apply(get_character)


    # 获得 淋巴结是否转移 的值
    def get_lymphaden(x):
        if pd.isnull(x):
            return
        if x[0]!='[':
            return x
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        bool_list=[]
        for i in x:
            if ('均未见' in i) or ('未见' in i):
                bool_list.append(False)
            # return '否'
            elif '见' in i:
                bool_list.append(True)
                # return '是'
        if not bool_list:
            return
        if True in bool_list:
            return '是'
        return '否'
        # if bool_list:
        #     result=True
        #     for i in bool_list:
        #         # 有一个False，result就是False
        #         result=(result and i)
        #     if result:
        #         return '是'
        #     return '否'
        # else:
        #     return x
    split_df['淋巴结是否转移'] = split_df['淋巴结是否转移'].apply(get_lymphaden)

    # 获得 参见报告 的值
    def get_report(x):
        if pd.isnull(x):
            return
        if x[0]!='[':
            return x
        x = x.replace("'", '')
        if x == '[]':
            return
        else:
            x = x[1:-1]
            x = x.split(',')
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        # 只保留数字、字母和-
        chosen_indexes=[]
        new_x=[]
        for i in range(len(x)):
            # 先删除中文
            x[i]=re.sub(pattern,'',x[i])
            # 再保留数字字母和-
            x[i] = "".join(filter(lambda ch: (ch in '——-') or(ch.isdigit()) or(ch.isalpha()), x[i]))
            # 表明多份报告合在了一起
            if len(re.findall('F',x[i]))>1:
                splits=x[i].split('F')
                splits = list(filter(None, splits))
                for s in range(len(splits)):
                    if splits[s][0]!='F':
                        splits[s]='F'+splits[s]
                chosen_indexes.append(i)
                new_x+=splits
        x=[x[i] for i in range(len(x)) if i not in chosen_indexes]
        x+=new_x
        x=list(set(x))
        x = list(filter(None, x))
        # eg.['结合原单位报告单上提供的免疫组化标记结果']没了
        if x:
            # 去掉list的形式
            str = x[0]
            if len(x) > 1:
                for i in range(len(x)):
                    if i == 0:
                        continue
                    str += '，'
                    str += x[i]
            return str
        return


    split_df['肠旁淋巴结个数'] = split_df['肠旁淋巴结个数'].apply(remove_list)


    split_df['参见报告'] = split_df['参见报告'].apply(get_report)





    pass
    # split_df.to_csv('../EMR_result/value_df.csv',index=False,encoding='GB2312')
    # split_df.to_csv('../EMR_result/value_df.csv',index=False)
    split_df.to_csv(value_df_path, index=False, encoding=to_encoding)
    return split_df

if __name__=='__main__':
    split_df_path='split_df.csv'
    value_df_path='value_df.csv'
    to_encoding='GB2312'
    value_df=get_value_df(to_encoding=to_encoding)