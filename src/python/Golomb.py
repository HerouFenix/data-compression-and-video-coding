import math
import BitStream

class Golomb:
    def __init__(self,m):
        self.encoding_parameter = m
        self.b_param = math.ceil(math.log2(m))

        self.unary_limit = pow(2, self.b_param) - self.encoding_parameter; #Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    
        self.bit_feed = []

    def encode(self, value):
        code = [True, value<0]
        value = abs(value)

        quotient = value // self.encoding_parameter
        remainder = value % self.encoding_parameter

        code = code + [True] * quotient + [False]   #Encode the quotient - UNARY
        
        for i in range(self.b_param-1, -1, -1):
            code.append(bool((remainder >> i) & 1))
        return code

    def can_decode(self):
        """
        if self.bit_feed == []:
            return False
        
        bit_test = self.bit_feed[1:]
        
        while True:
            if bit_test == []:
                return False
            bit = bit_test.pop(0)
            if not bit:
                break

        return len(bit_test) >= (self.b_param)
        """
        if len(self.bit_feed) < 2:
            return False
        
        bit_test = self.bit_feed[2:]
        
        while True:
            if bit_test == []:
                return False
            bit = bit_test.pop(0)
            if not bit:
                break

        return len(bit_test) >= (self.b_param)


    def add_bits(self, bits):
        self.bit_feed += bits
        return self.can_decode()

    def add_bit(self, bit):
        self.bit_feed.append(bit)
        return self.can_decode()
    
    def decode_nums(self):
        num_array = []
        while self.can_decode():
            if self.bit_feed[0]:
                num_array.append(self.decode(self.bit_feed))
            else:
                self.bit_feed.pop(0)

        return num_array

    def decode(self, code):
        code.pop(0)
        sign_bit = code.pop(0)

        quotient = 0
        remainder = 0

        while True:
            bit = code.pop(0)
            if not bit:
                break
            quotient+=1

        for i in range(self.b_param-1, -1, -1):
            bit = code.pop(0)
            remainder += int(bit) << i

        value = quotient*self.encoding_parameter + remainder
        if(sign_bit):
            value = -value

        return value

def main():
    gomby = Golomb(4) #Kawaii desu-nee?
    bity = BitStream.BitStream()
    
    for i in range(-16, 0):
        testis = gomby.encode(i)
        bity.add_to_bit_array(testis)

    bity.write_allbits("test.bin")

    bity.reset_bit_array()
    bity.clear_padding()
    
    for i in range (16):
        testis = gomby.encode(i)
        bity.add_to_bit_array(testis)
    bity.write_allbits("test.bin")

    bity2 = BitStream.BitStream("test.bin")
    array_of_nums = []
    number_of_numbers = 0
    while bity2.read_bits(20):
        got_number = gomby.add_bits(bity2.get_bit_array())
        bity2.delete_bits(20)

        if got_number:
            nums = gomby.decode_nums()
            array_of_nums += nums
            number_of_numbers += len(nums)
        
    bity2.read_allbits()
    got_number = gomby.add_bits(bity2.get_bit_array())
    nums = gomby.decode_nums()
    array_of_nums += nums
    print(array_of_nums)

if __name__ == "__main__":
    main()
