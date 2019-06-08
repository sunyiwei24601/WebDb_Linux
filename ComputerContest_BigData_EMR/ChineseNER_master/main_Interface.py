import os
import sys
current_path=os.path.dirname(os.path.abspath(__file__))
# print(current_path)


from main import *


# print(current_path)
last_path='\\'.join(current_path.split('\\')[:-1])

def get_infiltration_model():

    value_df_path=last_path+'/value_df.csv'

    import pandas as pd
    value_df = pd.read_csv(value_df_path, encoding='gb2312')

    value_df=my_evaluate_line(value_df)
    value_df.to_csv(value_df_path,encoding='GB2312',index=False)
if __name__ == '__main__':
    get_infiltration_model()