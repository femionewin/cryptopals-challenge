# https://cryptopals.com/sets/1/challenges/7

import base64
from Crypto.Cipher import AES

def decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

the_file = open('./7.txt', 'r')
data = the_file.read()

decoded = base64.b64decode(data)

# How is this 16 bytes if ascii chars are only 7 bits??
key = 'YELLOW SUBMARINE'

decrypted = decrypt(key, decoded)
print(decrypted)
