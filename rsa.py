import Utils as u
import encryption as en
import decryption as de
import random
import os
from egcd import egcd

LOWERBOUND = 1e259 #RSA-260 
UPPERBOUND = 9.99999999999999999999999999999999999999999999999999999999999999e259
#the last 4 digit of N % e + (coprime to N * e mod + 662)= word breaker
class RSAObj(object):
    delimiter = "~"
    securityDigits = 3
    def __init__(self, p = None, q = None, N = None, e = None, d = None):
        self.p = p
        self.q = q
        self.N = N
        self.e = e
        self.d = d
        self.message = None
        self.filePathIn = None
        self.filePathOut = None
        self.binary = False

    @classmethod
    def newUser(cls):
        newP = u.getPrime(-1, LOWERBOUND, UPPERBOUND)
        newQ = u.getPrime(newP, LOWERBOUND, UPPERBOUND)
        newE = u.getCoPrime((newP - 1) * (newQ - 1))
        return cls(newP, newQ, newP * newQ, newE)
    def getN(self):
        return self.N
    def getE(self):
        return self.e
    def getD(self):
        return egcd(self.e, (self.p-1)*(self.q-1))[1] % ((self.p-1)*(self.q-1))
    def getMessage(self, inputMess):
        self.message = inputMess
    def setPathIn(self, path):
        self.filePathIn = path
    def setPathOut(self, path):
        self.filePathOut = path
    def setBinaryOn(self):
        self.binary = True

    def encrypteMess(self):
        result = ""
        breaker = ((self.N % 10000) % self.e) + u.getCoPrime(self.N * self.e + 662)    
        for i in self.message:
            numEn = en.encrypt(ord(i), self.N, self.e)
            result = result + str(numEn) + str(breaker + u.getFirstDigits(numEn, self.securityDigits)) + self.delimiter 
        return result

    def decrypteMess(self):
        breaker = ((self.N % 10000) % self.e) + u.getCoPrime(self.N * self.e + 662)
        subsets = self.message.split(self.delimiter)
        result = ""
        #print(subsets)
        for letter in subsets:
            if letter == "" or letter == "\n":
                break
            #print(letter)
            letterNum = int(letter.strip())
            #print(letterNum)
            securityLen = u.getNumLength(breaker + u.getFirstDigits(letterNum, self.securityDigits))
            letterNum = letterNum // (10**securityLen)
            letterNum = de.decrypt(letterNum, self.e, self.p, self.q, self.d, self.N)
            result += chr(letterNum)
        return result

    def encrypteFile(self):
        if self.filePathIn == None:
            raise Exception("No File Path Provided!")
        if not os.path.isfile(self.filePathIn):
            raise Exception("Invalid File Path!")
        if os.path.getsize(self.filePathIn) == 0:
            raise Exception("Empty File!")

        readAccess = "r"
        writeAccess = "w"
        if self.binary:
            readAccess = "r+"
            writeAccess = "w+"
        

        with open(self.filePathIn, readAccess) as ufile:
            result = ""
            while True:
                line = ufile.readline()
                if line == "":
                    break
                self.message = line
                result = result + self.encrypteMess()
        if self.filePathOut == None:
            return result
        else:
            #Process Filename
            outputName = u.getFileName(self.filePathIn) + "_ENCRYPTED.txt"
            newPath = os.path.join(self.filePathOut, outputName)
            with open(newPath, writeAccess) as fileOut:
                subsets = result.split(self.delimiter)
                for num in subsets:
                    if num == "":
                        break
                    fileOut.write(num + self.delimiter)
                    fileOut.write("\n")
    
    def decryptFile(self):
        if self.filePathIn == None:
            raise Exception("No File Path Provided!")
        if not os.path.isfile(self.filePathIn):
            raise Exception("Invalid File Path!")
        if os.path.getsize(self.filePathIn) == 0:
            raise Exception("Empty File!")
        
        readAccess = "r"
        writeAccess = "w"
        if self.binary:
            readAccess = "r+"
            writeAccess = "w+"

        with open(self.filePathIn, readAccess) as ufile:
            result = ""
            while True:
                line = ufile.readline()
                if line == "":
                    break
                self.message = str(line)
                #print(type(self.message))
                result = result + self.decrypteMess()
                
        if self.filePathOut == None:
            return result
        else:
            #Process Filename
            outputName = u.getFileName(self.filePathIn).split("_")[0] + "_DECRYPTED_FILE.txt"
            print("\n " + outputName + "\n")
            newPath = os.path.join(self.filePathOut, outputName)
            with open(newPath, writeAccess) as fileOut:
                fileOut.writelines(result)




