import os

class BitStream:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if file_path is not None:
            self.file_size = os.path.getsize(self.file_path)*8
        else:
            self.file_size = 0

        self.bit_array = []

        self.bit_offset = 0

    # GETTERS & RESETTERS #
    def set_offset(self, value):
        """
        # Function used to set our offset counter to a given value
        #
        # @param value The value we want to change our offset to
        """

        if value > self.file_size:
            print("Error. Can't have an offset bigger than the file's size\n")
            return 0

        self.bit_offset = value
        return 1
    
    def reset_bit_array(self):
        self.bit_array=[]
    
    def add_to_bit_array(self, array):
        self.bit_array += array

    def get_bit_array(self):
        """
        # Function used to return our current bit array
        """
        return self.bit_array

    def get_file_size(self):
        """
        # Function used to get our current file's size
        """
        return self.file_size

    # READ BITS #
    def read_bits(self, no_of_bits, use_offset=True):
        """
        # Function used to read n bits from our file. Read values are put into our
        # bit_array
        #
        # @param no_of_bits How many bits we want to read
        # @param use_offset Control variable used to check whether we
        # want to read from the beggining or starting at our current offset
        """

        # Verify that the number of bits is correct
        if no_of_bits < 0:
            print("Invalid number of bits. Values must be positive\n")
            return None

        bit_counter = 0  # Used to count how many bits we've read

        try:
            with open(self.file_path, "rb") as loaded_file:
                if (use_offset and self.bit_offset + no_of_bits > self.file_size):
                    print(
                        "Error. Operation would cause an overflow (Tried to read more bits than the file has)\n")
                    return 0

                initial_offset = self.bit_offset
                for control in range(self.file_size//8):

                    byte = ord(loaded_file.read(1))

                    for i in range(7, -1, -1):
                        if bit_counter >= no_of_bits + int(use_offset)*initial_offset:
                            return 1

                        # Used to advance our file pointer until we catch up with our offset
                        bit_counter +=1
                        if use_offset and bit_counter <= self.bit_offset:
                            continue

                        if use_offset:
                            # E.g: 11101010 >> 2 -> 111010 111010 & 1 -> 0 & 1 == 0
                            self.bit_array.append(((byte >> i) & 1) == 1)
                            self.bit_offset += 1
                        else:
                            # E.g: 11101010 >> 2 -> 111010 111010 & 1 -> 0 & 1 == 0
                            self.bit_array[bit_counter-1] = ((byte >> i) & 1) == 1
            return 1

        except Exception as e:
            print(
                "An exception occurred when reading from the given file. Exception  ", e, "\n")

        return 0

    def read_allbits(self,use_offset=True):
        """
        # Function used to read the entire file(or what's left of it if we have an offset)
        #
        # @param use_offset The value we want to change our offset to
        """

        if (use_offset):
            return self.read_bits(self.file_size - self.bit_offset, use_offset)
        return self.read_bits(self.file_size, use_offset)

    # WRITE BITS #
    def write_bits(self,file_path, no_of_bits):
        """
        # Function used to write our current bit_array into a file
        #
        # @param file_path The name of the file we want to write to
        # @param no_of_bits The amount of bits we want to write
        """

        # Verify that the number of bits is correct
        if (no_of_bits < 0):
            print("Invalid number of bits. Values must be positive\n")
            return 0

        try:
            with open(file_path, "wb") as file_writer:
                remainder = no_of_bits % 8
                bitstream = 0 

                for i in range(no_of_bits):
                    bit = self.bit_array[i]
                    bitstream |= int(bit) << (7 - i % 8)

                    if i % 8 == 0 and i != 0:
                        file_writer.write(bitstream.to_bytes(1,"little"))
                        bitstream = 0

                if (remainder != 0):
                    for i in range (remainder, 8):
                        bitstream |= 0 << (7 - i % 8)

                file_writer.write(bitstream.to_bytes(1,"little"))
            return 1
        except Exception as e:
            print(
                "An exception occurred when reading from the given file. Exception  ", e, "\n")

        return 0

    def write_allbits(self,file_path):
        """
        # Function used to write the entirety of our bit_array into a file
        #
        # @param file_path The name of the file we want to write to
        """
        return self.write_bits(file_path, len(self.bit_array))



def main():
    test_stream = BitStream("../../a_love_story.txt")
    print("First read through the 16 bits\n")

    test_stream.read_bits(16)
    oof = test_stream.get_bit_array()
    print("Second read through the 16 bits\n")

    test_stream.read_bits(16, False)
    oof_2 = test_stream.get_bit_array()
    print("Third read, getting the next 16 bits\n")

    test_stream.read_bits(16)
    oof_3 = test_stream.get_bit_array()

    for i in range(len(oof)):
        print(int(oof[i]))
        print(int(oof_2[i]))
        print(int(oof_3[i]))

    for i in oof_3:
        print(int(i), end="")
    print()
    print(len(oof_3))

    test_stream.write_bits("../../tests/txt/a_poop_story.txt", 16)

    test_stream.write_allbits("../../tests/txt/a_poop_story_2.txt")

if __name__ == "__main__":
    main()
