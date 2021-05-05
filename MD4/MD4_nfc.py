import math
import time

# <========================== interface support
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_array_by_block(array, bsize, hl_start=None, hl_end=None, hl_col=None):
    print('[ '+bcolors.OKBLUE+'block number'+bcolors.ENDC+' / '+bcolors.OKCYAN+'character pos in block'+bcolors.ENDC+' ]')
    print(bcolors.OKCYAN+'\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15'+bcolors.ENDC)
    for i in range(math.ceil(len(array) / bsize)):
        line_abb = bcolors.OKBLUE+str(i)+'\t'+bcolors.ENDC
        for j in range(bsize):
            if (hl_start is not None) & (hl_col is not None) & ((i*bsize+j) == hl_start):
                line_abb += hl_col
            line_abb += str(array[i*bsize+j])+'\t'
            if (hl_end is not None) & (hl_col is not None) & ((i*bsize+j) == hl_end):
                line_abb += bcolors.ENDC
        print(line_abb)

def print_checksum_generation(block,charpos,array):
    line_csgen = bcolors.OKBLUE+str(block)+bcolors.ENDC+':'+bcolors.OKCYAN+str(charpos).zfill(2)+bcolors.ENDC+'\t'+bcolors.OKGREEN
    for i in range(len(array)):
        line_csgen += str(array[i]).zfill(3)+'\t'
    print('\r'+line_csgen+bcolors.ENDC, end='')

def print_hash_raw(array, bsize):
    for i in range(math.ceil(len(array) / 16)):
        print(''.join(map(lambda x: str(x)+'\t',array[i:i+BLOCK_SIZE])))

# <========================== interface support

print(bcolors.WARNING+'MD4 algorithm python step by step for learning purpose =-'+bcolors.ENDC)

# <========================== algorithm constants
BLOCK_SIZE = 64 # or 512 bits but remember last one should do 448 bits (56 chars)
PADDING = [
    128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

# <========================== algorithm constants

# define the message
msg = 'The saddest aspect of life right now is that science gathers knowledge faster than society gathers wisdom.'

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
print((msglen*8).to_bytes(8, 'little'))
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
    return (((x) & (y)) | ((x) & (z)) | ((y) & (z)))

def fun_H(x, y, z):
    return ((x) ^ (y) ^ (z))

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
    word_A = fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[0]) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[1]) % 0x100000000 , 7)
    word_C = fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[2]) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[3]) % 0x100000000 , 19)

    word_A = fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[4]) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[5]) % 0x100000000 , 7)
    word_C = fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[6]) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[7]) % 0x100000000 , 19)

    word_A = fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[8]) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[9]) % 0x100000000 , 7)
    word_C = fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[10]) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[11]) % 0x100000000 , 19)

    word_A = fun_rotleft((word_A + fun_F(word_B, word_C, word_D) + block[12]) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_F(word_A, word_B, word_C) + block[13]) % 0x100000000 , 7)
    word_C = fun_rotleft((word_C + fun_F(word_D, word_A, word_B) + block[14]) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_F(word_C, word_D, word_A) + block[15]) % 0x100000000 , 19)

    # STEP 4 - ROUND 2
    word_A = fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[0] + 0x5A827999) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[4] + 0x5A827999) % 0x100000000 , 5)
    word_C = fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[8] + 0x5A827999) % 0x100000000 , 9)
    word_B = fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[12] + 0x5A827999) % 0x100000000 , 13)

    word_A = fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[1] + 0x5A827999) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[5] + 0x5A827999) % 0x100000000 , 5)
    word_C = fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[9] + 0x5A827999) % 0x100000000 , 9)
    word_B = fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[13] + 0x5A827999) % 0x100000000 , 13)

    word_A = fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[2] + 0x5A827999) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[6] + 0x5A827999) % 0x100000000 , 5)
    word_C = fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[10] + 0x5A827999) % 0x100000000 , 9)
    word_B = fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[14] + 0x5A827999) % 0x100000000 , 13)

    word_A = fun_rotleft((word_A + fun_G(word_B, word_C, word_D) + block[3] + 0x5A827999) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_G(word_A, word_B, word_C) + block[7] + 0x5A827999) % 0x100000000 , 5)
    word_C = fun_rotleft((word_C + fun_G(word_D, word_A, word_B) + block[11] + 0x5A827999) % 0x100000000 , 9)
    word_B = fun_rotleft((word_B + fun_G(word_C, word_D, word_A) + block[15] + 0x5A827999) % 0x100000000 , 13)

    # STEP 4 - ROUND 3
    word_A = fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[0] + 0x6ED9EBA1) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[8] + 0x6ED9EBA1) % 0x100000000 , 9)
    word_C = fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[4] + 0x6ED9EBA1) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[12] + 0x6ED9EBA1) % 0x100000000 , 15)

    word_A = fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[2] + 0x6ED9EBA1) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[10] + 0x6ED9EBA1) % 0x100000000 , 9)
    word_C = fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[6] + 0x6ED9EBA1) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[14] + 0x6ED9EBA1) % 0x100000000 , 15)

    word_A = fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[1] + 0x6ED9EBA1) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[9] + 0x6ED9EBA1) % 0x100000000 , 9)
    word_C = fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[5] + 0x6ED9EBA1) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[13] + 0x6ED9EBA1) % 0x100000000 , 15)

    word_A = fun_rotleft((word_A + fun_H(word_B, word_C, word_D) + block[3] + 0x6ED9EBA1) % 0x100000000 , 3)
    word_D = fun_rotleft((word_D + fun_H(word_A, word_B, word_C) + block[11] + 0x6ED9EBA1) % 0x100000000 , 9)
    word_C = fun_rotleft((word_C + fun_H(word_D, word_A, word_B) + block[7] + 0x6ED9EBA1) % 0x100000000 , 11)
    word_B = fun_rotleft((word_B + fun_H(word_C, word_D, word_A) + block[15] + 0x6ED9EBA1) % 0x100000000 , 15)

    word_A = (word_A + AA) % 0x100000000 
    word_B = (word_B + BB) % 0x100000000 
    word_C = (word_C + CC) % 0x100000000 
    word_D = (word_D + DD) % 0x100000000 

md_digest = word_A.to_bytes(8, 'little')
md_digest += word_B.to_bytes(8, 'little')
md_digest += word_C.to_bytes(8, 'little')
md_digest += word_D.to_bytes(8, 'little')

print("".join(map(lambda x: hex(x).lstrip("0x"), md_digest)))
