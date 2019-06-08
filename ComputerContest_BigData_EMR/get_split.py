import re
import pandas as pd
import jieba
jieba.load_userdict('my_dict.txt')
from pandas import DataFrame
# path=r'../EMR_result/EMR_df_norm.csv'
# EMR_df=pd.read_csv(path,encoding='gb2312')


def get_split_df(EMR_df_norm_path='EMR_df_norm.csv',split_df_path='split_df.csv'):
    EMR_df = pd.read_csv(EMR_df_norm_path, encoding='gb2312')
    EMR_df.columns = ['索引', '文本内容']
    def get_split(x):
        x=x.iloc[0]


        # 需要提取的字段属性
        attributes=['标本','病理','上切端是否累及','下切端是否累及','基底切端是否累及',
                              '病理等级','肿瘤大小','分化等级','浸润','淋巴结是否转移',
                    '转移比例','脉管侵犯','神经侵犯','性状']
        attributes2=['回肠切端是否累及','结肠切端是否累及','网膜是否累及','阑尾是否累及','肠旁淋巴结个数']

        # 字段属性缩写，以直接匹配文本
        abbreviation_attributes=['标本','癌','上切端','下','基底',
                              '级','大小','分化','浸润','淋巴结',
                                 '枚','脉管','神经','型']

        # 参考https://www.91360.com/201603/60/26613.html结肠癌的组织学分型
        pathologies1 = ['乳头状腺癌', '管状腺癌', '黏液腺癌', '粘液腺癌','梭形细胞癌','筛状粉刺型腺癌','髓样癌','微乳头状癌',
                        '印戒细胞癌','大细胞癌','小细胞癌', '未分化癌','锯齿状腺癌','混合型腺神经内分泌癌','间质肿瘤',
                       '腺鳞癌', '鳞状细胞癌', '胰腺导管腺癌','透明细胞癌','黏液癌','错构瘤','淋巴瘤',
                        '绒毛状管状腺瘤','管状-绒毛状腺瘤','管状绒毛状腺瘤','癌疑']
        pathologies2 = [ '导管腺癌', '细胞癌','管状腺瘤', '神经内分泌癌','神经内分泌瘤']
        pathologies3=['腺癌','腺瘤']

        df=DataFrame(columns=attributes+attributes2+['参见报告','其他'])

        # 所有已知的性状
        charalist1 = ['溃疡隆起型', '弥漫溃疡型', '弥漫浸润型', '浅表隆起型','表浅隆起型',
                     '髓样型', '局限溃疡型',  '溃疡浸润型',
                     '表浅平坦型','浅表平坦型', '糜烂型', '浅表溃疡型', '肌壁间型',
                      '伴中度异型', '内膜下型', '壁间型', '肠型',
                     '斑块型', '大细胞型', '小细胞型',
                      '盘状型', '外生型',
                     '溃疡增殖型', '髓质型', '浅表凹陷型','表浅凹陷型', '嗜酸细胞型',
                     '浸润至型', '浆膜下型','不明确型',
                      'Ⅰ型','Ⅱ型','Ⅱa型','Ⅱb型','Ⅱc型','ⅡA型','ⅡB型','ⅡC型','Ⅲ型'
                      ]
        charalist2 = ['浸润型','增殖型','隆起型','平坦型','凹陷型','溃疡型',
                      '胶样型','菜花型','蕈伞型','中央型','周围型','弥漫型', '表浅型']

        # 参考https://www.haodf.com/zhuanjiaguandian/yangjundoctor_1581964542.htm 肿瘤的分型、分级和分期
        differentiations1 = [
            '中低分化', '中-低分化',
            '中-高分化', '中高分化']
        differentiations2 = ['高分化', '中分化', '低分化'
                             ]
        differentiations3 = ['g2', 'g1', 'g3', 'g4',
                             'G2', 'G1', 'G3', 'G4']

        upCut_synonym = ['上切端', '上切缘', '两侧切端', '两切端', '上、下切端', '上、下切缘', '两侧切缘', '两切缘']
        downCut_synonym = ['下切端', '下切缘', '两侧切端', '两切端', '上、下切端', '上、下切缘', '两侧切缘', '两切缘']
        involving_synonym = ['癌累及', '癌组织', '见肿瘤', '肿瘤累及', '癌组织累及', '癌','侵犯','阴性','阳性']

        # 匹配所有参见报告
        # 不区分样本是否结构化
        records=[]
        splits = re.split(pattern='，|。|：|；|\s|:', string=x)
        splits = list(filter(None, splits))

        # 记录splits中被选择过的字段索引
        chosen_indexs = []
        for j  in splits:
            if '报告' in j:
                records.append(j)
                chosen_indexs.append(splits.index(j))
        chosen_indexs=list(set(chosen_indexs))
        df['参见报告']=[records]

        # 针对结构化样本
        if '标本类型:' in x:
            splits = x.split('  ')
            splits = list(filter(None, splits))
            # print(splits)
            dict_splits = {}
            for s in splits:
                s=re.split('[:：]',s)
                for i in range(len(s)):
                    s[i]=s[i].strip()
                # s = s.split()
                try:
                    dict_splits[s[0]] = s[1]
                except:
                    pass
            try:
                df['标本'] = [[dict_splits['标本类型']]]
            except:
                pass
            try:
                records=[]
                j = dict_splits['组织学类型']
                # if '（' in pathology:
                #     pathology = pathology.split('（')[0]
                for p in pathologies1:
                    if p in j:
                        records.append(p)
                        j=j.replace(p,'')
                for p in pathologies2:
                    if p in j:
                        records.append(p)
                        j=j.replace(p,'')
                for p in pathologies3:
                    if p in j:
                        records.append(p)
                if records:
                    df['病理'] = [records]
                # else:
                #     df['病理'] = [[j]]
            except:
                pass

            # df['病理等级']=dict_splits['']
            try:
                records=[]
                for j in splits:
                    if '大小' in j:
                        pattern = re.compile(r'\d[^\u4e00-\u9fa5]*cm')
                        tumour_size = pattern.findall(j)
                        records+=tumour_size
                df['肿瘤大小'] = [records]
                # df['肿瘤大小'] = [[dict_splits['肿瘤大小']]]
            except:
                pass
            try:
                df['分化等级'] = [dict_splits['组织学分级']]
            except:
                df['分化等级']=[[]]
            try:
                if re.search('[，；。,:.]',dict_splits['肿瘤扩散']):
                    spreads=re.split('[，；。,:.]',dict_splits['肿瘤扩散'])
                else:
                    spreads=[dict_splits['肿瘤扩散']]
                df['浸润'] = [spreads]
            except:
                pass
            linba=''
            try:
                linba+=dict_splits['胰周淋巴结转移情况']
            except:
                pass
            try:
                linba += dict_splits['其他淋巴结转移情况']
            except:
                pass
            df['淋巴结是否转移'] = [[linba]]
            df['转移比例']=[re.findall('\d{1,2}\/\d{1,2}',x)]
            try:
                df['脉管侵犯'] = [[dict_splits['脉管内癌栓']]]
            except:
                pass
            try:
                df['神经侵犯'] = [[dict_splits['神经侵犯']]]
            except:
                pass
            records=[]
            for c in charalist1:
                if c in x:
                    records.append(c)
                    # 具体的找到后在x中删除
                    x=x.replace(c,'')
            for c in charalist2:
                if c in x:
                    records.append(c)
            df['性状']=[records]

            # 匹配所有‘上切端’
            records = []
            for j in splits:
                upCut_synonym_match = [True for cut in upCut_synonym if cut in j]
                if (True in upCut_synonym_match) and ('距' not in j):
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['上切端是否累及'] = [records]

            # 匹配所有‘下切端’
            records = []
            for j in splits:
                downCut_synonym_match = [True for cut in downCut_synonym if cut in j]
                if (True in downCut_synonym_match) and ('距' not in j):
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['下切端是否累及'] = [records]

            # 匹配所有‘基底切端’
            records = []
            for j in splits:
                if ('基底' in j)and ('距' not in j) :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['基底切端是否累及'] = [records]

            # 匹配所有‘回肠切端’
            records = []
            for j in splits:
                if '回肠切端' in j:
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['回肠切端是否累及'] = [records]

            # 匹配所有‘结肠切端’
            records = []
            for j in splits:
                if '结肠切端' in j:
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['结肠切端是否累及'] = [records]

            # 匹配所有‘网膜’
            records = []
            for j in splits:
                if ('网膜' in j) and ('网膜结节' not in j):
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['网膜是否累及'] = [records]

            # 匹配所有‘阑尾’
            records = []
            for j in splits:
                if '阑尾' in j:
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['阑尾是否累及'] = [records]

            records=[]
            # 匹配 肠旁淋巴结
            for j in splits:
                number = re.findall('肠旁淋巴结(.*\d)枚?', j)
                if number:
                    for n in range(len(number)):
                        if '枚' in number[n]:
                            index=number[n].index('枚')
                            number[n]=number[n][:index]
                        if '/' in number[n]:
                            number[n] = number[n].split('/')[1]
                        number[n] = "".join(filter(lambda ch: ch in '0123456789', number[n]))
                        number[n]=number[n].replace(' ','')
                    records+=number
                    chosen_indexs.append(splits.index(j))
            records = list(filter(None, records))
            records=list(set(records))
            df['肠旁淋巴结个数'] = [records]


            records=[]
            # 匹配病理等级
            pattern = re.compile('[ⅠⅡⅢⅣ][^\u4e00-\u9fa5]*?级')
            for j in splits:
                pathological_grade = re.search(pattern, j)
                if pathological_grade:
                    chosen_indexs.append(splits.index(j))
                    result=pathological_grade.group()
                    records.append(result)
            for ii in range(len(records)):
                records[ii]=records[ii].replace(' ','')
            records=list(set(records))
            df['病理等级'] = [records]

            return df
        # 非结构化样本
        else:

            # 分句
            splits=re.split(pattern='，|。|：|；|\s|:',string=x)
            splits = list(filter(None, splits))

            # 删除与报告相关的字段
            # splits = [splits[i] for i in range(len(splits)) if i not in chosen_indexs]


            # list元素合并        # 合并 切端、累及        # 分三种情况，合在一起有点难写
            for i in range(len(splits)):
                if i==len(splits)-1:
                    break
                upCut_synonym_match=[True for cut in upCut_synonym if cut in splits[i]]
                if (True in upCut_synonym_match) and ('距' not in splits[i]):
                # if ('上切端' in splits[i]) or('上切缘' in splits[i]) or\
                #         ('两侧切端' in splits[i])or('两切端' in splits[i])or ('上、下切端' in splits[i]) or\
                #         ('两侧切缘' in splits[i])or('两切缘' in splits[i]):
                    # 无需合并splits后面的
                    # 不能只写'肿瘤'
                    involving_synonym_match=[True for involve in involving_synonym if involve in splits[i]]
                    if True in involving_synonym_match:
                    # if ('癌累及' in splits[i]) or ('癌组织' in splits[i]) \
                    #         or('见肿瘤' in splits[i])or('肿瘤累及' in splits[i]) or('癌组织累及' in splits[i]):
                        continue
                    back_splits = splits[i + 1:]
                    for j in back_splits:
                        involving_synonym_match_j=[True for involve in involving_synonym if involve in j]
                        if True in involving_synonym_match_j:
                        # if ('癌累及' in j) or ('癌组织' in j) \
                        #         or ('见肿瘤' in j) or ('肿瘤累及' in j) or ('癌组织累及' in j):
                        #     print(splits[i],j)
                            splits[i]=splits[i]+j
                            # 不用删除，别的切端还用得到
                            # splits.remove(j)
                            break
                    # for...else...语句，跳出双层for循环
                    else:
                        continue
                    break
            for i in range(len(splits)):
                if i==len(splits)-1:
                    break
                downCut_synonym_match = [True for cut in downCut_synonym if cut in splits[i]]
                if (True in downCut_synonym_match)and ('距' not in splits[i]):
                    # 无需合并splits后面的
                    involving_synonym_match=[True for involve in involving_synonym if involve in splits[i]]
                    if True in involving_synonym_match:
                        continue
                    back_splits = splits[i + 1:]
                    for j in back_splits:
                        involving_synonym_match_j = [True for involve in involving_synonym if involve in j]
                        if True in involving_synonym_match_j:
                            splits[i]=splits[i]+j
                            # 不用删除，别的切端还用得到
                            # splits.remove(j)
                            break
                    # for...else...语句，跳出双层for循环
                    else:
                        continue
                    break
            for i in range(len(splits)):
                if i==len(splits)-1:
                    break
                if '基底' in splits[i]:
                    # 无需合并splits后面的
                    involving_synonym_match=[True for involve in involving_synonym if involve in splits[i]]
                    if (True in involving_synonym_match)and ('距' not in splits[i]):
                        continue
                    back_splits = splits[i + 1:]
                    for j in back_splits:
                        involving_synonym_match_j = [True for involve in involving_synonym if involve in j]
                        if True in involving_synonym_match_j:
                            splits[i]=splits[i]+j
                            # 不用删除，别的切端还用得到
                            # splits.remove(j)
                            break
                    # for...else...语句，跳出双层for循环
                    else:
                        continue
                    break
            new_cuts=['回肠切端','结肠切端','网膜','阑尾']
            for new_cut in new_cuts:
                for i in range(len(splits)):
                    if i==len(splits)-1:
                        break
                    if new_cut in splits[i]:
                        if (new_cut=='网膜') and ('网膜结节' in splits[i]):
                            continue
                        if (new_cut == '阑尾') and ('阑尾炎' in splits[i]):
                            continue
                        # 无需合并splits后面的
                        involving_synonym_match=[True for involve in involving_synonym if involve in splits[i]]
                        if True in involving_synonym_match:
                            continue
                        back_splits = splits[i + 1:i+4]
                        for j in back_splits:
                            involving_synonym_match_j = [True for involve in involving_synonym if involve in j]
                            if True in involving_synonym_match_j:
                                splits[i]=splits[i]+j
                                # 不用删除，别的切端还用得到
                                # splits.remove(j)
                                break
                        # for...else...语句，跳出双层for循环
                        else:
                            continue
                        break

            # 合并 淋巴结、转移
            # 需要合并所有的，因为前面可能提到淋巴结但跟这个属性无关
            flag=True
            while flag:
                for i in range(len(splits)):
                    if i==len(splits)-1:
                        # 表明到了最后，还未发现可以合并的
                        flag=False
                        break
                    # 4个条件都要满足
                    if ('淋巴结' in splits[i] and ('转移' not in splits[i]) and ('肿瘤' not in splits[i]) and ('癌组织' not in splits[i])):
                        if  ('转移' in splits[i+1]) or ('肿瘤' in splits[i+1]) or ('癌组织' in splits[i+1]):
                            # print(splits[i],splits[i+1])
                            splits[i]=splits[i]+splits[i+1]
                            splits.pop(i + 1)
                            break

            # list元素拆分
            # 形如：”直肠癌根治标本”中分化腺癌，被切为：”直肠癌根治标本”,中分化腺癌
            # 用for的话会让后面的被切开
            if '标本”' in splits[0]:
                sep='标本”'
                str=splits[0]
                i_splits=str.split('”')
                splits.pop(0)
                splits = i_splits + splits
            splits = list(filter(None, splits))
            # 不止开头，后面也可能有，但可以谨慎一些切
            flag=True
            while flag:
                for j in range(len(splits)):
                    if j==0:
                        continue
                    #标本”后面的字，拆出成新的元素
                    if '标本”'in splits[j]:
                        sep = '标本”'
                        str=splits[j]
                        index = str.find(sep) + 3
                        j_splits=[str[:index]]+[str[index:]]
                        splits.pop(j)
                        splits[j:j]=j_splits
                        break
                # 遍历完了还没有发现可以拆分的
                flag=False

            # 合并肿瘤大小
            # eg.肿瘤大小:最大径0.05-5.5cm
            pattern = re.compile(r'\d.*?cm')
            for i in range(len(splits)):
                if i==len(splits)-1:
                    break
                if ('肿瘤大小' in splits[i]) and (not re.search(pattern,splits[i])):
                    back_splits = splits[i + 1:]
                    for j in back_splits:
                        if re.search(pattern, j):
                            splits[i] = splits[i] + j
                            splits.remove(j)
                            break
                    else:
                        continue
                    break

            # 清除list中空的元素
            splits=list(filter(None, splits))


            # 标本字段通常在最前
            # 并删除右引号”

            # 结构化样本中才可能
            # if splits[0]=='标本类型':
            #     specimen=splits[1]
            #     chosen_indexs.append(1)
            # else:
            # flag=False
            # for j in splits:
            #     if ('标本' in j) :
            #         print(j)
            #         flag=True
            # if flag==False:
            #     print(x)
            # specimen=[]
            # chs = re.compile(r'[\u4e00-\u9fa5]')
            # if chs.search(splits[0]):
            #     specimen.append(splits[0])
            #     chosen_indexs.append(0)
            # for j in splits[1:]:
            #     if '标本”' in j:
            #         result=re.search('”.*标本”',j)
            #         if result:
            #             s=result.group().replace('”','')
            #             specimen.append(s)
            #             chosen_indexs.append(splits.index(j))
            # df['标本'] = [specimen]
            # df['标本']=[.replace('”','')]
            SPE=[]
            flag = False
            # 找带有'标本'的分句
            for j in splits:
                if '标本' in j:
                    if ('标本' in j) and ('+' not in j):
                        index = re.search('标本',j).regs[0][1]
                        j = j[:index]
                        j = j.replace('”', '')
                    if (j[0] == '”') and (j[-1] == '”'):
                        j = j[1:-1]
                    if (j.count('”') == 2) and ('标本' in j):
                        j = j.replace('”', '')
                    if j=='标本':
                        continue
                    if j[-2:] == '标本':
                        j = j.replace('另送', '')
                        j = "".join(filter(lambda ch: ch not in '0123456789.', j))
                    if j:
                        j=j.replace(' ','')
                        SPE.append(j)
                        flag = True
            # 找形如”.*?活检”，并标准化
            result = re.findall('”.*?活检”', x)
            if result:
                for ii in range(len(result)):
                    word = "”"
                    s = result[ii]
                    w = [m.start() for m in re.finditer(word, s)]
                    result[ii]=s[w[-2]+1:w[-1]]
                    result[ii]=result[ii].replace(' ','')
                result=[(i+'标本') for i in result]
                result=list(set(result))
                SPE+=result
                flag = True

            # if flag == False:
            #     # print(x)
            #     # 找形如”.*?”：，并标准化
            #     pattern = re.compile('”.*?”：')
            #     result = pattern.findall(x)
            #     if result:
            #         for ii in range(len(result)):
            #             result[ii] = ''.join(re.findall('[\u4e00-\u9fa5]', result[ii]))
            #         result = list(filter(None, result))
            #         result=[(i+'标本') for i in result]
            #         # if result:
            #         #     if spe[-2:]!='标本':
            #         #         spe+='标本'
            #         #     SPE.append(spe)
            #         SPE+=result
            #         flag = True

            # 上述三种方法都没找到，就直接返回文本
            if flag == False:
                    SPE.append(x)

            for i in range(len(SPE)):
                result = re.search('”.*标本”', SPE[i])
                if result:
                    SPE[i] = result.group().replace('”', '')

                result = re.search('（.*标本）', SPE[i])
                if result:
                    SPE[i] = result.group().replace('（', '')
                    SPE[i] = SPE[i] .replace('）', '')

                # result = re.search('”.*”:', SPE[i])
                # if result:
                #     SPE[i] = result.group()
                SPE[i] = SPE[i].replace(' ', '')

            # 无异常
            # for i in SPE:
            #     if (i=='根治标本') or (i=='切除标本'):
            #         print(i)

            SPE = [i for i in SPE if i != '标本']
            SPE = [i for i in SPE if i != '根治标本']
            SPE = [i for i in SPE if i != '标本类型']
            SPE = [i for i in SPE if i != '切除标本']
            df['标本'] = [SPE]

            # 匹配所有‘上切端’
            records = []
            for j in splits[1:]:
                upCut_synonym_match=[True for cut in upCut_synonym if cut in j]
                if (True in upCut_synonym_match) and ('距' not in j):
                # if ('上切端' in j) or ('上切缘' in j) or \
                # ('两侧切端' in j) or ('两切端' in j) or ('上、下切端' in j) or\
                # ('两侧切缘' in j) or ('两切缘' in j):
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                    # if ('癌累及' in j) or ('癌组织' in j) \
                    #         or('见肿瘤' in j)or('肿瘤累及' in j)\
                    #         or('癌组织累及' in j) or( '癌' in j):
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['上切端是否累及'] = [records]

            # 匹配所有‘下切端’
            records = []
            for j in splits[1:]:
                downCut_synonym_match=[True for cut in downCut_synonym if cut in j]
                if (True in downCut_synonym_match)and ('距' not in j):
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['下切端是否累及'] = [records]

            # 匹配所有‘基底切端’
            records = []
            for j in splits[1:]:
                if ('基底' in j)and ('距' not in j) :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['基底切端是否累及'] = [records]

            # 匹配所有‘回肠切端’
            records = []
            for j in splits[1:]:
                if '回肠切端' in j :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['回肠切端是否累及'] = [records]

            # 匹配所有‘结肠切端’
            records = []
            for j in splits[1:]:
                if '结肠切端' in j :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['结肠切端是否累及'] = [records]

            # 匹配所有‘网膜’
            records = []
            for j in splits[1:]:
                if ('网膜' in j) and ('网膜结节' not in j) :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['网膜是否累及'] = [records]

            # 匹配所有‘阑尾’
            records = []
            for j in splits[1:]:
                if '阑尾' in j :
                    involving_synonym_match = [True for involve in involving_synonym if involve in j]
                    if True in involving_synonym_match:
                        records.append(j)
                        chosen_indexs.append(splits.index(j))
            df['阑尾是否累及'] = [records]

            # 匹配病理
            # records = []
            # for j in splits[1:]:
            #     if ('癌' in j) or ('瘤' in j) or ('胃炎' in j):
            #         records.append(j)
            #         chosen_indexs.append(splits.index(j))
            #         break
            # df['病理'] = records
            records = []
            # 匹配所有病理的字段
            for j in splits:
                for p in pathologies1:
                    # if (p in j) and ('转移' not in j) and ('改变' not in j):
                    if p in j :
                        records.append(p)

                        # 有可能j里有两次具体情况，删除第一次也会出错
                        try:
                            chosen_indexs.append(splits.index(j))
                        except:
                            pass
                        j = j.replace(p, '')
                        # 具体的值提取到后删除，防止宽泛的情况匹配
                for p in pathologies2:
                    # if (p in j) and ('转移' not in j) and ('改变' not in j):
                    if p in j:
                        records.append(p)
                        try:
                            # 如果j被修改了，无法找到，但之前已经记录过索引
                            chosen_indexs.append(splits.index(j))
                        except:
                            pass
                        j = j.replace(p, '')
                for p in pathologies3:
                    # if (p in j) and ('转移' not in j) and ('改变' not in j):
                    if p in j:
                        records.append(p)
                        # 有可能j里有两次具体情况，删除第一次也会出错
                        try:
                            chosen_indexs.append(splits.index(j))
                            # j = j.replace(p, '')
                        except:
                            pass
                # result=re.findall('符合.{0, 10}癌',j)
                # if result:
                #     if ('转移' not in j) and ('改变' not in j):
                #         records +=result
                #         chosen_indexs.append(splits.index(j))
            # if records==[]:
            #     for j in splits[1:]:
            #         j_splits=jieba.lcut(j)
            #         if ('腺癌' in j) and ('转移' not in j) and ('改变' not in j):
            #             records.append('腺癌')
            #             chosen_indexs.append(splits.index(j))
            records=list(set(records))
            # 让病理按在文本中出现的顺序排序
            d={}
            for r in records:
                d[r]=re.search(r,x).span()[0]
            records_sort = sorted(d.items(), key=lambda x: x[1])
            new_records = []
            for i in records_sort:
                new_records.append(i[0])
            df['病理'] = [new_records]


            records = []
            # 匹配所有浸润的字段
            for j in splits:
                if ('浸润性' in j) or('浸润型' in j ) or('浸润至型' in j) \
                        or('细胞浸润' in j)or('浸润组织' in j)or('浸润深度' in j)or('未见癌浸润' in j):
                    continue
                # if ('浸润至' in j) or('侵犯' in j):
                if '浸润' in j:
                    records.append(j)
                    chosen_indexs.append(splits.index(j))
            df['浸润'] = [records]

            records = []
            # 匹配所有转移比例的字段
            initial_splits=re.split(pattern='，|。|：|；|\s|:',string=x)
            # for j in initial_splits:
            for j in splits:
                pattern=re.compile('\d{1,2}\/\d{1,2}')
                if '浸润深度' in j:
                    continue
                if re.findall(pattern,j):
                    records+=re.findall(pattern,j)
                    chosen_indexs.append(splits.index(j))
            df['转移比例'] = [records]


            # 匹配 性状
            records=[]
            flag=False
            for j in splits:
                j2=j
                for c in charalist1:
                    if c in j:
                        flag=True
                        records.append(c)
                        chosen_indexs.append(splits.index(j))
                        j2=j.replace(c,'')
                for c in charalist2:
                    if c in j2:
                        flag=True
                        records.append(c)
                        chosen_indexs.append(splits.index(j))
            # 如果已知性状匹配不到
            if flag==False:
                for j in splits:
                    result=re.findall('（(.*型)）', j)
                    if result:
                        records += result
                        chosen_indexs.append(splits.index(j))
                    # if re.match('.{1,6}型',j):
                    #     records.append(re.match('.{1,6}型',j).group())
                    #     chosen_indexs.append(splits.index(j))
                    # else:
                    #     character = re.findall('（(.{1,6}型.*)）?', j)
                    #     # character = re.findall('（(.*型.*)）', j)
                    #     if character:
                    #         records+=character
                    #         chosen_indexs.append(splits.index(j))
            records=list(set(records))
            df['性状'] = [records]
            # pattern = re.compile('(、|（|\()(.*?)型')
            # if re.search(pattern, j):

            records=[]
            # 匹配病理等级
            pattern = re.compile('(Ⅰ|Ⅱ|Ⅲ|Ⅳ|II)([^\u4e00-\u9fa5]*?)级')
            for j in splits:
                pathological_grade = re.search(pattern, j)
                if pathological_grade:
                    chosen_indexs.append(splits.index(j))
                    result=pathological_grade.group()
                    result = result.replace('III', 'Ⅲ')
                    result=result.replace('II','Ⅱ')
                    records.append(result)
            for ii in range(len(records)):
                records[ii]=records[ii].replace(' ','')
            records=list(set(records))
            df['病理等级'] = [records]


            # 匹配肿瘤大小
            records = []
            # 匹配‘大小’或‘直径’
            for j in splits:
                if ('大小' in j) or ('直径' in j):
                    records.append(j)
                    chosen_indexs.append(splits.index(j))
                # 形如(1.4*1*0.5cm)
                pattern=re.compile('\((\d.*?cm)\)')
                result=pattern.findall(j)
                if result:
                    records+=result
                    chosen_indexs.append(splits.index(j))
                    pass

            df['肿瘤大小']=[records]

            # 匹配分化等级
            records = []
            #本可以直接匹配x，但为了记录chosen_indexs，for循环匹配splits
            for j in splits:
                for d in differentiations1:
                    if d in j:
                        records.append(d)
                        chosen_indexs.append(splits.index(j))
                        j=j.replace(d,'')
                for d in differentiations2:
                    if d in j:
                        records.append(d)
                        try:
                            chosen_indexs.append(splits.index(j))
                        except:
                            pass
            for d in differentiations3:
                for j in splits:
                    if d in j:
                        # 避免炎症G2S4
                        l=jieba.lcut(j)
                        if d in l:
                            records.append(d)
                            chosen_indexs.append(splits.index(j))
            df['分化等级']=[records]

            # 匹配 淋巴结是否转移
            records = []
            for j in splits:
                if ('淋巴结' in j) and ('见' in j):
                    records.append(j)
                    chosen_indexs.append(splits.index(j))
            df['淋巴结是否转移']=[records]

            records=[]
            # 匹配 肠旁淋巴结
            for j in splits:
                number = re.findall('肠旁淋巴结(.*\d)枚?', j)
                if number:
                    for n in range(len(number)):

                        if '枚' in number[n]:
                            index=number[n].index('枚')
                            number[n]=number[n][:index]
                        if '/' in number[n]:
                            number[n] = number[n].split('/')[1]

                        number[n] = "".join(filter(lambda ch: ch in '0123456789', number[n]))
                        number[n]=number[n].replace(' ','')
                    records+=number
                    chosen_indexs.append(splits.index(j))

            # for i in range(len(number)):
            #     if '/' in number[i]:
            #         number[i] = number[i].split('/')[1]
            records = list(filter(None, records))
            records=list(set(records))
            df['肠旁淋巴结个数'] = [records]

            # 匹配 神经侵犯
            records = []
            for j in splits:
                if '神经' in j:
                    records.append(j)
                    chosen_indexs.append(splits.index(j))
            df['神经侵犯']=[records]

            # 匹配 脉管侵犯
            records = []
            for j in splits:
                if '脉管' in j:
                    records.append(j)
                    chosen_indexs.append(splits.index(j))
            df['脉管侵犯']=[records]

            # 一般情况下的遍历
            for i in range(len(attributes)):
                # 检查分化属性的问题
                # if abbreviation_attributes[i]!='分化':
                #     continue

                # 不用考虑索引0
                if i==0:
                    continue

                #浸润、转移比例、性状、病理、肿瘤大小、分化等级、淋巴结是否转移、三个切端、神经侵犯、脉管侵犯需要单独考虑
                if (i==8)| (i==10) | (i==13) |(i==1)|(i==5)|(i==6)|(i==7)|(i==9)|(i==2)|(i==3)|(i==4)|(i==12)|(i==11):
                    continue
                # record = []
                # 对其他的字段进行匹配
                # 0字段也有可能
                # 把0字段再切之后，0不可以
                for j in splits:
                    # 记录所有匹配得上的文本

                    # 匹配到第一个就停止
                    if i==2 or i==3:
                        if (abbreviation_attributes[i] in j) or ('两' in j):
                            # record.append(j)
                            df[attributes[i]] = [j]
                            chosen_indexs.append(splits.index(j))
                            break
                    else:
                        if abbreviation_attributes[i] in j:
                            # record.append(j)
                            df[attributes[i]]=[j]
                            chosen_indexs.append(splits.index(j))
                            break


                # if record:
                #     if len(record)>1:
                #         df[attributes[i]] = [record]
                #     else:
                #         df[attributes[i]] = [record[0]]

            chosen_indexs=set(chosen_indexs) # 索引去重


            remaining_splits=[i for i in splits if splits.index(i) not in chosen_indexs]

            if remaining_splits:
                # if len(remaining_splits)>1:

                df['其他']=[remaining_splits]
                # else:
                #     df['其他']=[remaining_splits[0]]

        return df

    EMR_df=EMR_df.groupby('索引')
    split_df=EMR_df['文本内容'].apply(get_split)
    # split_df.to_csv('../EMR_result/split_df.csv',index=False,encoding='GB2312')
    split_df.to_csv(split_df_path,index=False,encoding='GB2312')
    return split_df

if __name__=='__main__':
    EMR_df_norm_path='EMR_df_norm.csv'
    split_df_path='split_df.csv'
    split_df=get_split_df(EMR_df_norm_path,split_df_path)