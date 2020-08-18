import encryption as en
import decryption as de
import Utils as utils
import rsa as rsa
import unittest
from egcd import egcd
import filecmp 

class TestUtils(unittest.TestCase): 
    
    def setUp(self):
        self.lowerBound = 1e259 #RSA-260 
        self.upperBound = 9.9999999999999999999999999999999999e259
        self.testNums = [93383711897212911396958447042532050323727062482325155078645033614965216062355223103800636263113279517620420984575335170313940100024515531535219908258285773226078359091093527777258978900771303696451570603245032862990929343856761161394936410566955724417999811811,
                         13385873519475816143082450000623258454757272094093928616852818189642954038376442323378964055640150374022909555803183572942308954193227357784621495530759776621991420827057095335259481622164960641611699483768685275765462388066781729418653404761226913639092624547,
                         13385873519475816143082450000623258454757272094093928616852818189642954038376442323378964055640150374022909555803183572942308954193227357784621495530759776621991420827057095335259481622164960641611699483768685275765462388066781729418653404761226913639092624540,
                         78377548084331611993701143631344828714702343346227903078985755734117669820835792723302996641962320366830088872234571790140609610931816575643576962213337431711424694624646984424058904918657520574871852114450935547821025727163735370742525402591172560090251663241,
                         37527322338300293148339094585082583770658707833965790165539338666081614724865510406834614803844534639555115530123377845063813902835625007656761882469359934511490105121516146708998893260562722608765439115897598704118006010887211481077431393246710000844589829959,
                         37527322338300293148339094585082583770658707833965790165539338666081614724865510406834614803844534639555115530123377845063813902835625007656761882469359934511490105121516146708998893260562722608765439115897598704118006010887211481077431393246710000844589829952]

    def testMiller(self):
        result = [True, True, False, True, True, False]
        for i in range(len(self.testNums)):
            self.assertEqual(utils.MillerRabinPrime(self.testNums[i], -1), result[i])
    def testgetPrime(self):
        for _ in range(5):
            self.assertTrue(utils.MillerRabinPrime(utils.getPrime(self.testNums[0], self.lowerBound, self.upperBound), -1)) 
    def testgetCoPrime(self):
        for _ in range(5):
            prime = utils.getCoPrime(utils.getPrime(self.testNums[0], self.lowerBound, self.upperBound))
            coPrime = utils.getCoPrime(prime)
            self.assertEqual(egcd(prime,coPrime)[0], 1)

class TestMessagesBasics(unittest.TestCase):
    
    def setUp(self):
        self.path = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/"
        self.pathPlainText = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/test.txt"
        self.pathCipherText = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/test_ENCRYPTED.txt"
        self.shortMessage = "This is a test file!!!"
        self.shortCipherText = "157882350822094580151968147843281847469871015180061308032096170403692544211~"

    def testMessages(self):
        message = "Hello Friend!!! How are you today?"
        rsaTest = rsa.RSAObj.newUser()
        rsaTest.getMessage(message)
        encrypted = rsaTest.encrypteMess()
        self.assertNotEqual(encrypted, message)

        rsaTest.getMessage(encrypted)
        decryptedMess = rsaTest.decrypteMess()
        self.assertEqual(decryptedMess, message)

    def testEncryptNoOut(self):
        rsaTest = rsa.RSAObj.newUser()
        rsaTest.setPathIn(self.pathPlainText)
        message = rsaTest.encryptFile("test", "txt")
        self.assertNotEqual(message, self.shortMessage)

    def testDecryptNoOut(self):
        rsaTest = rsa.RSAObj.newUser()
        rsaTest.setPathIn(self.pathPlainText)
        rsaTest.setPathOut(self.path)
        rsaTest.encryptFile("test", "txt")
        rsaTest.setPathIn(self.pathCipherText)
        rsaTest.setPathOut("")
        plaintext = rsaTest.decryptFile("test_ENCRYPTED")
        self.assertNotEqual(plaintext, self.shortCipherText)
        
class TestFiles(unittest.TestCase):
    def setUp(self):
        self.path = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/"
        self.pathPlainText = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/longtest.txt"
        self.pathCipherText = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/longtest_ENCRYPTED.txt"
        self.pathDecryptedText = "/home/longtong/Documents/Projects/RSA-Encryptor/testData/longtest_ENCRYPTED_DECRYPTED_FILE"

    def testFile(self):
        rsaTest = rsa.RSAObj.newUser()
        rsaTest.setPathIn(self.pathPlainText)
        rsaTest.setPathOut(self.path)
        rsaTest.encryptFile("longtest", "txt")

        rsaTest.setPathIn(self.pathCipherText)
        rsaTest.setPathOut(self.path)
        rsaTest.decryptFile("longtest_ENCRYPTED")
        self.assertTrue(filecmp.cmp(self.pathPlainText, self.pathDecryptedText, shallow = False))

    def testStressTest(self):
        for _ in range(5):
            rsaTest = rsa.RSAObj.newUser()
            rsaTest.setPathIn(self.pathPlainText)
            rsaTest.setPathOut(self.path)
            rsaTest.encryptFile("longtest", "txt")

            rsaTest.setPathIn(self.pathCipherText)
            rsaTest.setPathOut(self.path)
            rsaTest.decryptFile("longtest_ENCRYPTED")
            self.assertTrue(filecmp.cmp(self.pathPlainText, self.pathDecryptedText, shallow = False))

class TestSadFiles(unittest.TestCase):
    def testEnSad(self):
        rsaTest = rsa.RSAObj.newUser()

        #No path in
        with self.assertRaises(Exception) as msg:
            rsaTest.encryptFile("longtest", "txt")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "No File Path Provided!")

        #Incorrect path
        rsaTest.setPathIn("/home")
        with self.assertRaises(Exception) as msg:
            rsaTest.encryptFile("longtest", "txt")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "Invalid File Path!")

        #Empty File
        rsaTest.setPathIn("/home/longtong/Documents/Projects/RSA-Encryptor/testData/empty.txt")
        with self.assertRaises(Exception) as msg:
            rsaTest.encryptFile("empty", "txt")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "Empty File!")
    
    def testDeSad(self):
        rsaTest = rsa.RSAObj.newUser()

        #No path in
        with self.assertRaises(Exception) as msg:
            rsaTest.decryptFile("longtest")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "No File Path Provided!")

        #Incorrect path
        rsaTest.setPathIn("/home")
        with self.assertRaises(Exception) as msg:
            rsaTest.decryptFile("longtest")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "Invalid File Path!")

        #Empty File
        rsaTest.setPathIn("/home/longtong/Documents/Projects/RSA-Encryptor/testData/empty.txt")
        with self.assertRaises(Exception) as msg:
            rsaTest.decryptFile("empty")
        warnMsg = msg.exception
        self.assertEqual(warnMsg.args[0], "Empty File!")

        






if __name__ == '__main__':
    unittest.main()