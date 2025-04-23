n =int(input())
r=0
while n>1:
    d=n%10
    r+=d*d
    n//=10
    r=n
if n==1:
    print("Happy Number")
else:
    print("Not happy number")
    
