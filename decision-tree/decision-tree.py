#!/usr/bin/env python
# coding=utf-8
"""
compute the H(D),the entropy of dataSet
"""
from math import log

def cal_entropy(dataSet):
    Entrynum = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentlabel = featVec[-1]
        if currentlabel not in labelCount.keys():
            labelCount[currentlabel] = 0
        labelCount[currentlabel] += 1
    entropy = 0.0
    for key in labelCount:
        prob = float(labelCount[key])/Entrynum
        entropy -= prob*log(prob,2)
    return entropy

"""
divide the dataSet by the feature that given
result dataSet don't include the feature
"""
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featureVec in dataSet:
        if featureVec[axis] == value:
            reducedFeatVec = featureVec[:axis]
            reducedFeatVec.extend(featureVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

"""
choose the best feature to split dataSet
"""
def chooseBestFeatue(dataSet):
    numFeature = len(dataSet[0])-1
    baseEntropy = cal_entropy(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeature):
        featValueList = [example[i] for example in dataSet]
        uniqueVal = set(featValueList)
        newEntropy = 0.0
        for value in uniqueVal:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*cal_entropy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
"""
if the program has processed all the featurs but
thers is yet different labels in the leaf
then wo vote to decide which label to choose
"""
import operator
def vote2chooseLabel(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),\
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return vote2chooseLabel(classList)
    bestFeature = chooseBestFeatue(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel:{}}
    del(labels[bestFeature])
    featValues = [example[bestFeature] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(splitDataSet\
                                                     (dataSet,bestFeature,value),subLabels)
    return myTree
