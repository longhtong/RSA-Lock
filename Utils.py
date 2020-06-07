import random
import decimal
from egcd import egcd
import math
import ntpath
import sys

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
            randNum = random.randrange(lowerBound, upperBound)
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
    limit = 7 #increase for better security
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
       
def getCoPrime(n):
    while True:
        result = random.randrange(2, 100)
        if egcd(result, n)[0] == 1:
            return result
def getFirstDigits(n, stop):
    strN = str(n)
    return int(strN[0:stop])
def getNumLength(n):
    return len(str(n))

#Credit: https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
#Original Author: Lauritz V. Thaulow      
def getFileName(path):
    if "\\" in path and sys.platform == "linux":
        raise Exception("Potential Invalid Linux Path. File Cannot Be Processed.") 
    head, tail = ntpath.split(path)
    if head is None:
        raise Exception("Please select a file.")
    fileName = tail
    isTextFile = False
    if ".txt" in fileName:
        isTextFile = True
    return (fileName.split(".")[0], isTextFile, head.split(tail)[0])
    #tail.split(".")[0]
  

