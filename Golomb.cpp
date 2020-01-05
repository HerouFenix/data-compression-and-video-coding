#include <stdio.h>
#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>
#include "BitStream.cpp"

using namespace std;

class Golomb
{
private:
    int encoding_parameter;
    int b_param;
    int unary_limit;
    vector<bool> bit_feed;

public:
    /* Constructor of the Golomb converter */
    Golomb(int m)
    {
        encoding_parameter = m;
        b_param = ceil(log2(m));

        unary_limit = pow(2, b_param) - encoding_parameter; //Encode the first 2b−m values of r using the first 2b−m binary codewords of b−1 bits
    }

    int enconding_parameter()
    {
        return encoding_parameter;
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
        for (i = 1; i < quotient + 1; i++)
        {
            code.push_back(true);
        }
        code.push_back(false); //Start binary code

        // Binary Code
        // Coversion of remainder to binary
        for (int j = b_param - 1; j >= 0; j--, i++)
        {
            int k = remainder >> j;
            code.push_back(k & 1);
        }

        return code;
    }

    bool can_decode()
    {
        if (bit_feed.size() < 1)
            return false;
        vector<bool>::iterator it = find(bit_feed.begin() + 1, bit_feed.end(), false);

        if (it == bit_feed.end())
            return false;

        return distance(it, bit_feed.end()) > b_param;
    }

    bool add_bits(vector<bool> bits)
    {
        bit_feed.insert(bit_feed.end(), bits.begin(), bits.end());

        return can_decode();
    }

    bool add_bit(bool bit)
    {
        bit_feed.push_back(bit);
        return can_decode();
    }

    vector<int> decode_nums()
    {
        vector<int> num_array;

        while (can_decode())
            num_array.push_back(decode());
        return num_array;
    }

    int decode()
    {
        bool bit;
        bool sign = bit_feed.at(0);

        int quotient, remainder, index;
        quotient = remainder = 0;
        index = 1;
        while (1)
        {
            bit = bit_feed.at(index++);
            if (!bit)
                break;
            quotient++;
        }

        for (int j = b_param; j > 0; j--)
        {
            bit = bit_feed.at(index++);
            remainder += bit << j - 1;
        }

        int value = quotient * encoding_parameter + remainder;
        sign ? value = value *-1 : value = value;

        bit_feed.erase(bit_feed.begin(), bit_feed.begin() + index);
        return value;
    }

    int decode(vector<bool> encoded)
    {
        bool sign = encoded.at(0);

        int quotient, remainder, index;
        quotient = remainder = 0;
        index = 1;
        while (1)
        {
            bool bit = encoded.at(index++);
            if (!bit)
                break;
            quotient++;
        }

        for (int j = b_param; j > 0; j--)
        {
            bool bit = encoded.at(index++);
            remainder += bit << j - 1;
        }

        int value = quotient * encoding_parameter + remainder;
        sign ? value = value *-1 : value = value;
        encoded.erase(encoded.begin(), encoded.begin() + index);

        return value;
    }
};
/*
int main()
{
    Golomb *gomby = new Golomb(4);
    BitStream *bity = new BitStream();

    ofstream write_file("test.bin");
    write_file << "";
    write_file.close(); 

    for (int i = -16; i < 0; i++){
        vector<bool> testis = gomby->encode(i);
        bity->add_to_bit_array(testis);
    }

    bity->write_bits("test.bin");

    for (int i = 0; i < 16; i++){
        vector<bool> testis = gomby->encode(i);
        bity->add_to_bit_array(testis);
    }
    bity->write_bits("test.bin");
    bity->close("test.bin");
    
    BitStream *bity2 = new BitStream("test.bin");
    vector<int> array_of_nums;
    int number_of_numbers = 0;
    vector<int> nums;
    bool got_number;

    while (bity2->read_bits(20)){

        got_number = gomby->add_bits(bity2->get_bit_array());

        bity2->delete_bits(20);
        
        if (got_number) {
            nums = gomby->decode_nums();
            for (auto i = nums.begin(); i!=nums.end(); ++i){
                array_of_nums.push_back(*i);
                number_of_numbers++;
            }
        }   
    }

    bity2->read_bits();
    got_number = gomby->add_bits(bity2->get_bit_array());
    nums = gomby->decode_nums();
    for (auto i = nums.begin(); i!=nums.end(); ++i)
        array_of_nums.push_back(*i);
    
    for (auto i = array_of_nums.begin(); i != array_of_nums.end(); i++){
        cout << *i <<",";
    }

    cout << "\n";
    return 0;
}*/