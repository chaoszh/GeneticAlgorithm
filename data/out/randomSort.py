from random import random as rd

filesize=int(input("filesize="))

for i in range(filesize):
	reset=[]
	f=open("data"+str(i+1)+".txt",'r')
	content=f.read()
	content=content.split()
	datasize=len(content)

	for j in range(datasize):
		pos=int(len(reset)*rd())
		reset.insert(pos,content[j])

	f=open("data"+str(i+1)+".txt",'w')
	for j in range(datasize):
		f.write(reset[j]+' ')
	f.close()