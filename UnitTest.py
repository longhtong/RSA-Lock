import encryption as en
import decryption as de
import Utils as utils
print(en.encrypt(13, 55, 3))
print(de.decrypt(en.encrypt(13, 55, 3),3,5,11))
print(utils.getPrime())