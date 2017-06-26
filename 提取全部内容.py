# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:54:31 2017

@author: zara
"""
import os
from urllib.request import Request
from urllib.request import urlopen
from lxml import html
from bs4 import BeautifulSoup
import numpy as np
import re
import chardet
import pandas as pd
import json
import codecs
#提取标题
f = open('C:\\Users\\zara\\Desktop\\C题-url_verify.txt','r',encoding='utf-8')
urls = f.readlines()
for lenurl in range(400,512):
    print(lenurl)
    url = urls[lenurl].strip()
    try:
        try:
            data1 = urlopen(url).read()
            charset = chardet.detect(data1)['encoding']
            request = Request(url=url)
            response = urlopen(request)
            html = response.read().decode(charset)
        except:
            charset = 'gbk'
            request = Request(url=url)
            response = urlopen(request)
            html = response.read().decode(charset)
    
        
        soup = BeautifulSoup(html,'lxml')
        title_soup = soup.find('title').get_text()
        fs = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'w',encoding=charset)
        fs.writelines(html)
        fs.close()
        fr = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'r',encoding=charset)
        html2 = fr.readlines()
        title = []
        z = []
        for i in html2:
            soup2 = BeautifulSoup(i,'lxml')
            i = soup2.get_text().strip()
            z.append(i)
            if((i in title_soup)&(i!='')&(i!=title_soup)&(i not in title)):
                title.append(i)
        if len(title) >1:
            max = 0
            for i in range(len(title)):
                if (i<len(title)-1):
                    if(len(title[i])<len(title[i+1])):
                        max = i+1
            title = title[max]
        if ((title==[])|('论坛' in title)):
            title = []
            title.append(title_soup)
        
        
        #提取正文
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
            
        try:
            data = urlopen(url).read()
            charset = chardet.detect(data) ['encoding']
            request = Request(url=url)
            response = urlopen(request)
            html = response.read().decode(charset)
        except:
            charset = 'gbk'
            request = Request(url=url)
            response = urlopen(request)
            html = response.read().decode(charset)
        fr = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'r',encoding=charset)
        html2 = fr.readlines()
        for i in range(len(html2)):
            html2[i] = html2[i].strip().replace('\n','')
        need = []
        index = []
        need_word = Word_set(word_content,html2)
        needMat = np.matrix(need_word)
        
        test1_result = []
        for n in range(len(needMat)):
            test1_result.append(classify(needMat[n],weight_content))
        
        test1_result = pd.DataFrame(test1_result)
        name_index = test1_result[test1_result[0]==1].index
        html2  = pd.DataFrame(html2)
        name = html2.ix[name_index]
        name = list(name.values)
        p1 = re.compile(r'<(\w+) ')
        p2 = re.compile(r'class="(.*?)"')
        p3 = re.compile(r'id="(.*?)"')
        content_max = []
        cn = []
        soup = BeautifulSoup(html,'lxml')
        for i in name:
            Tag = p1.findall(i[0])
            Class = p2.findall(i[0])
            Id = p3.findall(i[0])
            if((Class!=[])&(Id!=[])):
                data = soup.find_all(Tag,attrs={'class':Class,'id':Id})
                if(data != []):
                    for d in data:
                        content_max.append(d.get_text().strip())
                        cn.append(str(d))
            elif (Class!=[]):
                data = soup.find_all(Tag,attrs={'class':Class})
                if(data != []):
                    for d in data:
                        content_max.append(d.get_text().strip())
                        cn.append(str(d))
            else:
                data = soup.find_all(Tag,attrs={'id':Id})
                if(data != []):
                    for d in data:
                        content_max.append(d.get_text().strip())
                        cn.append(str(d))
                        
        #提取作者
        try:
            fr = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'r',encoding=charset)
            html = fr.readlines()
        except:
            fr = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'r',encoding='gbk')
            html = fr.readlines()
        for i in range(len(html)):
            html[i] = html[i].strip().replace('\n','')
        need = []
        index = []
        need_word = Word_set(word_name,html)
        needMat = np.matrix(need_word)
        
        test1_result = []
        for n in range(len(needMat)):
            test1_result.append(classify(needMat[n],weight_name))
        
        test1_result = pd.DataFrame(test1_result)
        name_index = test1_result[test1_result[0]==1].index
        html  = pd.DataFrame(html)
        name = html.ix[name_index]
        name = list(name.values)
        name_max = []
        for na in range(len(name)):
            soup = BeautifulSoup(name[na][0],'lxml')
            text = soup.get_text()
            if ((text !='')&(len(text)<8)):
                name_max.append(text.strip())
        z = 0
        n = []
        if(len(name_max)%2==0):
            for i in range(len(name_max)):
                if (i%2==0):
                    n.append(i)
                    if(name_max[i]==name_max[i+1]):
                        z+=1
        remove_name = []
        for i in n:
            remove_name.append(name_max[i])
        if(z>=len(name_max)/2):
            for i in remove_name:
                name_max.remove(i)
        
        #提取时间
        #data1 = urlopen(url).read()
        #charset = chardet.detect(data1)['encoding']
        request = Request(url=url)
        response = urlopen(request)
        html = response.read().decode(charset)
        fr = open('C:\\Users\\zara\\Desktop\\网络爬虫\\test\\%d.txt'%1,'r',encoding=charset)
        html2 = fr.readlines()
        time = []
        for i in html2:
            soup2 = BeautifulSoup(i,'lxml')
            i = soup2.get_text().strip()
            t = re.findall(r'(\d+-\d+.*\d+:.\d)',i)
            if (t!=[]):
                time.append(t[0])
        if (time==[]):
            for i in html2:
                soup2 = BeautifulSoup(i,'lxml')
                i = soup2.get_text().strip()
                t = re.findall(r'(\d+-\d+.*\d+)',i)
                if (t!=[]):
                    time.append(t[0])
        if (len(time)>=2):
            time1 = pd.DataFrame(time)
            time1 = time1.drop_duplicates()
            time = []
            for i in time1.values:
                time.append(i[0])
        data = {}
        data['post']={}
        if(len(title)>0):
            data['post']['title'] = title
        if((len(content_max)>0)&(len(content_max)<100)):
            data['post']['content'] = content_max[0].replace('\r','').replace('\n','')
        if(len(name_max)>0):
            data['post']['author'] = name_max[0]
        if(len(time)>0):
            data['post']['publish_date'] = time[0] 
        if len(content_max)>1:
            data['replys']=[]
            for i in range(len(content_max)-1):
                data['replys'].append({})
                data['replys'][i]['title'] = title
                if (len(content_max)>i+1&(len(content_max)<100)):
                    data['replys'][i]['content'] = content_max[i+1].replace('\r','').replace('\n','')
                if ((len(name_max))>i+1&(len(name_max)<100)):
                    data['replys'][i]['author'] = name_max[i+1]
                if (len(time)>i+1):
                    data['replys'][i]['publish_date'] = time[i+1]
        json_str = json.dumps(data,sort_keys=True,ensure_ascii=False) # json.dumps 中文是unicode 编码
        try:
            f = codecs.open('E:\\C题程序\\test\\test5_data.txt','a','utf-8')
            f.write(url+'\t'+json_str +os.linesep)
            f.close()
        except:
            f = codecs.open('E:\\C题程序\\test\\test5_data.txt','a',charset)
            f.write(url+'\t'+json_str +os.linesep)
            f.close()
                #last_result.append(title)
                #last_result.append(content_max)
                #last_result.append(name_max)
                #last_result.append(time)
                #last_result.append('------------')
    except:
        pass
