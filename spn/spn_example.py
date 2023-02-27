from SPN import SPN

ENCRYPTEDFILE='encrypted_dog.jpg'
DECRYPTEDFILE='decrypted_dog.jpg'
ORIGINALFILE='dog.jpg'

KEY = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]
SMAP = {
    0x0: 0xE,
    0x1: 0x4,
    0x2: 0xD,
    0x3: 0x1,
    0x4: 0x2,
    0x5: 0xF,
    0x6: 0xB,
    0x7: 0x8,
    0x8: 0x3,
    0x9: 0xA,
    0xA: 0x6,
    0xB: 0xC,
    0xC: 0x5,
    0xD: 0x9,
    0xE: 0x0,
    0xF: 0x7
}
PMAP = {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 1,
    5: 5,
    6: 9,
    7: 13,
    8: 2,
    9: 6,
    10: 10,
    11: 14,
    12: 3,
    13: 7,
    14: 11,
    15: 15
}

spn = SPN(KEY, SMAP, PMAP)

padding = spn.EncryptFile(ORIGINALFILE, ENCRYPTEDFILE)
spn.DecryptFile(ENCRYPTEDFILE, DECRYPTEDFILE, padding)

print(f'Original File: {ORIGINALFILE}')
print(f'Encrypted File: {ENCRYPTEDFILE}')
print(f'Decrypted File: {DECRYPTEDFILE}')