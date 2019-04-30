#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all" 

import numpy as np
import pandas as pd
import os
import sys
import datetime
from random import random as rd

#filepath is filepath
def mutateData(filepath, indexlist, carnum=7, boxNum=5,a=3,b=8,c=5,d=3,e=2):#path,list,7
    #boxNum-车间数
    #读取原表格，配合indexlist
    df=pd.read_csv(filepath)
    print(filepath)
    #变异的表集叫resultTable
    resultTable=pd.DataFrame()
    #删除第一列的索引
    chooseC=list(df.columns)
    type(chooseC)
    del chooseC[0]
    df=df[chooseC]
    
    #把顺序表集划分为表，根据indexlist遍历
    colnum=df.shape[1]
    rownum=df.shape[0]
    length=len(indexlist)
    
    #变异2-两个表的交叉变异
    while length>1:
        #table1 table2
        # print("length---",length)
        tablei1=int(length*rd())
        table1=indexlist[tablei1]
        # print("tablei1 is",tablei1)
        del indexlist[tablei1]
        tablei2=int((length-1)*rd())
        table2=indexlist[tablei2]
        # print("tablei2 is",tablei2)
        del indexlist[tablei2]
        #length-2
        length-=2
        
        # table1=carnum*table1
        # table2=carnum*table2
        table1=df[table1:table1+carnum]
        
        table2=df[table2:table2+carnum]
        
        #原表加入选集
        resultTable=pd.concat([resultTable,table1],axis=0,ignore_index=True)
        resultTable=pd.concat([resultTable,table2],axis=0,ignore_index=True)
        
        #选择交叉的车间
        exchangeIndex=int(boxNum*rd())
        temp=[0,a,a+b,a+b+c,a+b+c+d,a+b+c+d+e]
        start=temp[exchangeIndex]
        end=temp[exchangeIndex+1]
        chooseColumn=[]
        for i in range(end-start):
            chooseColumn.append(str(start+i))

        # print(chooseColumn)
        
        #交叉
        temptable=table1.copy(deep=True)
        # print("=============tab2 table=============")
        # print(table2)
        # print("=============tab1 table=============")
        # print(temptable)
        copy=table2.loc[:,chooseColumn].copy(deep=True)
        # print("=============copy table=============")
        # print(copy)
        copy=np.array(copy).tolist()
        # print("=============temp table=============")
        # print(temptable.loc[:,chooseColumn])
        temptable.loc[:,chooseColumn]=copy
        #突变
        # print("====================before change====================")
        # print(temptable)
        # print("====================after change=====================")
        temptable=saltation(temptable,colnum,carnum)
        # if YYY==True:
        #     print(temptable)
        # else:
        #     print("====================no change========================")
        #加入列表
        resultTable=pd.concat([resultTable,temptable],axis=0,ignore_index=True)
        #交叉
        temptable=table2.copy(deep=True)
        copy=table1.loc[:,chooseColumn].copy(deep=True)
        copy=np.array(copy).tolist()
        temptable.loc[:,chooseColumn]=copy
        #突变
        temptable=saltation(temptable,colnum,carnum)
        #加入列表
        resultTable=pd.concat([resultTable,temptable],axis=0,ignore_index=True)
        
    #导出到excel
    basedir=os.getcwd()
    # time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    # filedir=basedir+"\\data\\out\\"+time+"mutatetable.csv"
    filedir=basedir+"\\data\\out\\"+"mutatetable.csv"

    print(resultTable.tail(1))

    resultTable.to_csv(filedir)
    return filedir


def saltation(basetable,colnum,rownum):
    #指标:可有5次突变机会（不一定成功），成功就跳出
    baseindex=list(basetable.index)[0]
    isSaltated=False
    circleTime=0
    while isSaltated==False and circleTime<5:
        circleTime+=1
        #随机一个col上交换位置
        coli=int(rd()*colnum)
        #待变异表newtable
        newtable=basetable.copy(deep=True)
        coltarget=list(newtable[str(coli)])

        # print(circleTime)
        # print("coltarget: ")
        # print(coltarget)
        #保存顺序
        root=[]
        reroot=[]

        for rowi in range(rownum):
            # print("rowi=",rowi)
            # print("rownum=",rownum)
            if coltarget[rowi]!=0:
                root.append(coltarget[rowi])
                #随机摇序号
                pos=int((len(reroot)+1)*rd())
                reroot.insert(pos,coltarget[rowi])

        #顺序一样说明不变异
        if root==reroot:
            continue
        else:
            #新顺序替换旧顺序（变异）
            for rowi in range(rownum):
                if coltarget[rowi]!=0:
                    newtable.loc[baseindex+rowi:baseindex+rowi,str(coli)]=reroot[0]
                    del reroot[0]
                isSaltated=True
            # print(newtable)
            # print(type(newtable))
    return newtable


##试运行

# filepath="C:/Users/14994/Desktop/代码/遗传算法/data/out/50.csv"
# indexlist=[1,2,5,50]
# mutateData(filepath, indexlist, carnum=7,a=3,b=8,c=5,d=3,e=2)#path,list,7


# In[ ]:


#变异1-单个表的变异
#     for i in range(time):
#         #取表至basetable
#         target=indexlist[i]
#         tablestart=target*7
#         tableend=(target+1)*7
#         basetable=df[tablestart:tableend]
#         newtables.append(basetable)
#         
#         #仅在单个表的某一col上交换位置
#         for coli in range(colnum):
#             #待变异表newtable
#             newtable=basetable.copy(deep=True)
#             coltarget=list(newtable[coli])

#             root=[]
#             reroot=[]
#             for rowi in range(carnum):
#                 if coltarget[rowi]!=0:
#                     root.append(coltarget[rowi])
#                     #随机摇序号
#                     pos=int((len(reroot)+1)*rd())
#                     reroot.insert(pos,coltarget[rowi])

#             #顺序一样说明不变异
#             if root==reroot:
#                 continue

#             #新顺序替换旧顺序（变异）
#             for rowi in range(carnum):
#                 if coltarget[rowi]!=0:
#                     newtable.loc[tablestart+rowi:tablestart+rowi,coli]=reroot[0]
#                     del reroot[0]