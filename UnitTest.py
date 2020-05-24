import encryption as en
import decryption as de
import Utils as utils
lowerBound = 1e259 #RSA-260 
upperBound = 9e259
print(en.encrypt(13, 55, 3))
print(de.decrypt(en.encrypt(13, 55, 3),3,5,11))
#print(utils.getPrime(3))
x=1448253698229368010440434731715527436907444603619475643788436617178249755772639373106977420768228382693177505625573860309370280198474280439809533913663126983115003782748411347405597222712977
#print(utils.largest2Power(91))
#print(utils.miillerTest(x))
#print(utils.MillerRabinPrime(x, -1))
print(utils.getPrime(x, lowerBound, upperBound))
print(utils.getCoPrime(40))