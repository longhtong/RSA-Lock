import random
import decimal

def ASCIIConvert(message):
    result = 0
    for i in range(len(message)):
        result += ord(message[i])
    return result

#http://cacr.uwaterloo.ca/hac/about/chap4.pdf
#https://crypto.stackexchange.com/questions/1970/how-are-primes-generated-for-rsa
def getPrime(other):
    limit = 3
    prime = False

    randNum = decimal.Decimal(random.randrange(1e189, 9e189))
    while randNum % decimal.Decimal(2) == 0 or randNum == decimal.Decimal(other):
        randNum = random.randrange(1e189, 9e189)

    while not prime:
        
        #Get the largest 2^x factor that divides randNum
        twoPowerResult = largest2Power(randNum - 1)
        s = decimal.Decimal(twoPowerResult[1])
        r = decimal.Decimal((randNum - 1) / twoPowerResult[0])

        #check for prime
        for i in range(limit):
            a = random.randrange(2, randNum-2)
            while a == other:
                a = decimal.Decimal(random.randrange(2, randNum-2))
            y = (a**r) % randNum
            if y != 1 and y != (randNum-1):
                j = 1
                while j <= s-1 and y != (randNum-1):
                    y = (y**2) % randNum
                    if y == 1:
                        prime = False
                        break
                    j += 1
                if y != (randNum-1):
                    prime = False
            if prime == False:
                randNum += 2
                break
        
    return randNum

#https://crypto.stanford.edu/pbc/notes/numbertheory/millerrabin.html
def largest2Power(n):
    power = 1
    possible_power = []
    while (2**power) <= n:
        if (n % (2**power) == 0):
            possible_power.append(power)
        power += 1
    return (2**max(possible_power), max(possible_power))
        