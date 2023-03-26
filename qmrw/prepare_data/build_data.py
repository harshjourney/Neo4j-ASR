import re
import os
import json
import pandas as pd

dictx = {}
with open(file=r'./dict/school.txt', mode='r',encoding='UTF-8',errors='ignore') as f:
    res = f.readlines()  # 读取数据
    list_sc = []
    for i in res:
        list3 = i.strip()
        #print(list1)
        list_sc.append(list3)
dictx['name'] = list_sc

with open(file=r'./dict/desc.txt', mode='r',encoding='UTF-8',errors='ignore') as f:
    res = f.readlines()  # 读取数据
    list2 = []
    for i in res:
        list1 = i.replace('\\xa0','').replace('[','').replace(']','').replace("'",'').replace('\n','').replace(' ','')
        #print(list1)
        list2.append(list1)
dictx['desc'] = list2

with open(file=r'./dict/locate.txt', mode='r',encoding='UTF-8',errors='ignore') as f:
    res = f.readlines()  # 读取数据
    list_loc = []
    for i in res:
        list4 = i.replace('[','').replace(']','').replace('学校地址','').replace(':','').replace("'","").replace('：','').replace(' ','').replace('\n','')
        list_loc.append(list4)
dictx['loc'] = list_loc

with open(file=r'./dict/phonenum.txt', mode='r',encoding='UTF-8',errors='ignore') as f:
    res = f.readlines()  # 读取数据
    list_tel = []
    for i in res:
        listad = i.replace('联系电话：','').replace('[','').replace(']','').replace("'",'').replace(' ','').replace('\n','')
        list_tel.append(listad)
dictx['tel'] = list_tel

with open(file=r'./dict/guanwang.txt', mode='r+',encoding='UTF-8',errors='ignore') as f:
    res = f.readlines()  # 读取数据
    list_web = []
    for i in res:
        listweb = i.replace("'",'').replace('[','').replace(']','').replace(' ','').replace('\n','')
        list_web.append(listweb)
dictx['web'] = list_web

full = pd.DataFrame(dictx)
#数据填充
full.to_csv('school.csv')
