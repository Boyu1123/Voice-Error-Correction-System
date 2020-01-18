#coding=utf-8
import sys
from collections import Counter
import math
import jieba
from lby_Trie import codeutil
def _word_ngrams(tokens, stop_words=None,ngram_range=(1,1)):

        if stop_words is not None:
            tokens = [w for w in tokens if w not in stop_words]

        min_n, max_n = ngram_range
        if max_n != 1:
            original_tokens = tokens
            tokens = []
            n_original_tokens = len(original_tokens)
            for n in xrange(min_n,
                            min(max_n + 1, n_original_tokens + 1)):
                for i in xrange(n_original_tokens - n + 1):
                    tokens.append(" ".join(original_tokens[i: i + n]))

        return tokens

def readFile(file_name):
    arr = []
    for line in open(file_name):
        arr.append(line)
    return arr

# Bigrams
def buildBigrams(lines):
    frequenices = Counter()

    for line in lines:
        cut = jieba.cut(line)
        listcut = list(cut)
        prev = 'phi'
        for token in listcut:
            if token.split():
                frequenices[prev + ' ' + token.split()[0]] += 1
                prev = token
    return frequenices

# Unigrams
def buildUnigrams(lines):
    frequenices = Counter()
    for line in lines:
        cut = jieba.cut(line)
        listcut = list(cut)
        #n_gramWords = _word_ngrams(tokens = listcut,ngram_range=(2,2))
        #print listcut
        for token in listcut:
            #print token
            if token.split():
                frequenices[token.split()[0]] += 1

    return frequenices

def unigramFrequency(word, frequenices):
    #print word,frequenices[word]
    return frequenices[word] / float(sum(frequenices.values()))


def estimateUnigramSentence(sentence, frequencies):
    prob = 0.0
    cut = jieba.cut(sentence)
    listcut = list(cut)
    #n_gramWords = _word_ngrams(tokens = listcut,ngram_range=(2,2))
    for word in listcut:
        if prob == 0.0:
            prob = unigramFrequency(word, frequencies)
        else:
            prob *= unigramFrequency(word, frequencies)

    return math.log(prob, 2)

def estimateBigramSentence(sentence, unigrams, bigrams, phiCount, smooth):
    prob = 0.0
    prev = 'phi'
    cut = jieba.cut(sentence)
    listcut = list(cut)
    #n_gramWords = _word_ngrams(tokens = listcut,ngram_range=(2,2))
    for word  in listcut:
        if bigrams[prev + ' ' + word] == 0 and not smooth:
            return -1
        if prob == 0.0:
            prob = bigramFrequency(prev, word, unigrams, bigrams, phiCount, smooth)
        else:
            prob *= bigramFrequency(prev, word, unigrams, bigrams, phiCount, smooth)

        prev = word

    return math.log(prob, 2)

def bigramFrequency(B, A, unigrams, bigrams, phiCount, smooth):

    if smooth:
        return bigramFrequencySmoothed(B, A, unigrams, bigrams)

    # A = current
    # B = prev
    num = float(bigrams[B + ' ' + A])
    denom = unigrams[B]

    if B == 'phi':
        denom = phiCount

    return float(num) / float(denom)


def bigramFrequencySmoothed(B, A, unigrams, bigrams):

    bigram = B + ' ' + A
    if bigram not in bigrams:
        bigram_freq = 1
    else:
        bigram_freq = bigrams[bigram] + 1

    b_freq = 0
    for key in bigrams:
        if key.split()[0] == B:
            b_freq += bigrams[key]

    V = len(unigrams)

    return float(bigram_freq) / (b_freq + V + 1)

def train(training):
    unigrams = buildUnigrams(training)
    bigrams = buildBigrams(training)
    return unigrams, bigrams


def evaluate(unigrams, bigrams, sentence, phiCount):
    #print 'S = ' + sentence
    sentence = sentence.lower()

    unigramProb = estimateUnigramSentence(sentence, unigrams)
    bigramProb = estimateBigramSentence(sentence, unigrams, bigrams, phiCount, False)
    biggramSmoothedProb = estimateBigramSentence(sentence, unigrams, bigrams, phiCount, True)
    print sentence,unigramProb
    with open("ngram.txt","w") as d:
        d.write(str(unigramProb))
    with open("sentence.txt", "w") as f:
        f.write(str(sentence))
    return unigramProb
# Command line arguments
training_file = 'training.txt'
flag = '-test'
#testing_file = input('input\n')

#jieba.load_userdict('symptom.txt')
# # Read text from a text file
training = readFile(training_file)
input_sent = raw_input("search sentence:\n")
input_sent = codeutil(input_sent)
unigrams, bigrams = train(training)


evaluate(unigrams, bigrams, input_sent, len(training))
