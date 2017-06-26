# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:51:12 2017

@author: zara
"""
from urllib.request import Request
from urllib.request import urlopen
import lxml
from lxml import html
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import numpy as np
import chardet

columns2 = ['post_width','t_f','postmessage-top','t_msgfont lazyimg','postmessage','t_msgfont','font-family','post_content','text_'
,'quote-content','class="case"','tbody','class="content"','id="msgMainContent"','align=','class="cont"','bbs-cont'
,'read_tpc','post_msg','message','article','class="article scrollFlag"','conttxt','class="text"','ilt_p','thread_content','replycontent'
,'topiccontent','mainNoteInfo','article_main','f14 mb10','content-txt','main_topic','class="t_f"','content','txtmain','tpc_content"','article_content'
,'t_msgfont','con f_14','info','Amain_main','cellspacing="0"','cellpadding="0"','content_id','xname="content','id="thread"','align="center"']
def setWord_count(columns,htmlline):
    word_count = [0]*len(columns)
    for i in range(len(columns)):
        if columns[i] in htmlline:
            word_count[i] = 1
    return word_count
trainset_content = []
content = []
os.chdir(u'C:\\Users\\zara\\Desktop\\网络爬虫\\htmls_content2')
filesname = os.listdir()
for i in range(len(filesname)):
    print(i)
    try:
        f2 = open('C:\\Users\\zara\\Desktop\\网络爬虫\\htmls_content2\\%s'%filesname[i],'r')
        html2 = f2.readlines()
    except:
        pass
    z = ''
    for h in html2:
        z = z+h+'\n'
    html = BeautifulSoup(z,'lxml').prettify()
    soup = BeautifulSoup(html,'lxml')
    for j in range(len(html2)):
        word_count = setWord_count(columns2,html2[j])
        if sum(word_count) >=2:
            p1 = re.compile(r'<(\w+) ')
            p2 = re.compile(r'class="(.*?)"')
            p3 = re.compile(r'id="(.*?)"')
            Tag = p1.findall(html2[j])
            Class = p2.findall(html2[j])
            Id = p3.findall(html2[j])
            if((Class!=[])&(Id!=[])):
                data = soup.find_all(Tag,attrs={'class':Class,'id':Id})
                if(data != []):
                    for d in data:
                        content.append(d.get_text())
                        trainset_content.append(str(d))
            elif (Class!=[]):
                data = soup.find_all(Tag,attrs={'class':Class})
                if(data != []):
                    for d in data:
                        content.append(d.get_text())
                        trainset_content.append(str(d))
            else:
                data = soup.find_all(Tag,attrs={'id':Id})
                if(data != []):
                    for d in data:
                        content.append(d.get_text())
                        trainset_content.append(str(d))
trainset2_content = []
content_txt = []
trainset_pd = pd.DataFrame(trainset_content)
content_pd = pd.DataFrame(content)
content_pd = content_pd.drop_duplicates()
trainset_pd = trainset_pd.ix[content_pd.index]
for i in trainset_pd.values:
    trainset2_content.append(i[0])
for i in content_pd.values:
    content_txt.append(i[0])
    
#正文分类器
word_content = ['post_width','t_f','postmessage-top','t_msgfont lazyimg','postmessage','t_msgfont','font-family','post_content','text_'
,'quote-content','class="case"','tbody','class="content"','id="msgMainContent"','align=','class="cont"','bbs-cont'
,'read_tpc','post_msg','message','article','class="article scrollFlag"','conttxt','class="text"','ilt_p','thread_content','replycontent'
,'topiccontent','mainNoteInfo','article_main','f14 mb10','content-txt','main_topic','class="t_f"','content','txtmain','tpc_content"'
,'article_content','t_msgfont','con f_14','info','Amain_main','cellspacing="0"','cellpadding="0"','content_id','xname="content','id="thread"']
def Word_set(word_content,trainSet):
    word_set = []
    for train in trainSet:
        word_count = [0]*len(word_content)
        for i in range(len(word_content)):
            if word_content[i] in train:
                word_count[i] = 1
        word_count.append(1.0)
        word_set.append(word_count)
    return word_set
    
def setLabel():
    labfile = open(u'E:\\C题程序\\label_content.txt')
    label = labfile.readlines()
    for i in range(len(label)):
        label[i] = float(label[i].replace('\n',''))
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
    #weightchange = []
    #errorchange = []
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
        #weightchange.append(weightchange)
        #errorchange.append(sum(error))
    return weights,h#weightchange,#errorchange
        
        
    

word_set = Word_set(word_content,trainset2_content)
label = setLabel()
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
weight_content,h = gradAscent(trainw,trainl)
#errorchange = gradAscent(trainw,trainl)[2]

testMat = np.matrix(testw)
result = []
for i in range(len(testl)):
    result.append(classify(testMat[i],weight_content))

tr = 0
falindex = []
for i in range(len(result)):
    if(result[i]==testl[i]):
        tr+=1
    else:
        falindex.append(i)

tr/len(result)

#np.loadtxt('E:\\C题程序\\weight_content.txt')
#weight_content = np.matrix(weight_content).transpose()