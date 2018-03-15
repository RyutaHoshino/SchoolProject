#coding:utf-8
import random
num=30
count=0
for i in range(num):
    a=random.uniform(0,1)
    b=random.uniform(0,1)
    if a*a+b*b<1:
        count+=1
print ("pi="+str(4.0*count/num))
