import re
import pandas as pd


def get_EMR_df_norm(initial_EMR_path,read_encoding='gb2312',EMR_df_norm_path='EMR_df_norm.csv'):

    EMR_df=pd.read_csv(initial_EMR_path,header=None,encoding=read_encoding)
    EMR_df.columns=['文本内容']

    # 去除字符串开头非中文、非引号
    # eg. S12-10787（1-23）HEx23.“左侧乳腺改良根治标本”，所以括号留着不行
    # def remove_Abnormal_symbols(x):
    #     while True:
    #         if not re.match('[\u4e00-\u9fa5]|“',x[0]):
    #             x=x[1:]
    #             continue
    #         else:
    #             break
    #     return x
    #
    # EMR_df['文本内容']=EMR_df['文本内容'].apply(remove_Abnormal_symbols)

    # 会把转移比例的值删了
    #删除\d(、|，)
    #eg. 1、   2，
    # def romove2(x):
    #     pattern=re.compile('\d[、，]')
    #     # 没有匹配到不会报错
    #     x=re.sub(pattern,'',x)
    #     return x
    # EMR_df['文本内容']=EMR_df['文本内容'].apply(romove2)

    # 去除字符串开头或者结尾的空格
    # 把 切断 替换为 切端
    # 删除乱码？
    # 把 未及 替换为 未见
    def get_strip(x):
        x=x.replace('？','')
        x=x.replace('切断','切端')
        x = x.replace('未及', '未见')
        x = x.replace('增值型', '增殖型')
        x = x.replace('浸润至型', '浸润型')
        x = x.replace('III', 'Ⅲ')
        x = x.replace('II', 'Ⅱ')
        x = x.replace('，活检', '活检')
        x = x.replace('Dauglas', '道格拉斯')
        x = x.replace('Douglas', '道格拉斯')
        return x.strip()
    EMR_df['文本内容']=EMR_df['文本内容'].apply(get_strip)

    # 存在左右引号使用不规范，把左右引号都换为右引号
    def replace_quotation_mark(x):
        str=re.sub('“','”',x)
        return str
    EMR_df['文本内容']=EMR_df['文本内容'].apply(replace_quotation_mark)

    #删除描述病理等级时额外的空格\s，防止被切开
    #eg. 小肠腺癌II- III级
    def romove3(x):
        result=re.search('-\s',x)
        if result:
            index=result.regs[0][0]+1
            x=x[:index]+x[index+1:]
        return x
    EMR_df['文本内容']=EMR_df['文本内容'].apply(romove3)

    #删除描述肿瘤大小时额外的空格\s，防止被切开
    #eg. 3.0cm×2.5 cm×2.0 cm
    def romove4(x):
        x=re.sub('\sc', 'c', x)
        return x
    EMR_df['文本内容']=EMR_df['文本内容'].apply(romove4)


    #删除‘左’‘右’两边的引号
    #eg. “左”输卵管、“右”输卵管、“右”卵巢、“右”宫旁均未见癌累及
    def romove5(x):
        x=re.sub('”左”', '左', x)
        x = re.sub('”右”', '右', x)
        return x
    EMR_df['文本内容']=EMR_df['文本内容'].apply(romove5)

    #对结构化样本增加空格，方便分割
    #eg. 标本类型:胰体尾+脾脏切除标本组织学类型:多发性神经内分泌瘤（大于10灶）组织学分级:G2肿瘤大小:最大径0.05-5.5cm肿瘤扩散:肿瘤局限于胰腺内神经侵犯:未见脉管内癌栓:未见其他切缘:胰体切缘情况参见冰冻报告F2017-11180胰周淋巴结转移情况:胰周未查见淋巴结其他病理发现:脾脏未见肿瘤肠壁组织未见肿瘤其他:免疫组化提取了显示不全 所以没点提取
    def add1(x):
        if '标本类型:' in x:
            properties=['标本类型:','肿瘤部位:','组织学类型:','组织学分级:',
                        '肿瘤大小:','肿瘤扩散:','神经侵犯:','脉管内癌栓:','近端胰腺切缘:',
                        '远端胰腺切缘:','其他切缘:','胰腺颈部切缘:','钩突切缘:','门静脉切缘:',
                        '腔静脉切缘:','胆总管切缘:','近端切缘（胃或十二指肠）:','远端切缘（远端十二指肠或空肠）:',
                        '其他切缘（适用时）:','治疗效果:','胰周淋巴结转移情况:','特殊检查:','其他病理发现:',
                        '肿瘤距最近切缘的距离：','胆总管切缘:','胃切缘:','十二指肠切缘:','其他淋巴结转移情况:','肿瘤细胞:',
                        '胆囊:','炎十二指肠:','其余胰腺情况:']
            for p in properties:
                if p in x:
                    x=re.sub(p,'    '+p,x)
        return x
    EMR_df['文本内容']=EMR_df['文本内容'].apply(add1)


    # EMR_df.to_csv('../EMR_result/EMR_df_norm.csv',index=False,header=False)
    # EMR_df.to_csv('../EMR_result/EMR_df_norm.csv', encoding='gb2312')
    EMR_df.to_csv(EMR_df_norm_path, encoding='gb2312')
    return EMR_df

if __name__=='__main__':
    initial_EMR_path = r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'
    read_encoding='gb2312'
    EMR_df_norm=get_EMR_df_norm(initial_EMR_path,read_encoding=read_encoding)
    # EMR_df_norm.to_csv('../EMR_result/EMR_df_norm.csv', encoding='gb2312')