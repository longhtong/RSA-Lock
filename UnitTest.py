import encryption as en
import decryption as de
import Utils as utils
import rsa as rsa
lowerBound = 1e259 #RSA-260 
upperBound = 9.9999999999999999999999999999999999e259
path = "/home/jack/Desktop/RSATesting.txt"
pathOut = "/home/jack/Desktop"
def basicTest():
    print(en.encrypt(51, 55, 3))
    print(de.decrypt(en.encrypt(1, 55, 3),3,5,11))
    #print(utils.getPrime(3))
    x=1448253698229368010440434731715527436907444603619475643788436617178249755772639373106977420768228382693177505625573860309370280198474280439809533913663126983115003782748411347405597222712977
    #print(utils.largest2Power(91))
    #print(utils.miillerTest(x))
    #print(utils.MillerRabinPrime(x, -1))
    #print(utils.getPrime(x, lowerBound, upperBound))
    #print(utils.getCoPrime(40))
def RSAObjTest():
    rsaTest = rsa.RSAObj.newUser()
    rsaTest.getMessage("Hello FRiend!!! HOw are you today? Would you like somebread? The USSR is coming")
    encrypted = rsaTest.encrypteMess()
    print(encrypted)

    #rsaTest1 = rsa.RSAObj.newUser()
    rsaTest.getMessage(encrypted)
    decryptedMess = rsaTest.decrypteMess()
    print(decryptedMess)
def RSAFileTest():
    rsaTest = rsa.RSAObj.newUser()
    rsaTest.setPathIn(path)
    content_noFile = rsaTest.encrypteFile()
    print(content_noFile)
    rsaTest.setPathOut(pathOut)
    content_wFile = rsaTest.encrypteFile()

    # newPath = "/home/jack/Desktop/ENCRYPTED FILE"
    # rsaTest.setPathIn(newPath)
    # rsaTest.decryptFile()
    
    

#RSAObjTest()
#basicTest()
RSAFileTest()