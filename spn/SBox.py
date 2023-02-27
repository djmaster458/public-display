MASK0=0x000F
MASK1=0x00F0
MASK2=0x0F00
MASK3=0xF000

class SBox:
    def __init__(self, mapping:dict):
        """Creates a new substitution box with given substitution mapping"""
        self.mapping = mapping
        self.mapping_inv = { v:k for k,v in mapping.items() }
    

    def Encrypt(self, block:int) -> int:
        """Encrypts a block using forward SMap"""
        hex0 = (block & MASK0)
        hex1 = (block & MASK1) >> 4
        hex2 = (block & MASK2) >> 8
        hex3 = (block & MASK3) >> 12

        e_hex0 = self.mapping[hex0]
        e_hex1 = self.mapping[hex1]
        e_hex2 = self.mapping[hex2]
        e_hex3 = self.mapping[hex3]

        return (e_hex3 << 12) | (e_hex2 << 8) | (e_hex1 << 4) | e_hex0


    def Decrypt(self, block:int) -> int:
        """Decrypts a block using backward SMap"""
        e_hex0 = (block & MASK0)
        e_hex1 = (block & MASK1) >> 4
        e_hex2 = (block & MASK2) >> 8
        e_hex3 = (block & MASK3) >> 12

        hex0 = self.mapping_inv[e_hex0]
        hex1 = self.mapping_inv[e_hex1]
        hex2 = self.mapping_inv[e_hex2]
        hex3 = self.mapping_inv[e_hex3]

        return (hex3 << 12) | (hex2 << 8) | (hex1 << 4) | hex0