import random
import decimal
from egcd import egcd
import math
def ASCIIConvert(message):
    result = 0
    for i in range(len(message)):
        result += ord(message[i])
    return result

#http://cacr.uwaterloo.ca/hac/about/chap4.pdf
#https://crypto.stackexchange.com/questions/1970/how-are-primes-generated-for-rsa
def getPrime(other, lowerBound, upperBound):
    while True:
        randNum = random.randrange(lowerBound, upperBound)
        while randNum % 2 == 0.0 or randNum == other:
            randNum = random.randrange(1e189, 9e189)
        if MillerRabinPrime(randNum, other):
            return randNum

#https://crypto.stanford.edu/pbc/notes/numbertheory/millerrabin.html
def largest2Power(n):
    power = 1
    possible_power = [0]
    while (2**power) <= n:
        if (n % (2**power) == 0):
            possible_power.append(power)
        power += 1
    return (2**max(possible_power),max(possible_power))

#https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
#http://cacr.uwaterloo.ca/hac/about/chap4.pdf
def MillerRabinPrime(n, other):
    limit = 3
    #Get the largest 2^x factor that divides randNum
    twoPowerResult = largest2Power(n - 1)
    s = twoPowerResult[1]
    r = (n - 1) // twoPowerResult[0]

    #check for prime
    for i in range(limit):
        a = random.randrange(2, n-2)
        while a == other:
            a = random.randrange(2, n-2)
        y = pow(a,r,n)
        if y != 1 and y != (n-1):
            j = 1
            while j <= (s-1) and y != (n-1):
                y = pow(y,2,n)
                if y == 1:
                    return False
                j += 1
            if y != (n-1):
                return False
    return True
       

        

  

