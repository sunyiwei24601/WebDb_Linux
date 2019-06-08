import pickle
import codecs

# 不用修改 train的时候会自动生成
def modify_map_file():
    with open('maps.pkl', "rb") as f:
        pkllf=pickle.load(f)
        # pkllf[2]={'O':0,'I-INF':1,'B-INF':2,'E-INF':3}
        # pkllf[3] = {0: 'O', 1:'I-INF' ,2:'B-INF', 3:'E-INF'}
        # char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
        with open('maps.pkl', "wb") as f:
            pickle.dump(pkllf, f)

def check_Data():
    path='data/INF.Data'
    num=0
    for line in codecs.open(path, 'r', 'utf8'):
        if line=='\r\n':
            continue
        num+=1
        words=line.split()
        line=line.replace(' ','')
        if len(words)>2:
            print(num,line)
        if words[-1] not in ['O','I-INF','B-INF']:
            print(num,line)

modify_map_file()
