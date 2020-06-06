from egcd import egcd
#decrypt enMess
#enMess: an integer value
#e: integer value that is coprime to (p-1)(q-1)
#p, q: prime numbers
def decrypt(enMess, e, p, q, d = None, N = None):
    if d is None:
        #print("Bad1")
        inversedE = egcd(e, (p-1)*(q-1))[1] % ((p-1)*(q-1))
    else:
        #print("Good1")
        inversedE = d
    if N is None:
        #print("Bad1")
        return pow(enMess, inversedE, p*q)
    else:
        #print("Good1")
        return pow(enMess, inversedE, N)
    #(enMess**inversedE) % (p*q)
