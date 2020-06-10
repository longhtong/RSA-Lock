import Utils as u
import encryption as en
import decryption as de
import random
import os
from egcd import egcd
from sys import byteorder, getsizeof

LOWERBOUND = 1e259 #RSA-260 
UPPERBOUND = 9.99999999999999999999999999999999999999999999999999999999999999e259
#the last 4 digit of N % e + (coprime to N * e mod + 662)= word breaker
class RSAObj(object):
    delimiter = "~"
    securityDigits = 3
    def __init__(self, p = None, q = None, N = None, e = None, d = None):
        self.secretDictionary = {}
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
    def clearDictionaries(self):
        self.secretDictionary.clear()
    def encrypteMess(self):
        if self.binary:
            return en.encrypt(int.from_bytes(self.message, byteorder), self.N, self.e)
        result = ""
        breaker = (((self.N % 1000) % self.e) + (self.N * self.e + 662)) % 100      
        for i in self.message:
            if not self.binary:
                numIn = ord(i)
            else:
                numIn = i
            numEn = en.encrypt(numIn, self.N, self.e)
            result = result + str(numEn) + str(breaker + u.getFirstDigits(numEn, self.securityDigits)) + self.delimiter 
        return result

    def decrypteMess(self):
        if self.binary:
            return de.decrypt(int(self.message), self.e, self.p, self.q, self.d, self.N)
        breaker = (((self.N % 1000) % self.e) + (self.N * self.e + 662)) % 100   
        subsets = self.message.split(self.delimiter)
        result = ""
        #print(subsets)
        for letter in subsets:
            if letter == "" or letter == "\n" or letter == None:
                break
            #print(letter)
            if letter in self.secretDictionary:
                result += chr(self.secretDictionary[letter])
            else:
                letterNum = int(letter)
                #print(letterNum)
                securityLen = u.getNumLength(breaker + u.getFirstDigits(letterNum, self.securityDigits))
                letterNum = letterNum // (10**securityLen)
                letterNum = de.decrypt(letterNum, self.e, self.p, self.q, self.d, self.N)
                #print("letterNum: ", letterNum, "\n")
                result += chr(letterNum)

                self.secretDictionary[letter] = letterNum
        return result

    def encryptBin(self, outputName, fileExt):
        #need to save data in an array
        counter = 1
        with open(self.filePathIn, "rb") as ufile:
            result = fileExt + "\n"
            while True:
                line = ufile.readline()
                if line == "" or line == "\n" or not line:
                    break
                self.message = line
                #print(line, " ", counter, " \n")
                result = result + str(getsizeof(self.message)) + "\n" + str(self.encrypteMess()) + "\n"
                counter += 1
        if self.filePathOut == None:
            raise Exception("No file path out found.")
        #result = bytearray(result)
        outputName = outputName + "_ENCRYPTED.txt"
        newPath = os.path.join(self.filePathOut, outputName)
        with open(newPath, "w") as fileOut:
            #print(result)
            fileOut.write(str(result))
            #fileOut.write("\n")
    
    def decryptBin(self, outputName):
        counter = 1
        #outputName = outputName + "_DECRYPTED_FILE." + fileExt
        with open(self.filePathIn, "r") as ufile:
            result = ""
            fileExt = ufile.readline()
            outputName = outputName + "_DECRYPTED_FILE." + fileExt
            newPath = os.path.join(self.filePathOut, outputName)
            outFile = open(newPath, "wb")
            while True:
                length = ufile.readline()
                line = ufile.readline()
                if line == "" or length == "":
                    break
                
                self.message = str(line)
                #print(type(self.message))
                toWrite = self.decrypteMess().to_bytes(int(length), byteorder)
                outFile.write(toWrite)
            outFile.close()
       

    def encryptFile(self, outputName, fileExt):
        if self.filePathIn == None:
            raise Exception("No File Path Provided!")
        if not os.path.isfile(self.filePathIn):
            raise Exception("Invalid File Path!")
        if os.path.getsize(self.filePathIn) == 0:
            raise Exception("Empty File!")

        readAccess = "r"
        writeAccess = "w"
        if self.binary:
            self.encryptBin(outputName, fileExt)
        else:
        
            with open(self.filePathIn, readAccess) as ufile:
                result = fileExt + "\n"
                while True:
                    line = ufile.readline()
                    if line == '':
                        break
                    self.message = line
                    #print(line + "\n")
                    result = result + self.encrypteMess()
            if self.filePathOut == None:
                return result
            else:
                #Process Filename
                #outputName = u.getFileName(self.filePathIn) + "_ENCRYPTED.txt"
                outputName = outputName + "_ENCRYPTED.txt"
                newPath = os.path.join(self.filePathOut, outputName)
                with open(newPath, writeAccess) as fileOut:
                    subsets = result.split(self.delimiter)
                    for num in subsets:
                        if num == "":
                            break
                        fileOut.write(num + self.delimiter)
                        fileOut.write("\n")
    
    def decryptFile(self, outputName):
        if self.filePathIn == None:
            raise Exception("No File Path Provided!")
        if not os.path.isfile(self.filePathIn):
            raise Exception("Invalid File Path!")
        if os.path.getsize(self.filePathIn) == 0:
            raise Exception("Empty File!")
        
        readAccess = "r"
        writeAccess = "w"
        if self.binary:
            self.decryptBin(outputName)
        else:
            with open(self.filePathIn, readAccess) as ufile:
                result = ""
                fileExt = ufile.readline()
                while True:
                    line = ufile.readline()
                    if line == '':
                        break
                    self.message = str(line)
                    #print(type(self.message))
                    result = result + self.decrypteMess()
                    
            if self.filePathOut == None:
                return result
            else:
                #Process Filename
                #outputName = u.getFileName(self.filePathIn).split("_")[0] + "_DECRYPTED_FILE.txt"
                outputName = outputName + "_DECRYPTED_FILE." + fileExt
                #print("\n " + outputName + "\n")
                newPath = os.path.join(self.filePathOut, outputName)
                with open(newPath, writeAccess) as fileOut:
                    fileOut.writelines(result)

    


