#coding=utf-8
from jieba import posseg as pseg
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import jieba

jieba.load_userdict('symptom.txt')
total = []
wordtype = []
with open('segwords.txt','w') as f:
    with open('training.txt','r') as k:
        for i in k:
            #print i
            i = i.replace('"','')
            i = i.replace("'", '')
            seg = pseg.cut(i.strip())

            for word, flag in seg:
                total.append(word)
                wordtype.append(flag)
                #f.write('\n'.join(seg))
                f.write(word + flag + "\n")

c = Counter(total)
with open('dicmap.txt','w') as f:
    for i in c.most_common():
        f.write('"'+ i[0].decode('utf-8').encode('unicode_escape')+'": ' + str(i[1]) + ', ')








