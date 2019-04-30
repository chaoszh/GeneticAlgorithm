#!/usr/bin/env python
# coding: utf-8

# In[65]:


#-*- coding:utf-8 -*-
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 


# In[127]:


import numpy as np
import pandas as pd
import os
import sys
import datetime
from random import random as rd


# In[136]:


if __name__=="__main__":

    ###########
    # 函数参数列表
    # df
    df=pd.read_excel("data/out/test.xlsx")
    # indexlist
    indexlist=[1,7,3,2,5]#索引从0开始
    # carnum
    carnum=7
    ###########

    #变异的表集叫newtables
    newtables=[]


    #删除第一列的索引
    dict=[]
    for i in range(20):
        dict.append(i)
    df=df[dict]

    #把顺序表集划分为表，根据indexlist遍历
    colnum=df.shape[1]
    rownum=df.shape[0]
    time=len(indexlist)
    for i in range(time):
        #取表至basetable
        target=indexlist[i]
        tablestart=target*7
        tableend=(target+1)*7
        basetable=df[tablestart:tableend]
        newtables.append(basetable)
        #变异1-单个表的变异
        #仅在单个表的某一col上交换位置
        for coli in range(colnum):
            #待变异表newtable
            newtable=basetable.copy(deep=True)
            coltarget=list(newtable[coli])

            root=[]
            reroot=[]
            for rowi in range(carnum):
                if coltarget[rowi]!=0:
                    root.append(coltarget[rowi])
                    #随机摇序号
                    pos=int((len(reroot)+1)*rd())
                    reroot.insert(pos,coltarget[rowi])

            #顺序一样说明不变异
            if root==reroot:
                continue

            #新顺序替换旧顺序（变异）
            for rowi in range(carnum):
                if coltarget[rowi]!=0:
                    newtable.loc[tablestart+rowi:tablestart+rowi,coli]=reroot[0]
                    del reroot[0]

            #变异表加入表集
            newtables.append(newtable)

    #合并成dataframe
    resultTable=None

    newtablesnum=len(newtables)
    # newtablesnum

    for i in range(newtablesnum):
        newtable=newtables[i]
        resultTable=pd.concat([resultTable,newtable],axis=0,ignore_index=True)

    #导出到excel
    basedir=os.getcwd()
    time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filedir=basedir+"\\data\\out\\"+time+"mutatetable.csv"

    resultTable.to_csv(filedir)
    # writer=pd.ExcelWriter(filedir)
    # resultTable.to_excel(writer)
    # writer.save()


# In[135]:


def mutateData(filepath, indexlist, carnum):
    #读取原表格，配合indexlist
    df=pd.read_excel(filepath)
    #变异的表集叫newtables
    newtables=[]
    #删除第一列的索引
    dict=[]
    for i in range(20):
        dict.append(i)
    df=df[dict]
    
    #把顺序表集划分为表，根据indexlist遍历
    colnum=df.shape[1]
    rownum=df.shape[0]
    time=len(indexlist)
    for i in range(time):
        #取表至basetable
        target=indexlist[i]
        tablestart=target*7
        tableend=(target+1)*7
        basetable=df[tablestart:tableend]
        newtables.append(basetable)
        #变异1-单个表的变异
        #仅在单个表的某一col上交换位置
        for coli in range(colnum):
            #待变异表newtable
            newtable=basetable.copy(deep=True)
            coltarget=list(newtable[coli])

            root=[]
            reroot=[]
            for rowi in range(carnum):
                if coltarget[rowi]!=0:
                    root.append(coltarget[rowi])
                    #随机摇序号
                    pos=int((len(reroot)+1)*rd())
                    reroot.insert(pos,coltarget[rowi])

            #顺序一样说明不变异
            if root==reroot:
                continue

            #新顺序替换旧顺序（变异）
            for rowi in range(carnum):
                if coltarget[rowi]!=0:
                    newtable.loc[tablestart+rowi:tablestart+rowi,coli]=reroot[0]
                    del reroot[0]

            #变异表加入表集
            newtables.append(newtable)
    
    #合并成dataframe
    resultTable=None

    newtablesnum=len(newtables)
    # newtablesnum

    for i in range(newtablesnum):
        newtable=newtables[i]
        resultTable=pd.concat([resultTable,newtable],axis=0,ignore_index=True)
        
    #导出到excel
    basedir=os.getcwd()
    time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filedir=basedir+"\\data\\out\\"+time+"mutatetable.csv"

    resultTable.to_csv(filedir)


# In[ ]:




