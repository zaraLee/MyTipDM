# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:43:30 2017

@author: zara
"""
import re
import pandas as pd
import os
import numpy as np
#获取作者
columns1 = ['target="_blank"','class="xi2"','space-uid','uid','title','dropmenu','class="xw1"','space','name'
           ,'user-id','username','user_name','class="xw1 xs4"','class="louzhuinfo2"','postauthor','class="authi"','author'
           ,'"u"','readName','user','uname','postauthor','rel="nofollow"']
def setWord_count(columns,htmlline):
    word_count = [0]*len(columns)
    for i in range(len(columns)):
        if columns[i] in htmlline:
            word_count[i] = 1
    return word_count


os.chdir(u'C:\\Users\\zara\\Desktop\\网络爬虫\\htmls')
filesname = os.listdir()
trainset_name = []
trainNum_name = []
for i in range(len(filesname)):
    charset = re.findall(r'(.*?)_',filesname[i])[0]
    file = open(filesname[i],encoding=charset)
    html = file.readlines()
    for i in range(len(html)):
        word_count = setWord_count(columns1,html[i])
        if sum(word_count) >=2:
            trainset_name.append(html[i])
            trainNum_name.append(word_count)
    file.close()

trainset2_name=[] 
for i in trainset_name:
    if len(i)<=150:
        trainset2_name.append(i) 
        
        
#训练作者模型
word_name = ['target="_blank"','class="xi2"','space-uid','dropmenu','class="xw1"','space','name'
           ,'user-id','username','user_name','class="xw1 xs4"','class="louzhuinfo2"','postauthor','class="authi"','author'
           ,'"u"','readName','uname','postauthor','rel="nofollow"','amp','action','class="bold"','strong',
           'class="tit_user"','info','UID','积分','论坛','作者','<dt>','gid','<li','span','主题','好友','usergroup',
           'Powered by Discuz','手机版','ilt_name','name_txt','class="author"','class="authorname"'
           'name="users"','userinfo','u.php?uid','javascript','class="user-','userNick']

def Word_set(word_name,trainSet):
    word_set = []
    for train in trainSet:
        word_count = [0]*len(word_name)
        for i in range(len(word_name)):
            if word_name[i] in train:
                word_count[i] = 1
        word_count.append(1.0)
        word_set.append(word_count)
    return word_set
    
def setLabel():
    labfile = open(u'E:\\C题程序\\label_name.txt')
    label = labfile.readlines()
    for i in range(len(label)):
        label[i] = int(label[i].replace('\n',''))
    return label

def sigmoid(X):
    return 1.0/(1+np.exp(-X))
    
def classify(X,weights):
    prob = sigmoid(sum(X*weights))
    if prob > 0.5 :
        return 1.0
    else:
        return 0.0
def gradAscent(word_set,label):
    w1 = []
    w2 = []
    w3 = []
    h1 = []
    wordMat = np.matrix(word_set)
    labelMat = np.matrix(label).transpose().astype(float)
    m,n = np.shape(wordMat)
    alpha = 0.001
    times = 1500
    weights = np.ones((n,1))
    for t in range(times):
        h = sigmoid(wordMat*weights)
        error = (labelMat-h)
        weights = weights+alpha*wordMat.transpose()*error
        w1.append(weights[0])
        w2.append(weights[1])
        w3.append(weights[2])
        h1.append(h[0])
    return weights,h,w1,w2,w3,h1
        
        
fr1 = open(u'C:\\Users\\zara\\Desktop\\网络爬虫\\add_train.txt','r',encoding='utf-8')
stradd_name = fr1.readlines()
for i in range(len(stradd_name)):
    stradd_name[i] = stradd_name[i].strip().replace('/n','')
stradd_name = stradd_name[:-1]
trainset3_name = trainset2_name+stradd_name
word_set = Word_set(word_name,trainset3_name)
label = setLabel()
label_add_name = list(np.loadtxt('C:\\Users\\zara\\Desktop\\网络爬虫\\add_label_name.txt'))
label = label+label_add_name
word_set = pd.DataFrame(word_set)
label = pd.DataFrame(label)
word_set[49]=label
a = list(word_set.values)
np.random.shuffle(a)
train = a[:int(0.7*len(a))]
test = a[int(0.7*len(a)):]
trainw=[]
trainl=[]
testw=[]
testl=[]
for i in train:
    trainw.append(i[:-1])
    trainl.append(i[-1])
for i in test:
    testw.append(i[:-1])
    testl.append(i[-1])
weight_name ,h,w1,w2,w3,h1= gradAscent(trainw,trainl)
testMat = np.matrix(testw)
result = []
for i in range(len(testl)):
    result.append(classify(testMat[i],weight_name))

tr = 0
falindex = []
for i in range(len(result)):
    if(result[i]==testl[i]):
        tr+=1
    else:
        falindex.append(i)

tr/len(result)
#np.savetxt('E:\\C题程序\\weight_name.txt',weight_name)
#weight_name = np.loadtxt('E:\\C题程序\\weight_name.txt')
#weight_name = np.matrix(weight_name).transpose()


