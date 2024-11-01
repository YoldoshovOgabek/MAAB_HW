from math import isqrt
n = int(input('Enter a positive integer: '))

a=[]
for i in range(1, isqrt(n)+1):
    if(n%i==0):
    	a.append(i)
    	if(n/i!=i):a.append(n//i)
a.sort()
for i in a:
	print(f'{i} is a factor of {n}')
