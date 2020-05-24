import Utils as u
import encryption as en
import decryption as de

LOWERBOUND = 1e259 #RSA-260 
UPPERBOUND = 9e259

class RSAObj(object):
    def __init__(self, p = None, q = None, N = None, e = None):
        self.p = p
        self.q = q
        self.N = N
        self.e = e
        self.message = None
        self.filePath = None

    @classmethod
    def newUser(cls):
        newP = u.getPrime(-1, LOWERBOUND, UPPERBOUND)
        newQ = u.getPrime(newP, LOWERBOUND, UPPERBOUND)
        newE = u.getCoPrime((newP-1)*(newQ-1))
        return cls(newP, newQ, newP*newQ, newE)
    
    def getMessage(self, inputMess):
        self.message = inputMess

    def encrypteString(self):
        pass
        