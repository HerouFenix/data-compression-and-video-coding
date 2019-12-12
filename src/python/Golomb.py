import math

class Golomb:
    def __init__(self,m):
        self.encoding_parameter = m
        self.b_param = math.ceil(math.log2(m))

        self.unary_limit = pow(2, self.b_param) - self.encoding_parameter; #Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    
    def encode(self, value):
        quotient = value // self.encoding_parameter
        remainder = value % self.encoding_parameter

        code = [True] * quotient + [False]
        
        for i in range(self.b_param-1, -1, -1):
            code.append(bool((remainder >> i) & 1))
        return code

    def decode(self, code):

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

        return quotient*self.encoding_parameter + remainder

def main():
    gomby = Golomb(2) #Kawaii desu-nee?
    
    for i in range(16):
        testis = gomby.encode(i)
        print("Testing",i, "\t", end="")
        for j in range(i//5+gomby.b_param+1):
            print(int(testis[j]), end="")
        print(" D E C O D I N G - ", gomby.decode(testis),"\n")
    

if __name__ == "__main__":
    main()
