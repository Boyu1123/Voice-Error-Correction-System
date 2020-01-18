#coding=utf-8
from jieba import posseg as pseg
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import jieba


with open("symptom.txt",'r') as d:
    data = d.readlines()
    with open('dicmap1.txt','w') as f:
        for i in data:
            #print i
            f.write('"'+ i.split()[0].decode('utf-8').encode('unicode_escape')+'": ' + '1' + ', ')










