from egcd import egcd
#decrypt enMess
#enMess: an integer value
#e: integer value that is coprime to (p-1)(q-1)
#p, q: prime numbers
def decrypt(enMess, e, p = None, q = None, d = None, N = None):
    #print("Enmess: ", enMess, "\n")
    if d is None:
        #print("Bad1")
        inversedE = egcd(e, (p-1)*(q-1))[1] % ((p-1)*(q-1))
    else:
        #print("Good1 ", d, "\n")
        inversedE = d
    if N is None:
        #print("Bad1")
        return pow(enMess, inversedE, p*q)
    else:
        #print("Good1 ", N, "\n")
        return pow(enMess, inversedE, N)
    #(enMess**inversedE) % (p*q)
