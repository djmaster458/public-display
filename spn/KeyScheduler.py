SUBKEYSIZE=4

class KeyScheduler:
    def __init__(self, key:list, number_of_rounds:int):
        """
            Creates a new Key Scheduler for SPN. 
            Key is a list of single-digit, hex numbers.
            Generates 4 hex char round keys.
        """

        self.key = key
        self.number_of_rounds = number_of_rounds
        
    def GetRoundKey(self, round:int):
        """Return the key for a given round"""
        if round not in range(self.number_of_rounds):
            raise Exception(f'Round must be in range: {range(self.number_of_rounds)}')

        lsn = round + SUBKEYSIZE - 1
        result = 0

        result = (self.key[lsn]) | result
        result = (self.key[lsn -1] << 4) | result
        result = (self.key[lsn -2] << 8) | result
        result = (self.key[lsn -3] << 12) | result
        
        return result

    def GetFinalKey(self):
        """Returns the final key for SPN"""
        result = 0
        lsn = len(self.key) - 1

        result = (self.key[lsn]) | result
        result = (self.key[lsn -1] << 4) | result
        result = (self.key[lsn -2] << 8) | result
        result = (self.key[lsn -3] << 12) | result
        
        return result
