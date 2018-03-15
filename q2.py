#coding:utf-8
a=input()
b=input()
def gcd(a,b):
    print str(a),str(b)
    if b==0:
        return a
    else:
        return gcd(b,a%b)
print "最大公約数は"+ str(gcd(a,b))
