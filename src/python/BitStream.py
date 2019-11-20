class BitStream():
    def __init__(self):
        self.bit_array = []

    def read_file(self, file_name, nbits=None):
        if nbits is not None and nbits < 0:
            print("Error: Invalid number of bits, nbits must be positive")
            return False
        with open(file_name, "r") as f:
            num_chars = nbits//8 +1
            info_read = f.read(num_chars) if nbits is not None else f.read()
            counter = 0
            for char in info_read:
                print(format(ord(char), "b"))
                for index in range(7,-1,-1):
                   self.bit_array.append(bool((ord(char) >> index) & 1))
                   counter+=1
                   if nbits is not None and counter == nbits:
                       return True
        return False
    
    def write_file(self, file_name, nbits = None):
        if nbits is not None and nbits < 0:
            print("Error: Invalid number of bits, nbits must be positive")
            return False
        if nbits > len(self.bit_array):
            print("Number of bits inputted greater than the number of bits stored")
            return False
        with open(file_name, "wb") as f:
            num_bytes = nbits//8 + 1
            char = 0
            limit = nbits if nbits is not None else len(self.bit_array)
            for counter in range(limit):
                if counter %8 == 0 and counter != 0:
                    f.write(bytes(chr(char), 'utf-8'))
                    char = 0
                char |= int(self.bit_array[counter]) << (7-(counter%8))
            f.write(bytes(chr(char), 'utf-8'))
            return True
        return False

bts = BitStream()
if bts.read_file("../../README.md",16):
    print(bts.bit_array)
if bts.write_file("../../test.bin", 16):
    print("Written successful")