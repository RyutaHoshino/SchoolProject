#coding :utf-8
a=1
b=0
while a<2**31:
    print a
    a,b=a+b,a
