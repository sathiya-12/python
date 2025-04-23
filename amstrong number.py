n=int(input("Enter a input number: "))
temp=n
a=0
while n>0:
    d=n%10
    a=a+d*d*d
    n //=10
if temp==a:
    print("Amstrong")
else:
    print("not Amstrong")
