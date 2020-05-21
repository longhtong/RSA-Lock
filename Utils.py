import random

def ASCIIConvert(message):
    result = 0
    for i in range(len(message)):
        result += ord(message[i])
    return result

#http://cacr.uwaterloo.ca/hac/about/chap4.pdf
#https://crypto.stackexchange.com/questions/1970/how-are-primes-generated-for-rsa
def getPrime():
    randNum = random.randrange(1e189, 9e189)
    
    while randNum % 2 != 0:
        randNum = random.randrange(1e189, 9e189)
        
    #check for prime
    return randNum