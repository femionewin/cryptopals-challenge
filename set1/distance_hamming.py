def hamming_distance(bytes1, bytes2):
  # The strings must be equal length or this will fail.
  assert len(bytes1) == len(bytes2)

  distance = 0
  for zipped_bytes in zip(bytes1, bytes2):
    # XOR a bit from bytes1 with the corresponding bit in bytes2
    x = zipped_bytes[0] ^ zipped_bytes[1]

    set_bits = 0
    while (x > 0):
      # Check if the right most bit is set. If it is then track it.
      set_bits += x & 1;

      # Right shift the bits so we can check the next one in line.
      x >>= 1; 

    # Add the number of set bits for the current chars to the total
    # distance
    distance += set_bits

  return distance


b1 = b'this is a test'
b2 = b'wokka wokka!!!'

assert hamming_distance(b1, b2) == 37
print(hamming_distance(b1, b2))
