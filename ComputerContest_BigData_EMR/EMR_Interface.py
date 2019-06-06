from preprocess import get_EMR_df_norm
from get_split import get_split_df
from get_value import get_value_df

if __name__=='__main__':
    initial_EMR_path=r'D:\SUFE\ComputerContest_BigData\Data\EMR\1000records.csv'

    # 官方所给病历文件的编码
    read_encoding='gb2312'

    # 输出结构化文本文件的编码
    to_encoding='gb2312'

    # 数据清洗与预处理
    get_EMR_df_norm(initial_EMR_path, read_encoding)

    # 截取属性对应分句
    get_split_df()

    # 获取值
    value_df = get_value_df(to_encoding)
    pass