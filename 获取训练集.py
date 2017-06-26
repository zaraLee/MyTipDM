# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:35:48 2017

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

columns1 = ['target="_blank"','class="xi2"','space-uid','uid','title','dropmenu','class="xw1"','space','name'
           ,'user-id','username','user_name','class="xw1 xs4"','class="louzhuinfo2"','postauthor','class="authi"','author'
           ,'"u"','readName','user','uname','postauthor','rel="nofollow"']
columns2 = ['post_width','t_f','postmessage-top','t_msgfont lazyimg','postmessage','t_msgfont','font-family','post_content','text_'
,'quote-content','class="case"','tbody','class="content"','id="msgMainContent"','align=','class="cont"','bbs-cont'
,'read_tpc','post_msg','message','article','class="article scrollFlag"','conttxt','class="text"','ilt_p','thread_content','replycontent'
,'topiccontent','mainNoteInfo','article_main','f14 mb10','content-txt','main_topic','class="t_f"','content','txtmain','tpc_content"','article_content'
,'t_msgfont','con f_14','info','Amain_main','cellspacing="0"','cellpadding="0"','content_id','xname="content','id="thread"','align="center"']
#获取作者
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
#获取正文
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