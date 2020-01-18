#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import os
import sys
import json

jieba.load_userdict('symptom.txt')

class proofread:
    def __init__(self):
        if os.path.exists("dicmap.txt"):
            encodedjson=self.readfile()
            self.dicmap=json.loads(encodedjson)
        else:
            self.dicmap=self.initdicmap()
        for item in self.dicmap:
            #print "%s:%d"%(item,self.dicmap[item])
            #print item
            pass
        exit

    def proofreadAndSuggest(self,txt):
        ctarget=proofcheck(self.dicmap)
        errortoken = ctarget.getCorrectTokens(u"%s"%txt)
        return errortoken
    def initdicmap(self):
        root='dataset2/'
        list=os.listdir(root)
        tmplines=[]
        maplist={}
        for d in list:
            dir = os.listdir(root+d+"/")
            for f in dir:
                file=open(root+d+"/"+f)
                while 1:
                    lines = file.readlines(100000)
                    if not lines:
                        break
                    for line in lines:
                        tmplines.append(line)
        for line in tmplines:
            line=self.filter(line)
            ret=jieba.cut(line,cut_all=False)
            tmplitter=[]
            littercnt=0
            indexf=0
            for item in ret:
                tmplitter.append(self.filter(item))
                littercnt+=1
            for litter in tmplitter:
                if litter and type(litter) is not int:
                    if litter in maplist:
                        maplist[litter]+=1
                    else:
                        maplist[litter]=1
                    #if  indexf<littercnt-1:
                    #    if tmplitter[indexf+1] and type(tmplitter[indexf+1]) is not int:
                    #        tmpanotherlitter=litter+tmplitter[indexf+1]
                    #        if tmpanotherlitter in maplist:
                    #            maplist[tmpanotherlitter]+=1
                    #        else:
                    #            maplist[tmpanotherlitter]=1
                #indexf+=1
        encodedjson = json.dumps(maplist)
        self.writefile(encodedjson)
        return maplist

    def writefile(self,txt):
        file_object = open('dicmap.txt', 'w')
        file_object.write(txt)
        file_object.close()

    def readfile(self):
        file_object = open('dicmap.txt', 'r')
        txt=file_object.read( )
        file_object.close()
        return txt


    def filter(self,line):
        spechars=[",","，",":",'"',"'","﹔","ㄍ","#","\\","）","（","，","！",".","-","/","’","，","？","?","[","；","）",")","(","，","。","、","“","，","%","·","》","”","*",">","┆","：","．","％","】","《","]","_","〗","【","██","|","]","}","="]
        line=line.strip()
        for spechar in spechars:
            line=line.replace(spechar,"")
        line=line.strip()
        return line

class proofcheck:
    def __init__(self, maplist):
        self.maplist = maplist
        pass

    def proofreadAndSuggest(self, txt):
        sInputResult = list(txt)
        correctTokens, errorTokens = self.getCorrectTokens(sInputResult)
        if len(errorTokens) > 0:
            ret = jieba.cut(txt, cut_all=False)
            unitresult = []
            for unittoken in ret:
                #print unittoken
                if len(errorTokens) > 0:
                    for errortoken in errorTokens:
                        if errortoken in unittoken:
                            unitresult.append(unittoken.replace(errortoken, ""))
                            errorTokens.remove(errortoken)
                            break
                        else:
                            unitresult.append(unittoken)
                else:
                    unitresult.append(unittoken)

            ctokens = self.readfile()
            for linetoken in ctokens:
                existflag = 0
                matchflag = -1
                for unittoken in unitresult:
                    if unittoken in linetoken:
                        tmpposition = linetoken.find(unittoken)
                        if tmpposition > matchflag:
                            matchflag = tmpposition
                        else:
                            existflag = 1
                            break;
                    else:
                        existflag = 1
                        break;
                if existflag == 0:

                    print linetoken
        else:

            print txt
        errortoken = ''
        for i in errorTokens:
            errortoken += i
        #print errortoken.decode('utf-8')
        return errortoken

    def getCorrectTokens(self, sInputResult):
        correctTokens = []
        isCorrect = []
        errorTokens = []
        wronglist = []
        wordlist = []
        hasError = 0
        wrongcnt = 0
        tokencount = 0

        ret = jieba.cut(sInputResult, cut_all=False)
        for token in ret:
            wordlist.append(token)

        for i in range(len(wordlist)-1):
            if i==len(wordlist):
                break
            if len(wordlist[i]) == 1 and wordlist[i]!='。':
                wordlist = [wordlist[i]+wordlist[i+1] if j == wordlist[i] else j for j in wordlist]
                wordlist.remove(wordlist[i+1])
                    #print wordlist
        for token in wordlist:

            tokencount += 1
            probOne = self.probBetweenTowTokens(token)
            #print token,probOne

            if probOne <= 0:
                if len(token )!= 1:
                    isCorrect.append(0)
                    wronglist.append(token)
                    wrongcnt += 1
                elif len(token ) == 1 and token != "。":
                    # if tokencount==1:
                    #     isCorrect.append(0)
                    #     t = token + wordlist[tokencount]
                    if tokencount>1:
                        isCorrect.append(0)
                        t = wordlist[tokencount-2]+token
                        if "，" not  in t:
                            wronglist.append(t)
                            #print tokencount,wordlist[tokencount-2],token,wordlist
                            wrongcnt += 1
                    elif tokencount<len(wordlist)-1:
                        isCorrect.append(0)
                        #print tokencount, wordlist[tokencount], token, wordlist
                        t = token+wordlist[tokencount]
                        if "，" not  in t and "。" not in t:
                            wronglist.append(t)
                            wrongcnt += 1
            else:
                isCorrect.append(1)
        #print wordlist,  wronglist,isCorrect
        for i in range(len(isCorrect)-1):

            if isCorrect[i]==0 and isCorrect[i+1]==0:
                #print wordlist[i],wordlist[i+1],wronglist
                wronglist.append(wordlist[i]+wordlist[i+1])
                isCorrect.append(0)
                if wordlist[i] in wronglist:
                    wronglist.remove(wordlist[i])
                    isCorrect.remove(isCorrect[i])
                    i = i-1
                if wordlist[i+1] in wronglist:
                    wronglist.remove(wordlist[i+1])
                    isCorrect.remove(isCorrect[i + 1])

        for i in range(len(isCorrect) - 1):

            if isCorrect[i] == 0 and isCorrect[i + 1] == 0:
                # print wordlist[i],wordlist[i+1],wronglist
                wronglist.append(wordlist[i] + wordlist[i + 1])
                isCorrect.append(0)
                if wordlist[i] in wronglist:
                    wronglist.remove(wordlist[i])
                    isCorrect.remove(isCorrect[i])
                    i = i - 1
                if wordlist[i + 1] in wronglist:
                    wronglist.remove(wordlist[i + 1])
                    isCorrect.remove(isCorrect[i + 1])
                # for j in wronglist:
                #     if "。" in j :
                #         wronglist.remove(j)
                #     if j == wordlist[i]:
                #         wronglist.remove(j)
                        # if wordlist[i+1]:
                        #     wronglist.remove(wordlist[i+1])

        for i in wronglist:
            if i[0] == "。" :
                wronglist.remove(i)

        wronglist = list(set(wronglist))
        #tokencount = len
        print wordlist, isCorrect, wronglist,tokencount
        if 0 not in isCorrect:
            return sInputResult
        # if tokencount>2:
        if tokencount > 0:
            if wrongcnt == 0:
                counti = 0
                while counti < tokencount - 1:
                    tokenbuf = sInputResult[counti]
                    countj = counti + 1
                    while countj < tokencount:
                        probOne = self.probBetweenTowTokens("%s%s" % (tokenbuf, sInputResult[countj]))
                        if probOne > 0:
                            tokenbuf = "%s%s" % (tokenbuf, sInputResult[countj])
                            #print "two:"+tokenbuf
                            if countj < tokencount -1  and self.probBetweenTowTokens("%s%s" % (tokenbuf, sInputResult[countj + 1])) > 0:
                                tokenbuf = "%s%s" % (tokenbuf, sInputResult[countj + 1])
                                #print "three:" + tokenbuf
                                if countj < tokencount -2  and self.probBetweenTowTokens("%s%s" % (tokenbuf, sInputResult[countj + 2])) > 0:
                                    tokenbuf = "%s%s" % (tokenbuf, sInputResult[countj + 2])
                        else:
                            if countj < tokencount - 1 and self.probBetweenTowTokens(
                                            "%s%s%s" % (tokenbuf, sInputResult[countj], sInputResult[countj + 1])) > 0:
                                tokenbuf = "%s%s" % (sInputResult[countj], sInputResult[countj + 1])

                            else:
                                if countj < tokencount - 2 and self.probBetweenTowTokens(
                                            "%s%s%s%s" % (tokenbuf, sInputResult[countj],sInputResult[countj + 1], sInputResult[countj + 2])) > 0:
                                    tokenbuf = "%s%s%s%s" % (tokenbuf, sInputResult[countj], sInputResult[countj + 1],sInputResult[countj + 2])
                                else:
                                    hasError = 1
                                    break
                        countj += 1
                    counti += 1
                    correctTokens.append(tokenbuf)
                if self.probBetweenTowTokens(sInputResult[tokencount - 1]) > 0:
                    correctTokens.append(sInputResult[tokencount - 1])
            else:

                counti = 0
                while counti < tokencount-1:
                    a = isCorrect[counti]
                    tokenbuf = ''
                    if a > 0:
                        tokenbuf = sInputResult[counti]
                        countj = counti + 1
                        while countj < tokencount:
                            probOne = self.probBetweenTowTokens("%s%s" % (tokenbuf, sInputResult[countj]))
                            if probOne > 0:
                                tokenbuf = sInputResult[countj]
                            else:
                                hasError = 2
                                break
                            countj += 1
                        correctTokens.append(tokenbuf)
                    elif self.probBetweenTowTokens("%s%s" % (sInputResult[counti], sInputResult[counti + 1])) > 0:
                        tokenbuf = "%s%s" % (sInputResult[counti], sInputResult[counti + 1])
                        countj = counti + 2
                        while countj < tokencount:
                            probOne = self.probBetweenTowTokens("%s%s" % (tokenbuf, sInputResult[countj]))
                            if probOne > 0:
                                tokenbuf = "%s%s" % (tokenbuf, sInputResult[countj])
                            else:
                                hasError = 3
                                break
                            countj += 1
                        correctTokens.append(tokenbuf)
                    else:
                        hasError = 4
                    counti += 1
        #for i in wronglist:
        #     print "i:"+i
        #     tokencount = len(i)
        #     sInputResult = i
        # # 计算错误的是哪个地方
        #     if tokencount > 2:
        #         counti = 0;
        #
        #         while counti < tokencount:
        #             if counti > 0 and counti < tokencount - 1 and sInputResult[counti+1]!="。":
        #                 probOnea = self.probBetweenTowTokens("%s%s" % (sInputResult[counti], sInputResult[counti + 1]))
        #                 probOneb = self.probBetweenTowTokens("%s%s" % (sInputResult[counti - 1], sInputResult[counti]))
        #                 print "%s%s" % (sInputResult[counti], sInputResult[counti + 1])
        #                 print "%s%s" % (sInputResult[counti - 1], sInputResult[counti])
        #                 if probOnea == 0 and probOneb == 0:
        #                     print sInputResult[counti]
        #                     errorTokens.append(sInputResult[counti])
        #             counti += 1
        #     elif tokencount == 2:
        #         probOne = self.probBetweenTowTokens("%s%s" % (sInputResult[0], sInputResult[1]))
        #         print "%s%s" % (sInputResult[0], sInputResult[1]),probOne
        #         if probOne == 0:
        #             errorTokens.append(sInputResult)
        #errortoken = ''
        # for errortoken in wronglist:
        #     if errortoken!='\n' and errortoken!='。' and errortoken != '':
        #         print sInputResult+' wrong:'+errortoken.decode('utf-8')
        for i in wronglist:
            for j in wronglist:
                if i!=j and i in j:
                    wronglist.remove(i)
        return  wronglist

    def readfile(self):
        tmplines = []
        file = open('dicmap.txt', 'r')
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                tmplines.append(line)
        return tmplines

    def probBetweenTowTokens(self, token):
        tmpcount = 0
        if token in self.maplist:
            # print token
            tmpcount = self.maplist[token]
        if len(token) == 1:
            tmpcount = 0
        return tmpcount

def filter(line):
    spechars=[",",":",'"',"'","﹔","ㄍ","#","\\","）","（","，","！",".","-","/","’","，","？","?","[","；","）",")","(","，","、","“","，","%","·","》","”","*",">","┆","：","．","％","】","《","]","_","〗","【","██","|","]","}","="]
    line=line.strip()
    for spechar in spechars:
        line=line.replace(spechar," ")
    line=line.split()
    if len(line) >= 1:
        for i in range(len(line)-1):
            line[i] += "。"
    return line
def main():
    ptarget=proofread()
    # with open("sentence.txt","r") as d:
    #     sentence = d.read()
    # for sen in filter(sentence):
    sen = "患者言语轻微，胎未不正。"
    ptarget.proofreadAndSuggest(sen)

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

