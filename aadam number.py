n=int(input())
temp=n*n
r=0
e=0
while temp>=1:
    d1=temp%10
    e=e*10+d1
    temp //=10
print("Reverse(n2)", e)    
while n>=1:
    d=n%10
    r=r*10+d
    n //=10
r1=r*r
print("square(reverse(n))",r1)

if e==r1:
    print("Adam Number")
else :
    print("Not Adam Number")
