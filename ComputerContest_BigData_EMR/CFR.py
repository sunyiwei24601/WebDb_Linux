import re
import pandas as pd
# import jieba
# jieba.load_userdict('my_dict.txt')
from pandas import DataFrame
# path=r'D:\SUFE\ComputerContest_BigData\EMR_result\split_df.csv'
# EMR_df=pd.read_csv(path,encoding='gb2312')


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
# infiltration=EMR_df['浸润'].apply(remove_list)

# for i in infiltration:
#     if pd.isnull(i):
#         continue
#     i=i.replace('”','')
#     i = i.replace(' ', '')
#     l=i.split('，')
#     # print (l)
#     for j in l:
#         print(jieba.lcut(j))

def get_labeledData1():
    EMR_df_norm_path = 'EMR_df_norm.csv'
    EMR_df = pd.read_csv(EMR_df_norm_path, encoding='gb2312')
    EMR_df.columns = ['索引', '文本内容']
    EMR_df = EMR_df.groupby('索引')

    def get_label(x):
        x = x.iloc[0]
        str=''
        for i in x:
            str+=i
            str+='O'
        return str


    label_df = EMR_df['文本内容'].apply(get_label)
    pass
    label_df.to_csv("../LabeledData/label_df.csv", encoding='GB2312')

def get_SPE_label():
    path=r'D:\SUFE\ComputerContest_BigData\LabeledData\SPE.csv'
    df=pd.read_csv(path,index_col=False)

    def add_BIO(x):
        str=''
        if pd.isnull(x):
            return
        for i in range(len(x)):
            if x[i]==',':
                continue
            str+=x[i]
            if i==0:
                str+='B-SPE'
            elif x.find('，')==i-1:
                str += 'B-SPE'
            elif x[i]=='，':
                continue
            else:
                str += 'I-SPE'

        return str
    df['标本'] = df['标本'].apply(add_BIO)
    df.to_csv(r'D:\SUFE\ComputerContest_BigData\LabeledData\SPE_labeled.csv',index=False)

def get_SPE_label2():
    EMR_df_norm_path = 'EMR_df_norm.csv'
    EMR_df = pd.read_csv(EMR_df_norm_path, encoding='gb2312')
    EMR_df.columns = ['索引', '文本内容']

    SPE=[]

    for x in EMR_df['文本内容']:

        # 分句
        splits = re.split(pattern='，|。|：|；|\s|:', string=x)
        splits = list(filter(None, splits))

        # list元素拆分
        # 形如：”直肠癌根治标本”中分化腺癌，被切为：”直肠癌根治标本”,中分化腺癌
        # 用for的话会让后面的被切开
        if '”' in splits[0]:
            sep = '”'
            str = splits[0]
            i_splits = str.split('”')
            splits.pop(0)
            splits = i_splits + splits
        splits = list(filter(None, splits))

        flag = False
        for j in splits:
            if ('标本' in j):
                print(j)
                SPE.append(j)
                flag = True
        if flag == False:
            print(x)
            SPE.append(x)
    for i in range(len(SPE)):
        # if '标本' in SPE[i]:
        #     index = re.search('标本', SPE[i]).regs[0][1]
        #     SPE[i] = SPE[i][:index]
        if (SPE[i][0]=='”') and (SPE[i][-1]=='”'):
            SPE[i]=SPE[i][1:-1]
        if SPE[i].count('”')==1:
            SPE[i] = SPE[i].replace('”','')
        result = re.search('”.*标本”', SPE[i])
        if result:
            SPE[i]=result.group().replace('”','')
    SPE=[i for i in SPE if i!='标本']
    SPE = [i for i in SPE if i != '根治标本']
    SPE = [i for i in SPE if i != '标本类型']
    SPE = [i for i in SPE if i != '切除标本']
    SPE = [i for i in SPE if i[-2:] != '标本']
    SPE_df=DataFrame(SPE,columns=['SPE'])
    pass

def get_SPEclassify():
    path='D:\SUFE\ComputerContest_BigData\EMR_coding\split_df.csv'
    split_df = pd.read_csv(path, encoding='gb2312')
    done_SPE=[]
    todo_SPE=[]
    for x in split_df['标本']:
        x = x.replace("'", '')
        x = x[1:-1]
        x = x.split(',')
        x = list(set(x))

        for s in x:
            # s=s.replace(' ','')
            # if s=='标本':
            #     continue
            if s[-2:]=='标本':
                # s=s.replace('另送','')
                # s= "".join(filter(lambda ch: ch not in '0123456789.',s))
                s=s.replace(' ','')
                done_SPE.append(s)
            else:
                todo_SPE.append(s)

    done_SPE_df=DataFrame(done_SPE,columns=['done_SPE'])
    todo_SPE_df = DataFrame(todo_SPE, columns=['todo_SPE'])
    done_SPE_df.to_csv('../LabeledData/done_SPE_df.csv',encoding='gb2312')
    todo_SPE_df.to_csv('../LabeledData/todo_SPE_df.csv', encoding='gb2312')
    pass

# def filter_todo_SPE_df():
#     path='../LabeledData/todo_SPE_df.csv'
#     todo_SPE_df = pd.read_csv(path, encoding='gb2312',index_col=0)
#     def get_filter_todo_SPE(x):
#         if ('+' not in x):
#             if '标本' in x:
#                 index = re.search('标本', x).regs[0][1]
#                 x=x[:index]
#         return x
#
#     todo_SPE_df['filter_todo_SPE']=todo_SPE_df['todo_SPE'].apply(get_filter_todo_SPE)
#     todo_SPE_df.to_csv('../LabeledData/filter_todo_SPE.csv', encoding='gb2312')
#     pass

def get_infiltrate_data():
    path='../LabeledData/Inf_labeled.csv'

    with open(path,encoding='utf8') as f:
        lines=  f.readlines()
    Data=[]
    for line in lines:
        sample=''
        for i in line:
            sample+=i
            if i in ['O','B','I']:
                sample+='\n'
            if (re.match('[\u4e00-\u9fa5]',i)) or (i in 'a-cm（）、/”ⅠⅡⅢⅣ1234567890.①②③④⑤⑥⑦⑧⑨') :
                sample += ' '
        Data.append(sample)
    for i in range(len(Data)):
        if re.match('^\s',Data[i]):
            Data[i]=re.sub('^\s','',Data[i])
        Data[i]=Data[i].replace('I','I-INF')
        Data[i] = Data[i].replace('B', 'B-INF')
        if re.search('\nI-INF',Data[i]):
            Data[i]=re.sub('\nI-INF','',Data[i])
        if re.search('\nB-INF',Data[i]):
            Data[i]=re.sub('\nB-INF','',Data[i])
        if re.search('\nO',Data[i]):
            Data[i]=re.sub('\nO','',Data[i])

    num=len(Data)
    indexs=[i for i in range(num)]
    import random
    train_indexs=random.sample(indexs, int(num*0.7))
    dev_indexs=random.sample([ i for i in indexs if i not in train_indexs], int(num*0.2))
    test_indexs = [i for i in indexs if i not in dev_indexs and i not in train_indexs]

    train=[Data[i] for i in train_indexs]
    dev = [Data[i] for i in dev_indexs]
    test = [Data[i] for i in test_indexs]

    with open(r'D:\SUFE\ComputerContest_BigData\ChineseNER-master\data/INF.Data', 'w+',encoding='utf8') as f:
        for i in Data:
            f.write(i)
    with open(r'D:\SUFE\ComputerContest_BigData\ChineseNER-master\data/INF.train', 'w+',encoding='utf8') as f:
        for i in train:
            f.write(i)
    with open(r'D:\SUFE\ComputerContest_BigData\ChineseNER-master\data/INF.dev', 'w+',encoding='utf8') as f:
        for i in dev:
            f.write(i)
    with open(r'D:\SUFE\ComputerContest_BigData\ChineseNER-master\data/INF.test', 'w+',encoding='utf8') as f:
        for i in test:
            f.write(i)

    pass

def get_todo_SPE_Data():
    todo_SPE_df = pd.read_csv('../LabeledData/todo_SPE_df.csv', encoding='gb2312', index_col=0)
    with open('ChineseNER_master2/data/todo_SPE.Data', 'w+', encoding='utf8') as f:
        for x in todo_SPE_df['todo_SPE']:
            for s in x:
                for i in range(len(s)):
                    f.write(s[i])
                    f.write('O')
            f.write('\n')


def get_spe_data():
    Data=[]
    with open('ChineseNER_master2/data/todo_SPE.Data', 'r', encoding='utf8') as f:
        todo_lines=f.readlines()

    for line in todo_lines:
        sample=''
        for i in line:
            sample+=i
            # f.write(i)
            if i in 'BIO':
                sample += '\n'
                # f.write('\n')
            elif i=='\n':
                continue
            else:
                sample += ' '
                # f.write(' ')
        Data.append(sample)
    done_SPE_df = pd.read_csv('../LabeledData/done_SPE_df.csv', encoding='gb2312', index_col=0)
    for line in done_SPE_df['done_SPE']:
        sample = ''
        for i in range(len(line)):
            sample += line[i]
            sample+=' '
            if i==0:
                sample += 'B'
            else:
                sample += 'I'
            sample += '\n'
        sample += '\n'

        Data.append(sample)

    for i in range(len(Data)):
        if re.match('^\s',Data[i]):
            Data[i]=re.sub('^\s','',Data[i])
        Data[i]=Data[i].replace('I','I-SPE')
        Data[i] = Data[i].replace('B', 'B-SPE')
        if re.search('\nI-SPE',Data[i]):
            Data[i]=re.sub('\nI-SPE','',Data[i])
        if re.search('\nB-SPE',Data[i]):
            Data[i]=re.sub('\nB-SPE','',Data[i])
        if re.search('\nO',Data[i]):
            Data[i]=re.sub('\nO','',Data[i])


    num=len(Data)
    indexs=[i for i in range(num)]
    import random
    train_indexs=random.sample(indexs, int(num*0.7))
    dev_indexs=random.sample([ i for i in indexs if i not in train_indexs], int(num*0.2))
    test_indexs = [i for i in indexs if i not in dev_indexs and i not in train_indexs]

    train=[Data[i] for i in train_indexs]
    dev = [Data[i] for i in dev_indexs]
    test = [Data[i] for i in test_indexs]

    with open(r'ChineseNER_master2/data/SPE.Data', 'w+',encoding='utf8') as f:
        for i in Data:
            f.write(i)
    with open(r'ChineseNER_master2/data/SPE.train', 'w+',encoding='utf8') as f:
        for i in train:
            f.write(i)
    with open(r'ChineseNER_master2/data/SPE.dev', 'w+',encoding='utf8') as f:
        for i in dev:
            f.write(i)
    with open(r'ChineseNER_master2/data/SPE.test', 'w+',encoding='utf8') as f:
        for i in test:
            f.write(i)



    # for x in done_SPE_df['done_SPE']:
    # sample = ''
    # for s in x:
    #     for i in range(len(s)):
    #         f.write(s[i])
    #         f.write('O')
    # f.write('\n')

    #
    #     for x in split_df['标本']:
    #         x = x.replace("'", '')
    #         x = x[1:-1]
    #         x = x.split(',')
    #         x = list(set(x))
    #         for s in x:
    #             if s[-2:] == '标本':
    #                 for i in range(len(s)):
    #                     if i==0:
    #                         f.write(s[i])
    #                         f.write(' B\n')
    #                     else:
    #                         f.write(s[i])
    #                         f.write(' I\n')
    #             else:
    #                 for i in range(len(s)):
    #                     f.write(s[i])
    #                     f.write(' O\n')
    #         f.write('\n')

get_spe_data()