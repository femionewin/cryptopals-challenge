# Hexlify is used here for converting bytes to hex
from binascii import hexlify

def repeating_key_xor(key, string):
    # i is the position within the key
    i = 0
    arr = []
    for ch in string:
    	# Convert the key char and the plaintext char to
        # integers using `ord`, XOR them and add them to
        # the array.
        arr.append(ord(ch) ^ ord(key[i]))
        
		# Manage the "repeating" part of the repeating key.
        # If the end of the key is reached start back at the
        # beginning.
        i += 1
        if (i == len(key)):
            i = 0

	# Finally convert our array to a byte array (which
    # hexlify likes), then convert to hex and return it.
    return hexlify(bytearray(arr))

string = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
key = 'ICE'

encrypted = repeating_key_xor(key, string)
print(encrypted)
