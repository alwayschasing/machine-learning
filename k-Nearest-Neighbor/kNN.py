#!/usr/bin/env python
# coding=utf-8
"""
dataSet-训练样本集
inX-输入向量
labels-标签向量
k-选择最近邻的数目
"""
from numpy import tile
import operator

def classfiy(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    #tile(A，array_like):numpy中的函数，建立A的类数组类型数据结构
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #argsort()：numpy中的函数，return the indices that would sort an array
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
        key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


