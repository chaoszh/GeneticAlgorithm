import xlrd
import pandas as pd
from mutateData import mutateData as mt

class CRH:
    def __init__(self):
        self.level = 0
        self.aWork = -1
        self.bWork = -1
        self.cWork = -1
        self.dWork = -1
        self.eWork = -1
        self.aTime = 0
        self.bTime = 0
        self.cTime = 0
        self.dTime = 0
        self.eTime = 0
        self.arvTime = 0
        self.repairTime = 0

class resIndex:
    def __init__(self):
        self.repTime=0
        self.index=-1

def repTime(train):
    res = 0
    aWork = [CRH(), CRH(), CRH()]  # 3
    bWork = [CRH(), CRH(), CRH(), CRH(), CRH(), CRH(), CRH(), CRH()]  # 8
    cWork = [CRH(), CRH(), CRH(), CRH(), CRH()]  # 5
    dWork = [CRH(), CRH(), CRH()]  # 3
    eWork = [CRH(), CRH()]  # 2
    wait = []

    if(len(train) == 1):
        return train[0].aTime+train[0].bTime+train[0].cTime+train[0].dTime+train[0].eTime

    startTime = train[0].arvTime
    aWork[train[0].aWork] = train.pop(0)
    while(wait or aWork or bWork
          or cWork or dWork or eWork):
        if(train):
            #列车到站，时间推进（可能一次跳跃多个车间，需修改代码，仅逻辑性完善，当前情况暂不需要）
            gapTime = train[0].arvTime-startTime
            startTime = train[0].arvTime
            wait.append(train.pop(0))
            res += gapTime
        else:
            #列车全部到站
            #print(res//60,res%60,len(aWork),len(bWork),len(cWork),len(dWork),len(eWork))
            if(len(aWork)):
                for i in range(len(aWork)):
                    if(aWork[i].level != 0 and aWork[i].repairTime < aWork[i].aTime):
                        gapTime = aWork[i].aTime-aWork[i].repairTime
                        break
            elif(len(bWork)):
                for i in range(len(bWork)):
                    if(bWork[i].level != 0 and bWork[i].repairTime < bWork[i].bTime):
                        gapTime = bWork[i].bTime-bWork[i].repairTime
                        break
            elif(len(cWork)):
                for i in range(len(cWork)):
                    if(cWork[i].level != 0 and cWork[i].repairTime < cWork[i].cTime):
                        gapTime = cWork[i].cTime-cWork[i].repairTime
                        break
            elif(len(dWork)):
                for i in range(len(dWork)):
                    if(dWork[i].level != 0 and dWork[i].repairTime < dWork[i].dTime):
                        gapTime = dWork[i].dTime-dWork[i].repairTime
                        break
            else:
                for i in range(len(eWork)):
                    if(eWork[i].level != 0 and eWork[i].repairTime < eWork[i].eTime):
                        gapTime = eWork[i].eTime-eWork[i].repairTime
                        break
            res += gapTime

        for i in range(len(aWork)):
            if(aWork[i].level != 0):
                aWork[i].repairTime += gapTime
        for i in range(len(bWork)):
            if(bWork[i].level != 0):
                bWork[i].repairTime += gapTime
        for i in range(len(cWork)):
            if(cWork[i].level != 0):
                cWork[i].repairTime += gapTime
        for i in range(len(dWork)):
            if(dWork[i].level != 0):
                dWork[i].repairTime += gapTime
        for i in range(len(eWork)):
            if(eWork[i].level != 0):
                eWork[i].repairTime += gapTime

        for i in range(len(eWork)):
            if(eWork[i].repairTime >= eWork[i].eTime):
                #print(eWork[i].repairTime,eWork[i].arvTime,"e")
                eWork[i] = CRH()
        for i in range(len(dWork)):
            #由检修表得d可能结束或转到e
            if(dWork[i].repairTime >= dWork[i].dTime):
                if(dWork[i].eWork == -1):
                    dWork[i] = CRH()
                elif(eWork[dWork[i].eWork].level == 0 and dWork[i].eWork >= 0):
                    #print(dWork[i].repairTime,dWork[i].arvTime,dWork[i].dTime,"d->e")
                    #print(len(aWork),len(bWork),len(cWork),len(dWork),len(eWork))
                    dWork[i].repairTime -= dWork[i].dTime
                    eWork[dWork[i].eWork] = dWork[i]
                    dWork[i] = CRH()
        for i in range(len(cWork)):
            #由检修表得c可能结束或转到d
            if(cWork[i].repairTime >= cWork[i].cTime):
                if(cWork[i].dWork == -1):
                    cWork[i] = CRH()
                elif(dWork[cWork[i].dWork].level == 0 and cWork[i].dWork >= 0):
                    #print(cWork[i].repairTime,cWork[i].arvTime,"c->d")
                    cWork[i].repairTime -= cWork[i].cTime
                    dWork[cWork[i].dWork] = cWork[i]
                    cWork[i] = CRH()
                    # elif([cWork[i].eWork] and eWork[cWork[i].eWork].level==0):
                    #     cWork[i].repairTime -= cWork[i].cTime
                    #     eWork[cWork[i].eWork] = cWork[i]
                    #     cWork[i] = CRH()
        for i in range(len(bWork)):
            #由检修表得b可能结束或转到c或d
            if(bWork[i].repairTime >= bWork[i].bTime):
                if(bWork[i].cWork == -1 and bWork[i].dWork == -1):
                    bWork[i] = CRH()
                elif(cWork[bWork[i].cWork].level == 0 and bWork[i].cWork >= 0):
                    #print(bWork[i].repairTime,bWork[i].arvTime,"b->c")
                    bWork[i].repairTime -= bWork[i].bTime
                    cWork[bWork[i].cWork] = bWork[i]
                    bWork[i] = CRH()
                elif(dWork[bWork[i].dWork].level == 0 and bWork[i].cWork == -1 and [bWork[i].dWork]):
                    #print(bWork[i].repairTime,bWork[i].arvTime,"b->d")
                    bWork[i].repairTime -= bWork[i].bTime
                    dWork[bWork[i].dWork] = bWork[i]
                    bWork[i] = CRH()
                    # elif([bWork[i].eWork] and eWork[bWork[i].eWork].level==0):
                    #     bWork[i].repairTime -= bWork[i].bTime
                    #     eWork[bWork[i].eWork] = bWork[i]
                    #     bWork[i] = CRH()
        for i in range(len(aWork)):
            #由检修表得a转到b或c
            if(aWork[i].repairTime >= aWork[i].aTime):
                if( bWork[aWork[i].bWork].level == 0 and aWork[i].bWork >= 0):
                    #print(aWork[i].repairTime,aWork[i].arvTime,"a->b")
                    aWork[i].repairTime -= aWork[i].aTime
                    bWork[aWork[i].bWork] = aWork[i]
                    aWork[i] = CRH()
                elif(cWork[aWork[i].cWork].level == 0 and aWork[i].bWork == -1 and aWork[i].cWork >= 0):
                    #print(aWork[i].repairTime,aWork[i].arvTime,"a->c")
                    aWork[i].repairTime -= aWork[i].aTime
                    cWork[aWork[i].cWork] = aWork[i]
                    aWork[i] = CRH()
        j = 0
        while(j < len(wait)):
            if(aWork[wait[j].aWork].level == 0):
                aWork[wait[j].aWork] = wait[j]
                #print(wait[j].arvTime,"wait")
                del wait[j]
                # for k in range(len(wait)):
                #     print(wait[k].arvTime,wait[k].aWork,"wait arv")
                j -= 1
            j += 1
        #print(len(train),"t",len(wait))
        if(len(train) == 0 and len(wait) == 0):
                i = 0
                if(len(aWork)):
                    while(i < len(aWork)):
                        #print(aWork[i].level,"a level")
                        if(aWork[i].level == 0):
                            #print("del a",i)
                            del aWork[i]
                            i -= 1
                        i += 1
                elif(len(bWork)):
                    while(i < len(bWork)):
                        if(bWork[i].level == 0):
                            del bWork[i]
                            i -= 1
                        i += 1
                elif(len(cWork)):
                    while(i < len(cWork)):
                        if(cWork[i].level == 0):
                            del cWork[i]
                            i -= 1
                        i += 1
                elif(len(dWork)):
                    while(i < len(dWork)):
                        if(dWork[i].level == 0):
                            del dWork[i]
                            i -= 1
                        i += 1
                else:
                    while(i < len(eWork)):
                        if(eWork[i].level == 0):
                            del eWork[i]
                            i -= 1
                        i += 1
    return res


def result():
    train = []
    num = 7
    for i in range(num):
        temp = CRH()
        if(i == 0):
            s = '00:16'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 2
        elif(i == 1):
            s = '00:47'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 5
        elif(i == 2):
            s = '01:22'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 2
        elif(i == 3):
            s = '02:00'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 6
        elif(i == 4):
            s = '02:21'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 3
        elif(i == 5):
            s = '03:02'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 6
        elif(i == 6):
            s = '03:31'
            temp.arvTime = int(s[0]+s[1])*60+int(s[3]+s[4])
            temp.level = 2
        if(temp.level == 2):
            temp.aTime = 1*60
            temp.bTime = 2*60
            temp.cTime = 1.5*60
            temp.dTime = 4*60
            temp.eTime = 7*60
        elif(temp.level == 3):
            temp.aTime = 0.8*60
            temp.bTime = 2.4*60
            temp.cTime = 0.5*60
            temp.dTime = 4.8*60
            temp.eTime = 6.5*60
        elif(temp.level == 5):
            temp.aTime = 1.3*60
            temp.bTime = 2.5*60
            temp.cTime = 1.5*60
            temp.dTime = 3*60
            temp.eTime = 6.5*60
        else:
            temp.aTime = 1*60
            temp.bTime = 2.7*60
            temp.cTime = 0.3*60
            temp.dTime = 5*60
            temp.eTime = 7*60
        for j in range(3):
            if(CRHs[i][j] != 0):
                temp.aWork = j
                break
            elif(j == 2):
                temp.aTime = 0
        for j in range(3, 11):
            if(CRHs[i][j] != 0):
                temp.bWork = j-3
                break
            elif(j == 10):
                temp.bTime = 0
        for j in range(11, 16):
            if(CRHs[i][j] != 0):
                temp.cWork = j-11
                break
            elif(j == 15):
                temp.cTime = 0
        for j in range(16, 19):
            if(CRHs[i][j] != 0):
                temp.dWork = j-16
                break
            elif(j == 18):
                temp.dTime = 0
        for j in range(19, 21):
            if(CRHs[i][j] != 0):
                temp.eWork = j-19
                break
            elif(j == 20):
                temp.eTime = 0
        train.append(temp)

    allTime = repTime(train)
    #print('The time needed for repair is: ', allTime //
    #60, 'hour(s)', allTime % 60, 'minute(s)!')

    return allTime


# myWorkbook = xlrd.open_workbook(
#     '/Users/return0/Downloads/QQFileRecv/20190429-204343generatetable.xlsx')
# mySheets = myWorkbook.sheets()
# mySheet = mySheets[0]

# row = mySheet.nrows
# col = mySheet.ncols

# csvFile = open('/Users/return0/Downloads/QQFileRecv/20190429-210305generatetable.csv','r')
# reader = csv.reader(csvFile)
carnum=7

qid="Question3"
filepath="data\\in\\"+qid+"\\1000.csv"
lastMin=0
flagout=0
circleTime=10
n=0
while True:
    n+=1
    data = pd.read_csv(filepath)
    CRHs = []
    index=[]
    allResult = []
    for i in range(len(data)):
        rowT = list(data.loc[i])
        del rowT[0]
        #print(rowT)
        CRHs.append(rowT)
        #print(i)
        if((i+1) % carnum == 0):
            tempTime=result()
            res=resIndex()
            res.repTime=tempTime
            res.index=i-carnum+1
            allResult.append(res)
            CRHs.clear()

    #distinctResult = list(set(allResult))
    allResult.sort(key=lambda resIndex: resIndex.repTime)
    # resResult=allResult[len(allResult)//2:len(allResult)] ## 最大值
    resResult=allResult[0:len(allResult)//2] ## 最小值
    print("length of resResult: ",len(resResult))
    #output
    folder="data\\out\\"
    f=open(folder+'data'+str(n)+'.txt','w')
    for i in resResult:
        # print(i.repTime)
        index.append(i.index)
        f.write(str(int(i.repTime))+' ')
    f.close()

    #jumpint out
    print("this time the shortest time is",resResult[0].repTime)
    if resResult[0].repTime==lastMin:
        flagout+=1
        if(flagout==circleTime-1):
            break
    else:
        lastMin=resResult[0].repTime

    print("--1-- GO TO MUTATE PROCEDURE--")
    filepath=mt(filepath,index)
    print("\n--2-- GO TO RESORT PROCEDURE--")