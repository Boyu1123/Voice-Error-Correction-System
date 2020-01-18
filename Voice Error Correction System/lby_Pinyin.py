# coding=UTF-8
from xpinyin import Pinyin
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


p = Pinyin()

#把语料库转为拼音
sym_word_dic = []
sym_uword_dic = []
sym_pinyin_dic = []
sym_initial_dic = []

drug_word_dic = []
drug_uword_dic = []
drug_pinyin_dic = []
drug_initial_dic = []

sym_word_list =  open('symptom.txt','r')
for i in sym_word_list.readlines():
    if i.split():
        sym_word_dic.append(i.split()[0])
        sym_chineselist = i.split(' ')
        for j in sym_chineselist:
            sym_uword_dic = unicode(j,"utf-8")
            sym_pinyin_dic.append(p.get_pinyin(sym_uword_dic,''))
            sym_initial_dic.append(p.get_initials(sym_uword_dic,''))

drug_word_list =  open('drug.txt','r')
for i in drug_word_list.readlines():
    if i.split():
        drug_word_dic.append(i.split()[0])
        drug_chineselist = i.split(' ')
        for j in drug_chineselist:
            drug_uword_dic = unicode(j,"utf-8")
            drug_pinyin_dic.append(p.get_pinyin(drug_uword_dic,''))
            drug_initial_dic.append(p.get_initials(drug_uword_dic,''))

with open('sym_pinyin.txt','w') as f:
    for pinyin_i,word_i in zip(sym_pinyin_dic,sym_word_dic):
        f.write(word_i+':'+pinyin_i)

with open('sym_initial.txt','w') as f:
    for i,word in zip(sym_initial_dic,sym_word_dic):
        f.write(word+':'+i)

with open('drug_pinyin.txt','w') as f:
    for pinyin_i,word_i in zip(drug_pinyin_dic,drug_word_dic):
        f.write(word_i+':'+pinyin_i)

with open('drug_initial.txt','w') as f:
    for i,word in zip(drug_initial_dic,drug_word_dic):
        f.write(word+':'+i)
