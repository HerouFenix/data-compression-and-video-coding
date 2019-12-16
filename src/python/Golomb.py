import math

class Golomb:
    def __init__(self,m):
        self.encoding_parameter = m
        self.b_param = math.ceil(math.log2(m))

        self.unary_limit = pow(2, self.b_param) - self.encoding_parameter; #Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    
        self.bit_feed = []

    def encode(self, value):
        code = [value<0]
        value = abs(value)

        quotient = value // self.encoding_parameter
        remainder = value % self.encoding_parameter

        code = code + [True] * quotient + [False]
        
        for i in range(self.b_param-1, -1, -1):
            code.append(bool((remainder >> i) & 1))
        return code

    def can_decode(self):
        if self.bit_feed == []:
            return False
        
        bit_test = self.bit_feed[1:]
        
        while True:
            if bit_test == []:
                return False
            bit = bit_test.pop(0)
            if not bit:
                break

        return len(bit_test) >= (self.b_param +1)

    def add_bits(self, bits):
        self.bit_feed += bits
        return self.can_decode

    def add_bit(self, bit):
        self.bit_feed.append(bit)
        return self.can_decode()
    
    def decode_nums(self):
        num_array = []
        while self.can_decode():
            num_array.append(self.decode(self.bit_feed))

        return num_array

    def decode(self, code):
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
    gomby = Golomb(5) #Kawaii desu-nee?

    for i in range(-16, 16):
        testis = gomby.encode(i)
        print("Testing",i, "\t", end="")
        for j in range(abs(i)//5+gomby.b_param+2):
            print(int(testis[j]), end="")
        print("  D E C O D I N G - ", gomby.decode(testis),"\n")
    

if __name__ == "__main__":
    main()
