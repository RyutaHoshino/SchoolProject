#coding:utf-8
a,b=input(),input()
x=a*b
print ("a="+str(a)+",b="+str(b))
def gbc(a,b):
    if b==0:
        return a
    else:
        return gbc(b,a%b)
i=gbc(a,b)
print "最大公約数は"+str(i)
print "最小公倍数は"+str(a*b/i)
