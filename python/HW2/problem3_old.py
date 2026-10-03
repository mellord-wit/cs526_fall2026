def doIt(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return doIt(n-1) + doIt(n-2) - doIt(n-3)

print("do it with 1: ",doIt(1))
print("do it with 2: ",doIt(2))
print("do it with 6: ",doIt(6))
