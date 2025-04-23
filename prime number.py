n=int(input("Enter number: "))
if (n==1) or (n==0):
    print("Not a prime number")
elif n==2:
    print("Prime number")
else:
    for i in range(2,6):
        if n%i==0:
            print("Not a prime number")
            break
    else:
        print("Prime number")
