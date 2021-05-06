import math
import time

print('MD5 algorithm python step by step for learning purpose =-')

# <========================== algorithm constants
BLOCK_SIZE = 64 # or 512 bits but remember last one should do 448 bits (56 chars)
PADDING = [
    128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
T = [   0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 
        0xd62f105d, 0x2441453,  0xd8a1e681, 0xe7d3fbc8, 
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
# <========================== algorithm constants

# define the message
msg = 'You know, I know this steak doesn\'t exist. I know that when I put it in my mouth, the Matrix is telling my brain that it is juicy and delicious. After nine years, you know what I realize? Ignorance is bliss.'

print('---\r\n'+msg+'\r\n---')

# translate the text message into an array of msg's character ascii codes
msg = [ord(c) for c in msg]

# =========================== STEP 1 - padding
msglen = len(msg)
index = msglen % 64
if index < 56:
    msg = msg + PADDING[0:(56-index)]
else:
    msg = msg + PADDING[0:(120-index)]
# =========================== STEP 2 - append message length in bits !
msg = msg+list((msglen*8).to_bytes(8, 'little'))
# =========================== STEP 3 - init words
word_A = 0x67452301
word_B = 0xefcdab89
word_C = 0x98badcfe
word_D = 0x10325476
# =========================== STEP 4 - process our formatted message
def fun_F(x, y, z):
    return (((x) & (y)) | ((~x) & (z)))

def fun_G(x, y, z):
    return (((x) & (z)) | ((y) & (~z)))

def fun_H(x, y, z):
    return ((x) ^ (y) ^ (z))

def fun_I(x, y, z):
    return ((y) ^ ((x) | (~z)))

def fun_rotleft(x, n):
    return (((x) << (n)) | ((x) >> (32-(n))))

def decode_block(raw):
    proecssdblock = []
    for i in range(0, len(raw), 4):
        proecssdblock.append((raw[i]) | ((raw[i+1]) << 8) | ((raw[i+2]) << 16) | ((raw[i+3]) << 24))
    return(proecssdblock)

for i in range(math.ceil(len(msg) / BLOCK_SIZE)):
    block = decode_block(msg[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE])

    AA = word_A
    BB = word_B
    CC = word_C
    DD = word_D

    # STEP 4 - ROUND 1
    word_A = (word_B + fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[0] + 0xd76aa478) % 0x100000000 , 7))
    word_D = (word_A + fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[1] + 0xe8c7b756) % 0x100000000 , 12))
    word_C = (word_D + fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[2] + 0x242070db) % 0x100000000 , 17))
    word_B = (word_C + fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[3] + 0xc1bdceee) % 0x100000000 , 22))
    word_A = (word_B + fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[4] + 0xf57c0faf) % 0x100000000 , 7))
    word_D = (word_A + fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[5] + 0x4787c62a) % 0x100000000 , 12))
    word_C = (word_D + fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[6] + 0xa8304613) % 0x100000000 , 17))
    word_B = (word_C + fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[7] + 0xfd469501) % 0x100000000 , 22))
    word_A = (word_B + fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[8] + 0x698098d8) % 0x100000000 , 7))
    word_D = (word_A + fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[9] + 0x8b44f7af) % 0x100000000 , 12))
    word_C = (word_D + fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[10] + 0xffff5bb1) % 0x100000000 , 17))
    word_B = (word_C + fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[11] + 0x895cd7be) % 0x100000000 , 22))
    word_A = (word_B + fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[12] + 0x6b901122) % 0x100000000 , 7))
    word_D = (word_A + fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[13] + 0xfd987193) % 0x100000000 , 12))
    word_C = (word_D + fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[14] + 0xa679438e) % 0x100000000 , 17))
    word_B = (word_C + fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[15] + 0x49b40821) % 0x100000000 , 22))

    # STEP 4 - ROUND 2
    word_A = (word_B + fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[1] + 0xf61e2562) % 0x100000000 , 5))
    word_D = (word_A + fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[6] + 0xc040b340) % 0x100000000 , 9))
    word_C = (word_D + fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[11] + 0x265e5a51) % 0x100000000 , 14))
    word_B = (word_C + fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[0] + 0xe9b6c7aa) % 0x100000000 , 20))
    word_A = (word_B + fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[5] + 0xd62f105d) % 0x100000000 , 5))
    word_D = (word_A + fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[10] + 0x2441453) % 0x100000000 , 9))
    word_C = (word_D + fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[15] + 0xd8a1e681) % 0x100000000 , 14))
    word_B = (word_C + fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[4] + 0xe7d3fbc8) % 0x100000000 , 20))
    word_A = (word_B + fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[9] + 0x21e1cde6) % 0x100000000 , 5))
    word_D = (word_A + fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[14] + 0xc33707d6) % 0x100000000 , 9))
    word_C = (word_D + fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[3] + 0xf4d50d87) % 0x100000000 , 14))
    word_B = (word_C + fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[8] + 0x455a14ed) % 0x100000000 , 20))
    word_A = (word_B + fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[13] + 0xa9e3e905) % 0x100000000 , 5))
    word_D = (word_A + fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[2] + 0xfcefa3f8) % 0x100000000 , 9))
    word_C = (word_D + fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[7] + 0x676f02d9) % 0x100000000 , 14))
    word_B = (word_C + fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[12] + 0x8d2a4c8a) % 0x100000000 , 20))

    # STEP 4 - ROUND 3
    word_A = (word_B + fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[5] + 0xfffa3942) % 0x100000000 , 4))
    word_D = (word_A + fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[8] + 0x8771f681) % 0x100000000 , 11))
    word_C = (word_D + fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[11] + 0x6d9d6122) % 0x100000000 , 16))
    word_B = (word_C + fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[14] + 0xfde5380c) % 0x100000000 , 23))
    word_A = (word_B + fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[1] + 0xa4beea44) % 0x100000000 , 4))
    word_D = (word_A + fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[4] + 0x4bdecfa9) % 0x100000000 , 11))
    word_C = (word_D + fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[7] + 0xf6bb4b60) % 0x100000000 , 16))
    word_B = (word_C + fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[10] + 0xbebfbc70) % 0x100000000 , 23))
    word_A = (word_B + fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[13] + 0x289b7ec6) % 0x100000000 , 4))
    word_D = (word_A + fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[0] + 0xeaa127fa) % 0x100000000 , 11))
    word_C = (word_D + fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[3] + 0xd4ef3085) % 0x100000000 , 16))
    word_B = (word_C + fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[6] + 0x4881d05) % 0x100000000 , 23))
    word_A = (word_B + fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[9] + 0xd9d4d039) % 0x100000000 , 4))
    word_D = (word_A + fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[12] + 0xe6db99e5) % 0x100000000 , 11))
    word_C = (word_D + fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[15] + 0x1fa27cf8) % 0x100000000 , 16))
    word_B = (word_C + fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[2] + 0xc4ac5665) % 0x100000000 , 23))

    # STEP 4 - ROUND 4
    word_A = (word_B + fun_rotleft((word_A + fun_I(word_B, word_C, word_D) + block[0] + 0xf4292244) % 0x100000000 , 6))
    word_D = (word_A + fun_rotleft((word_D + fun_I(word_A, word_B, word_C) + block[7] + 0x432aff97) % 0x100000000 , 10))
    word_C = (word_D + fun_rotleft((word_C + fun_I(word_D, word_A, word_B) + block[14] + 0xab9423a7) % 0x100000000 , 15))
    word_B = (word_C + fun_rotleft((word_B + fun_I(word_C, word_D, word_A) + block[5] + 0xfc93a039) % 0x100000000 , 21))
    word_A = (word_B + fun_rotleft((word_A + fun_I(word_B, word_C, word_D) + block[12] + 0x655b59c3) % 0x100000000 , 6))
    word_D = (word_A + fun_rotleft((word_D + fun_I(word_A, word_B, word_C) + block[3] + 0x8f0ccc92) % 0x100000000 , 10))
    word_C = (word_D + fun_rotleft((word_C + fun_I(word_D, word_A, word_B) + block[10] + 0xffeff47d) % 0x100000000 , 15))
    word_B = (word_C + fun_rotleft((word_B + fun_I(word_C, word_D, word_A) + block[1] + 0x85845dd1) % 0x100000000 , 21))
    word_A = (word_B + fun_rotleft((word_A + fun_I(word_B, word_C, word_D) + block[8] + 0x6fa87e4f) % 0x100000000 , 6))
    word_D = (word_A + fun_rotleft((word_D + fun_I(word_A, word_B, word_C) + block[15] + 0xfe2ce6e0) % 0x100000000 , 10))
    word_C = (word_D + fun_rotleft((word_C + fun_I(word_D, word_A, word_B) + block[6] + 0xa3014314) % 0x100000000 , 15))
    word_B = (word_C + fun_rotleft((word_B + fun_I(word_C, word_D, word_A) + block[13] + 0x4e0811a1) % 0x100000000 , 21))
    word_A = (word_B + fun_rotleft((word_A + fun_I(word_B, word_C, word_D) + block[4] + 0xf7537e82) % 0x100000000 , 6))
    word_D = (word_A + fun_rotleft((word_D + fun_I(word_A, word_B, word_C) + block[11] + 0xbd3af235) % 0x100000000 , 10))
    word_C = (word_D + fun_rotleft((word_C + fun_I(word_D, word_A, word_B) + block[2] + 0x2ad7d2bb) % 0x100000000 , 15))
    word_B = (word_C + fun_rotleft((word_B + fun_I(word_C, word_D, word_A) + block[9] + 0xeb86d391) % 0x100000000 , 21))

    word_A = (word_A + AA) % 0x100000000 
    word_B = (word_B + BB) % 0x100000000 
    word_C = (word_C + CC) % 0x100000000 
    word_D = (word_D + DD) % 0x100000000 

md_digest = word_A.to_bytes(8, 'little')
md_digest += word_B.to_bytes(8, 'little')
md_digest += word_C.to_bytes(8, 'little')
md_digest += word_D.to_bytes(8, 'little')

print("".join(map(lambda x: hex(x).lstrip("0x"), md_digest)))
