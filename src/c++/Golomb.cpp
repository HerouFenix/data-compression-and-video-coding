#include <stdio.h>
#include <iostream>
#include <math.h>

using namespace std;

class Golomb
{
public:
    int encoding_parameter;
    int b_param;
    int unary_limit;

public:
    /* Constructor of the Golomb converter */
    Golomb(int m)
    {
        encoding_parameter = m;
        b_param = ceil(log2(m));

        unary_limit = pow(2, b_param) - encoding_parameter; //Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    }

    bool *encode(int m)
    {
        bool sign;
        m < 0 ? sign = true : false;
        m = abs(m);

        int quotient = m / encoding_parameter,
            remainder = m % encoding_parameter;

        bool *code = new bool[quotient + 1 + b_param + 1];
        int i;

        // Unary code
        code[0] = sign;
        for (i = 1; i < quotient+1; i++)
        {
            code[i] = (bool)1;
        }
        code[i++] = (bool)(0); //Start binary code
        
        // Binary Code
        // Coversion of remainder to binary
        for (int j = b_param-1; j >= 0; j--, i++)
        {
            //cout << "index: " << i;
            int k = remainder >> j;
            code[i] = k & 1;
        }

        return code;
    }

    int decode(bool* encoded){
        bool sign = encoded[0];

        int result, index;
        
        int quotient, remainder;
        result = quotient= remainder= 0;
        index = 1;
        while (1){
            bool bit = encoded[index++];
            if (!bit) break;
            quotient++;
        }

        for (int j = b_param; j > 0; j--){
            bool bit = encoded[index++];
            remainder += bit << j-1;
        }

        int value = quotient*encoding_parameter + remainder;
        sign ? value = value*-1 : value = value;

        return value;
    }

};

int main()
{
    Golomb *g = new Golomb(5);

    for (int i = -15; i < 16; i++)
    {
        bool *test = g->encode(i);
        cout << "Testing " << i << "\t";
        for (int j = 0; j <= abs(i) / 5 + g->b_param; j++)
        {
            cout << test[j];
        }
        cout << "\t";
        cout << "D E C O D I N G - " << g->decode(test) << "\n";
    }
    

    return 0;
}
