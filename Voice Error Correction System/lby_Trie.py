# coding=utf-8
from collections import defaultdict
import sys
from ChineseCut import *
from lby_Levenshtein import lev
from lby_Ngram import *
reload(sys)
sys.setdefaultencoding('utf8')


class LBTrie:
    def __init__(self):
        self.trie = {}
        self.size = 0

        # 添加单词
    def add(self, word):
        p = self.trie
        dicnum = 0
        word = word.strip()
        for c in word:
            if not c in p:
                p[c] = {}
            dicnum += 1
            p = p[c]
        if word != '':
            # 在单词末尾处添加键值''作为标记，即只要某个字符的字典中含有''键即为单词结尾
            p[''] = ''
        if dicnum == len(word):
            return True

    # 查询单词
    def search(self, word):
        p = self.trie
        word = word.lstrip()
        for c in word:
            if not c in p:
                return False
            p = p[c]
            # 判断单词结束标记''
        if '' in p:
            return True
        return False


def codeutil(strs):
    return strs.decode('utf8', 'ignore').encode('GBK', 'ignore').decode('GBK', 'ignore')

def cut(strs):
    results = []
    strs = codeutil(strs)
    for x in range(len(strs)):
        for i in range(len(strs) - x):
            results.append(strs[i:i + x + 1])
    return results



if __name__ == '__main__':
    sym_namelist = []
    drug_namelist = []
    symtrie_obj = LBTrie()
    drugtrie_obj = LBTrie()

    # 添加单词
    symptom_corpus = open('symptom.txt', 'r')
    drug_corpus = open('drug.txt','r')
    max = 0

    sym_countdic = defaultdict(int)
    for record in symptom_corpus.readlines():
        sym_namelist.append(record)
        sym_recordlist = record.split(' ')
        for word in sym_recordlist:
            sym_check = symtrie_obj.add(codeutil(word))
            if sym_check:
                sym_countdic[word] += 1
    sym_resortedcountdic = sorted(sym_countdic.items(), key=lambda item: item[1], reverse=True)

    drug_countdic = defaultdict(int)
    for record in drug_corpus.readlines():
        drug_namelist.append(record)
        drug_recordlist = record.split(' ')
        for word in drug_recordlist:
            drug_check = drugtrie_obj.add(codeutil(word))
            if drug_check:
                drug_countdic[word] += 1
    drug_resortedcountdic = sorted(drug_countdic.items(), key=lambda item: item[1], reverse=True)
    ptarget = proofread()
    with open("sentence.txt", "r") as d:
        sentence = d.read()
    #answer = ""
    for sen in filter(sentence):
        #sen = sen.split()[0] + "。"
        #print sen
        input_words = ptarget.proofreadAndSuggest(sen)

        if isinstance(input_words,basestring):
            #answer += input_words
            continue
        for input_word in input_words:
            input_word = codeutil(input_word).replace("。",'')
            print input_word
            # if input_word == '':
            #     #print "正确"
            #     continue
            # # 查找单词
            # #input_word = raw_input("search word:\n")
            if symtrie_obj.search(codeutil(input_word)):
                print 'symfind:'+input_word
                continue
            elif drugtrie_obj.search(codeutil(input_word)):
                print 'drugfind:'+input_word
                continue
            else:
                results = cut(input_word)
                trie = []
                for i in results:
                    #print  i
                    flag = 0
                    result = codeutil(i)
                    for j in range(len(i)):

                        if flag:
                            break
                        for record in sym_namelist:
                            if j == 0:
                                r = result
                            else:r = result[:-j]
                            #print r
                            if r in record:

                                #print record
                                trie.append(record)
                                flag = 1
                        for record in drug_namelist:
                            if r in record:
                                #print record
                                trie.append(record)
                                flag = 1

                with open("trie.txt","w") as f:
                    f.write(input_word.split()[0]+"\n")
                    for i in trie:
                        if i:
                            f.write(i)

            #answer += lev()
            wrongword = lev()
            #print input_word,wrongword
            sentence = sentence.replace(input_word,wrongword)
    data2 = evaluate(unigrams, bigrams, sentence, len(training))
    with open("ngram.txt",'r') as d:
        data1 = float(d.read())
    print sentence