def SwapBits(num, b1, b2):
    """Swaps bits at index b1 and b2"""
    set1 = (num >> b1) & 1
    set2 = (num >> b2) & 1
    x = (set1 ^ set2)
    x = (x << b1) | (x << b2)

    return num ^ x


class PBox:
    def __init__(self, mapping:dict, blockSizeInBits=16):
        """Creates a new PBox with given mapping for block of size N bits"""
        if len(mapping) != blockSizeInBits:
            raise Exception('PMap must be size of block size in bits.')

        self.mapping = mapping
        self.mapping_inv = { v:k for k,v in mapping.items() }
        self.blockSizeInBits = blockSizeInBits
    

    def Encrypt(self, block:int) -> int:
        """Encrypts a block using forward PMap"""
        for i in range(self.blockSizeInBits):
            block = SwapBits(block, i, self.mapping[i])

        return block


    def Decrypt(self, block:int) -> int:
        """Decrypts a block using backward PMap"""
        for i in range(self.blockSizeInBits):
            block = SwapBits(block, i, self.mapping_inv[i])

        return block
        