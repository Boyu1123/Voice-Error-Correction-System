# coding=utf-8

from xpinyin import Pinyin
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class arithmetic():
    def __init__(self):
        pass

    ''' 【编辑距离算法】 【levenshtein distance】 【字符串相似度算法】 '''

    def levenshtein(self, first, second):
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [range(second_length) for x in range(first_length)]

        for i in range(1, first_length):
            for j in range(1, second_length):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)

        return distance_matrix[first_length - 1][second_length - 1]

def codeutil(strs):
    return strs.decode('utf8', 'ignore').encode('GBK', 'ignore').decode('GBK', 'ignore')


#if __name__ == "__main__":
def lev():
    arith = arithmetic()
    pinyindisdic = {}
    initialdisdic = {}
    disdic = {}
    sym_pinyin_dic = {}
    sym_initial_dic = {}
    drug_pinyin_dic = {}
    drug_initial_dic = {}

    with open("sym_pinyin.txt","r")as f:
        data = f.readlines()
        for i in data:

            sym_pinyin_dic[i.split(':')[1].split()[0]]= i.split(':')[0]
    with open("sym_initial.txt","r")as f:
        data = f.readlines()
        for i in data:

            sym_initial_dic[i.split(':')[1].split()[0]]= i.split(':')[0]
    with open("drug_pinyin.txt", "r")as f:
        data = f.readlines()
        for i in data:

            drug_pinyin_dic[i.split(':')[1].split()[0]] = i.split(':')[0]
    with open("drug_initial.txt", "r")as f:
        data = f.readlines()
        for i in data:

            drug_initial_dic[i.split(':')[1].split()[0]] = i.split(':')[0]

    with open("trie.txt","r")as f:
        data = f.readlines()
        data = [codeutil(i.split()[0]) for i in data]
        p = Pinyin()
        input_word = data[0]
        pinyin = p.get_pinyin(input_word, '')
        initial = p.get_initials(input_word, '')
        #print input_word,pinyin,initial
        for i in data[1:]:
            disdic[i] = arith.levenshtein(data[0], i)
            f = zip(disdic.values(), disdic.keys())
            f = sorted(f)
            minf = f[0][0]
        #print sym_pinyin_dic.keys()[:5]
        for i in f:

            if pinyin in sym_pinyin_dic and i[0] == minf:
                #print pinyin
                if pinyin in drug_pinyin_dic and i[0] == minf:
                    #print drug_pinyin_dic[pinyin], pinyin, i[0]
                    pass
                #print sym_pinyin_dic[pinyin],pinyin,i[0]
                return sym_pinyin_dic[pinyin]
            elif initial in sym_initial_dic and i[0] == minf:
                if initial in drug_initial_dic and i[0] == minf:
                    #print drug_initial_dic[initial], initial, i[0]
                    pass
                print sym_initial_dic[initial],initial,i[0]
                return sym_initial_dic[initial]
            else:
                #print i[0],i[1]
                return i[1]
        #for i in data[1:]:
            #disdic[i] = arith.levenshtein(data[0], i)
        #f = zip(disdic.values(), disdic.keys())
        #f = sorted(f)
        #minf = f[0][0]

        #for i in f:
         #   if i[0] == minf:
          #      print i[0], i[1]







