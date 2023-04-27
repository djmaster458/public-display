from KeyScheduler import KeyScheduler
from SBox import SBox
from PBox import PBox
import sys

class SPN:
    def __init__(self, key:list, s_mapping:dict, p_mapping:dict, blocksize=2, number_of_rounds=4):
        """Creates a new SPN object with given SBox, PBox, Key, Number of Rounds, and Blocksize"""
        self.key_scheduler = KeyScheduler(key, number_of_rounds)
        self.sbox = SBox(s_mapping)
        self.pbox = PBox(p_mapping)
        self.blocksize = blocksize
        self.number_of_rounds = number_of_rounds


    def EncryptBlock(self, block:int) -> int:
        """Performs SPN Encryption of a block"""
        for i in range(self.number_of_rounds):
            block = block ^ self.key_scheduler.GetRoundKey(i)
            block = self.sbox.Encrypt(block)
            block = self.pbox.Encrypt(block)

        block = block ^ self.key_scheduler.GetFinalKey()
        return block


    def DecryptBlock(self, block:int) -> int:
        """Performs SPN Decryption of a block"""
        block = block ^ self.key_scheduler.GetFinalKey()

        for i in reversed(range(self.number_of_rounds)):
            block = self.pbox.Decrypt(block)
            block = self.sbox.Decrypt(block)
            block = block ^ self.key_scheduler.GetRoundKey(i)

        return block


    def EncryptFile(self, input_file:str, output_file:str):
        """Encrypt a given binary file to a given output file using SPN. Returns amount of padding added"""
        input_file_fp = open(input_file, 'rb')
        x = bytearray(input_file.read())

        padding = len(x) % self.blocksize
        x.extend(0 for i in range(padding))

        y = bytearray()

        for i in range(len(x) // self.blocksize):
            start = i * self.blocksize
            end = start + self.blocksize

            block = int.from_bytes(x[start:end], sys.byteorder)

            enc_block = self.EncryptBlock(block)
            y.extend(enc_block.to_bytes(self.blocksize, sys.byteorder))
        
        output_file_fp = open(output_file, 'wb')
        output_file_fp.write(y)

        output_file_fp.close()
        input_file_fp.close()

        return padding


    def DecryptFile(self, input_file:str, output_file:str, padding:int):
        """Decrypt a given binary file to a given output file using SPN. Padding field is to remove any padding added from encryption"""
        input_file_fp = open(input_file, 'rb')
        y = bytearray(input_file.read())
        z = bytearray()

        for i in range(len(y) // self.blocksize):
            start = i * self.blocksize
            end = start + self.blocksize

            block = int.from_bytes(y[start:end], sys.byteorder)

            dec_block = self.DecryptBlock(block)
            z.extend(dec_block.to_bytes(self.blocksize, sys.byteorder))

        z = z[:len(z) - padding]
        
        output_file_fp = open(output_file, 'wb')
        output_file_fp.write(z)

        input_file_fp.close()
        output_file_fp.close()
        