#!/usr/bin/env python
# coding=utf-8
from numpy import zeros

"""
create word list dataset
"""
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
"""
translate the input to vector
"""
def setWord2Vec(vocabList,input):
    returnVec = [0]*len(vocabList)
    for word in input:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word:%s is not in my vocabulary"%word
    return returnVec
"""
taining the bayesian
"""
def train(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = zeros(numWords);p1Num = zeros(numWords)
    p0Denom = 0.0;p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix)
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom
    return p0Vect,p1Vect,pAbusive
"""
the classify function
"""
from numpy import log
def classify(vec2Class,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Class*p1Vec) + log(pClass1)
    p0 = sum(vec2Class*p0Vec) + log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
