#include <stdio.h>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

class Golomb
{
private:
    int encoding_parameter;
    int unary_limit;
    vector<bool> bit_feed;

public:
    int b_param;
    /* Constructor of the Golomb converter */
    Golomb(int m)
    {
        encoding_parameter = m;
        b_param = ceil(log2(m));

        unary_limit = pow(2, b_param) - encoding_parameter; //Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    }

    vector<bool> encode(int m)
    {
        bool sign = m < 0;
        m = abs(m);

        int quotient = m / encoding_parameter,
            remainder = m % encoding_parameter;

        vector<bool> code;
        int i;

        // Unary code
        code.push_back(sign);
        for (i = 1; i < quotient+1; i++)
        {
            code.push_back(true);
        }
        code.push_back(false); //Start binary code
        
        // Binary Code
        // Coversion of remainder to binary
        for (int j = b_param-1; j >= 0; j--, i++)
        {
            //cout << "index: " << i;
            int k = remainder >> j;
            code.push_back(k & 1);
        }

        return code;
    }

    bool can_decode(){
        if (bit_feed.size() < 1) return false;
        int index = 1;
        bool bit;
        while (true){
            if (index > bit_feed.size()) return false;
            bit = bit_feed.at(index++);
            if (!bit) break;
        }
        return bit_feed.size() - index >= b_param;
    }

    bool add_bits(vector<bool> bits){
        for (auto i = bits.begin(); i!=bits.end(); ++i)
            bit_feed.push_back(*i);

        return can_decode();
    }

    bool add_bit(bool bit){
        bit_feed.push_back(bit);
        return can_decode();
    }

    vector<int> decode_nums(){
        vector<int> num_array;
        while (can_decode())
            num_array.push_back(decode(bit_feed));
        
    }

    int decode(vector<bool> encoded){
        bool sign = encoded.at(0);

        int result, index;
        
        int quotient, remainder;
        result = quotient= remainder= 0;
        index = 1;
        while (1){
            bool bit = encoded.at(index++);
            if (!bit) break;
            quotient++;
        }

        for (int j = b_param; j > 0; j--){
            bool bit = encoded.at(index++);
            remainder += bit << j-1;
        }

        int value = quotient*encoding_parameter + remainder;
        sign ? value = value*-1 : value = value;
        encoded.erase(encoded.begin(), encoded.begin()+index);
        return value;
    }

};

int main()
{
    Golomb *g = new Golomb(5);

    for (int i = -15; i < 16; i++)
    {
        vector<bool> test = g->encode(i);
        cout << "Testing " << i << "\t";
        for (int j = 0; j <= abs(i) / 5 + g->b_param; j++)
        {
            cout << test.at(j);
        }
        cout << "\t";
        cout << "D E C O D I N G - " << g->decode(test) << "\n";
    }
    
    return 0;
}
