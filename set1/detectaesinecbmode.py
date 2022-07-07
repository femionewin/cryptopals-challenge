# https://cryptopals.com/sets/1/challenges/8

# Helper to split a string into arbitrary length blocks
def split_in_n(ciphertext, length):
    blocks = []

    start = 0
    end = length
    while(1):
        if (start >= len(ciphertext)): break

        blocks.append(ciphertext[start:end])
        start = end
        end += length

    return blocks

# The problem with ECB is that it is stateless and deterministic; the same 16
# byte plaintext block will always produce the same 16 byte ciphertext.
#
# This function will score a given ciphertext by seeing how many 16 byte
# repeating chunks there are in it.
def score_ciphertext(ciphertext):
    # Every 32 hex characters is 16 bytes (a hex character is 4 bits wide). This
    # splits the ciphertext into chunks of that size.
    blocks = split_in_n(ciphertext, 32)

    total = 0
    for block in blocks:
        # Subtract 1 so the string we're checking doesn't get counted.
        # Otherwise just treat each additional duplicated block as 1 point.
        score = blocks.count(block) - 1
        total += score

    return total


# Open the file and read it's lines, cleaning up newlines
the_file = open('./8.txt', 'r')
ciphertexts = [line.rstrip('\n') for line in the_file]

# Loop over each ciphertext, score each one and remember the highest scoring
# line.
max_score = 0
max_ciphertext = ''
for ciphertext in ciphertexts:
    score = score_ciphertext(ciphertext)
    if (score > max_score):
        max_score = score
        max_ciphertext = ciphertext

print(max_score)
print(max_ciphertext)
