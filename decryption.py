from egcd import egcd
#decrypt enMess
#enMess: an integer value
#e: integer value that is coprime to (p-1)(q-1)
#p, q: prime numbers
def decrypt(enMess, e, p, q):
    inversedE = egcd(e, (p-1)*(q-1))[1] % ((p-1)*(q-1))
    return (enMess**inversedE) % (p*q)
