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
        int quotient = m / encoding_parameter,
            remainder = m % encoding_parameter;

        int code_size, remainder_bin_size;
        if (remainder < unary_limit)
        {
            code_size = quotient + b_param;
            remainder_bin_size = b_param - 1; // Binary codewords of b−1 bits.
        }
        else
        {
            code_size = quotient + 1 + b_param;
            remainder = remainder + unary_limit; //Encode the remainder values of r by coding the number r+2b−m in binary codewords of b bits.

            remainder_bin_size = b_param; // Binary codewords of b bits
        } 

        bool *code = new bool[code_size];
        int i;

        // Unary code
        for (i = 0; i < quotient; i++)
        {
            code[i] = (bool)1;
        }
        code[i++] = (bool)(0); //Start binary code
        
        // Binary Code
        // Coversion of remainder to binary
        for (int j = remainder_bin_size-1; j >= 0; j--, i++)
        {
            //cout << "index: " << i;
            int k = remainder >> j;
            code[i] = k & 1;
        }

        return code;
    }


    int decode(bool* bits)
    {
        int number = 0, 
            quocient = 0,
            index = 0;

        bool current_bit;

        //Get Quotient
        while(true){
            current_bit = bits[index++];

            if(!current_bit){   //Means we stopped counting the quotient
                number = quocient * encoding_parameter;
                break;
            }

            quocient++;
        }

        //Get remainder
        // If the first 'remainder bit' is 0 -> Remainder < b_parameter -> We only want the first b_param - 1 bits
        int read_bits = b_param;
        if(current_bit = bits[index] == 0){
            read_bits = b_param - 1;
        }

        int control = 0;

        for (int i = 0; i < read_bits; i++){
            current_bit = bits[index++];
            if (!current_bit){
                control += 1;
            }
            
        }
        
        return number;
    }
    /* GETTERS & SETTERS */

};

int main()
{
    Golomb *g = new Golomb(5);

    for (int i = 0; i < 16; i++)
    {
        bool *test = g->encode(i);
        cout << "Testing " << i << "\t";
        for (int j = 0; j <= i / 5 + g->b_param; j++)
        {
            cout << test[j];
        }
        cout << "\n";
        cout << "D E C O D I N G - " << g->decode(test) << "\n";
    }
    

    return 0;
}
