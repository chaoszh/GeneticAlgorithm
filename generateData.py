#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
import sys
import datetime
from random import random as rd

#选择题号
question=int(input("What is the question number?(2/3):"))

#需要生成的数据的数量
dataAmount=int(input("输入需要生成的数据的数量："))

#动车基本信息
dfbasic=pd.read_excel("data/basicMessageQ"+str(question)+".xlsx")
##取数据示例 dfBasic['a'][0]==第一辆车在a车间中的检修时间

if question==2:
    #第二题车间数量
    a=3
    b=8
    c=5
    d=0
    e=0
else:
    #第三题车间数量
    a=3
    b=8
    c=5
    d=3
    e=2

boxnum=a+b+c+d+e
#列车数量
carnum=dfbasic.shape[0]#shape[0] 行 shape[1] 列
#作业数量
count=0
for index,row in dfbasic.iterrows():
    for i in row:
        if i!=0:
            count+=1

#生成多个顺序选择矩阵

##初始顺序表集
sequence=None

for time in range(dataAmount):
    
    #对车间进行选择
    choose=pd.DataFrame(np.zeros([carnum,boxnum],dtype=bool))
    for i in range(carnum):
        if dfbasic['a'][i]!=0:
            choose[int(a*rd())][i]=True;
        if dfbasic['b'][i]!=0:
            choose[int(b*rd()+a)][i]=True;
        if dfbasic['c'][i]!=0:
            choose[int(c*rd()+b+a)][i]=True;
        # if dfbasic['d'][i]!=0:
        #     choose[int(d*rd()+c+b+a)][i]=True;
        # if dfbasic['e'][i]!=0:
        #     choose[int(e*rd()+d+c+b+a)][i]=True;
    
    #生成随机顺序
    array=[]
    for i in range(count):
        pos=int((len(array)+1)*rd())
        array.insert(pos,i+1)

    #生成顺序表
    sequenceTable=pd.DataFrame(np.zeros([carnum,boxnum],dtype=int))

    n=0
    for i in range(boxnum):
        for j in range(carnum):
            if choose[i][j]==True:
                sequenceTable[i][j]=array[n]
                n+=1
    
    #加入顺序表集
    sequence = pd.concat([sequence,sequenceTable],axis=0,ignore_index=True)

    #hint
    if time%100==0:
        print("已生成"+str(time)+"个数据")

print("顺序表集生成结束")

#导出到excel
basedir=os.getcwd()
time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
filedir=basedir+"\\data\\in\\Question"+str(question)+"\\"+time+"generatetable.csv"
print("开始导出数据到"+filedir)
sequence.to_csv(filedir)
# writer=pd.ExcelWriter(filedir)
# sequence.to_excel(writer)
# writer.save()