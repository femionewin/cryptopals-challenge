# https://cryptopals.com/sets/1/challenges/6

# An important lesson I took away from this... Understand what kind of data you are working with...
# Strings, base64, hex, etc

# Also, take maybe the top 3 key lengths or top 10

import base64
from binascii import hexlify

"""
Helper to calculate the Hamming distance between the bytes of two equal length
strings.
"""
def hamming_distance(bytes1, bytes2):
    # The strings must be equal length or this will fail.
    assert len(bytes1) == len(bytes2)

    distance = 0
    for zipped_bytes in zip(bytes1, bytes2):
        """
        XOR the integer representations of the current char in the string.
        This gets us a value whose byte representation is the integer where
        each bit is different between the two.

        Example:
           for ascii chars a and b
           ord('a') = 97 and ord('b') = 98
           97 in bytes is 0110 0001
           98 in bytes is 0110 0010
           97 ^ 98     is 0000 0011 (aka 3 in decimal)

        Where each bit is set in this new value represents a hamming distance
        of one. Now it's just a matter of summing those set bits.
        """
        x = zipped_bytes[0] ^ zipped_bytes[1]

        set_bits = 0
        while (x > 0):
            # Check if the right most bit is set. If it is then track it.
            set_bits += x & 1;

            """
            Shift the decimal value one bit to the right and do the process
            again.

            Bit shifting example:
            3 in decimal is 0000 0011 in binary
            3 >> 1       is 0000 0001 in binary

            We use each shifted value to compare to 1 (or 0000 0001 in bin)
            on the previous lines.
            """
            x >>= 1; 

        # Add the number of set bits for the current chars to the total distance
        distance += set_bits

    return distance




"""
Helper to find the potential length of the key that encrypted the text.

If we can determine the key length we can use that number to decrypt individual
chunks of text that are the length of that key.

Why is a low hamming distance an indicator of key length?

Well... We are working on a few assumptions here. We are assuming that the text
and the key are in English or are at least made up of letters in the English
alphabet. If we know that it's using English letters and not random bytes then
the hamming distance between two characters in the English alphabet should be
lower than two randomly distributed, completely unrelated, bytes.

So, a low hamming distance implies characters that are close to eachother on the
ASCII table. If we find a lot of characters that are close to eachother
(hamming distance wise) then this implies something that's not random and
probably written in English alphabet characters.
"""
def get_keylength(data):
    lowest = None
    best_keylength = None

    # This is a bit arbitrary but let's test key lengths from 2 - 40 and see
    # What kind of hamming distances we come up with.
    for i in range(2, 41):
        keylength = i

        """
        This array holds the normalized distance values for each KEYLENGTH
        sized chunk of the cypher text. All of these values will be averaged
        and the best (lowest) score is a good inficator of what the keylength
        actually is.
        """
        to_average = []

        """
        Grab chunks of the encrypted bytes until the final chunk is shorter than
        KEYLENGTH. That many chunks should provide us enough information to get
        a good normalized score for the current key length.
        """
        start = 0
        end = start + keylength
        while (1):
            # Grab 2 adjacent chunks of data that are KEYLENGTH long.
            first_chunk = data[start:end]
            second_chunk = data[start + keylength:end + keylength]

            """
            This is just an exit clause that basically just ignores the last
            dangling bit of text that will likely wind up shorter than
            KEYLENGTH. Having all the chunks of text up to that one should be
            sufficient.
            """
            if (len(second_chunk) < keylength):
                break

            """
            Get the hamming distance between the first chunk of byes and the
            second chunk of bytes. See comments on this function as to why a low
            hamming distance is a good indicator of a key.
            """
            distance = hamming_distance(first_chunk, second_chunk)

            """
            "Normalize" the distance. This basically gets it to a decimal
            place that is relative to the total keylength so that it can be
            compared to distances based on other key lengths.
            """
            normalized = distance / keylength

            # We've got a score append it to the list of distances we want the
            # average of.
            to_average.append(normalized)

            # Move on to the next chunk that we'll want to get hamming distances
            # for.
            start = end + keylength
            end = start + keylength

        # Find the average of those distances and then empty out the array for
        # the next iteration.
        average = sum(to_average) / len(to_average)
        to_average = []

        # Check if we've beat the current lowest score. If we have that's more
        # likely the correct key length.
        if lowest == None or average < lowest:
            lowest = average
            best_keylength = keylength

    return best_keylength


"""
Transpose chunks of the encrypted bytes into KEYLENGTH long blocks for each char
within the key (which we still don't know at this time).

Example:
Unencrypted text: Hello, how are you?
Repeating Key:    FINEFINEFINEFINEFIN

This would get broken up into...
F -> Hooro
I -> e,weu
N -> l   ?
E -> lhay

Even though we don't know the key this organizes the text into chunks that we
know have been XOR'd against the same byte/char.
"""
def transpose_chunks_by_keylength(keylength, data):
    # Create a dictionary for the number of chunks that the data can be broken
    # into.
    chunks = dict.fromkeys(range(keylength))

    i = 0
    for byte in data:
        # If we're at the end of the key start at the beginning again. This is
        # "repeating key" XOR after all.
        if (i == keylength): i = 0

        # If the chunk is null, set it to an empty array.
        if (chunks[i] == None): chunks[i] = []

        # Append the current byte to the chunk.
        chunks[i].append(byte)

        i += 1

    return chunks


"""
OK We've got our transposed blocks now we can use a scoring system to see what
the most likely values are for each char in the key.
"""
def get_key(blocks):
    common = 'ETAOIN SHRDLU'

    key = ''

    for i in blocks:
        current_high_score = 0
        current_key_char = ''

        for j in range(127):
            # Create an array of all the XOR'd
            x = [j ^ the_bytes for the_bytes in blocks[i]]

            # Convert the array of numbers back into bytes
            b = bytes(x)
            b_str = str(b, 'utf-8')

            score = 0
            for k in b_str.upper():
                if k in common:
                    score += 1

            if score > current_high_score:
                current_high_score = score
                current_key_char = chr(j)

        key += current_key_char

    return key


"""
We've got the key! Success. Now we just need to do a repeating key XOR between
each byte in the key and the corresponding encrypted byte in the text and if
all the prior steps have been completed properly this should give us our
decrypted message.
"""
def decrypt(message_bytes, key):
    decrypted = b''

    i = 0
    for byte in message_bytes:
        if (i == len(key)):
            i = 0

        xor = byte ^ ord(key[i])
        decrypted += bytes([xor])

        i += 1

    return decrypted


s1 = b'this is a test'
s2 = b'wokka wokka!!!'
assert hamming_distance(s1, s2) == 37

the_file = open('./6.txt', 'r')
data = the_file.read()

# We know the file is base64 encoded so decode it first, this converts it
# to raw bytes.
decoded = base64.b64decode(data)
# print(decoded)

# First we need to take a stab at finding the key length.
keylength = get_keylength(decoded)

# Once we have a good key length
chunks = transpose_chunks_by_keylength(keylength, decoded)
key = get_key(chunks)
decrypted = decrypt(decoded, key)
print(decrypted)
