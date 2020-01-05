#include <string>
#include <iostream>
#include <exception>
#include <fstream>
#include <iterator>
#include <vector>
//#include "headers/BitStream.h"

using namespace std;

class BitStream
{
private:
    int bit_offset;

    string file_path;
    int file_size;
    vector<bool> bit_array;

public:
    BitStream(string fp)
    {
        file_path = fp;

        ifstream loaded_file(file_path, ios::binary | ios::ate);
        file_size = loaded_file.tellg() * 8 + 8;
        loaded_file.close();

        bit_offset = 0;
    }

    BitStream()
    {
        file_path = "";
        file_size = 0;
        bit_offset = 0;
    }

    /* GETTERS & RESETTERS */
    bool set_offset(int value)
    {
        /********************************************/ /**
        * Function used to set our offset counter to 0
        *
        * @param value The value we want to change our offset to
        ***********************************************/

        if (value > file_size)
        {
            cout << "Error. Can't have an offset bigger than the file's size\n";
            return 0;
        }
        bit_offset = value;
        return 1;
    }

    void delete_bits(int num)
    {
        bit_array.erase(bit_array.begin(), bit_array.begin() + num);
    }

    void reset_bit_array()
    {
        bit_array.clear();
    }

    void add_to_bit_array(vector<bool> array)
    {
        bit_array.insert(bit_array.end(), array.begin(), array.end());
        
    }

    vector<bool> get_bit_array()
    {
        /********************************************/ /**
        * Function used to return our current bit array
        ***********************************************/

        return bit_array;
    }

    int get_file_size()
    {
        /********************************************/ /**
        * Function used to get our current file's size
        ***********************************************/
        return file_size;
    }

    /* READ BITS */
    bool read_bits(int no_of_bits, bool use_offset = true)
    {
        /********************************************/ /**
        * Function used to read n bits from our file. Read values are put into our
        * bit_array
        *
        * @param no_of_bits How many bits we want to read
        * @param use_offset Control variable used to check whether we 
        * want to read from the beggining or starting at our current offset
        ***********************************************/
        //Verify that the number of bits is correct
        if (no_of_bits < 0)
        {
            cout << "Invalid number of bits. Values must be positive\n";
            return NULL;
        }

        int bit_counter = 0; //Used to count how many bits we've read

        try
        {
            ifstream loaded_file(file_path, ifstream::binary);

            if (use_offset && bit_offset + no_of_bits > file_size)
            {
                cout << "Error. Operation would cause an overflow (Tried to read more bits than the file has)\n";
                return 0;
            }
            if (use_offset)
            {
                int num_bytes = bit_offset / 8;
                loaded_file.seekg(num_bytes, ios::beg);
                bit_counter = num_bytes * 8;
            }

            int initial_offset = bit_offset;

            char c;
            while (loaded_file.get(c))
            {   
                
                for (int i = 7; i >= 0; i--)
                {
                    if (bit_counter >= (no_of_bits + use_offset * initial_offset))
                    {
                        loaded_file.close();
                        return 1;
                    }

                    //Used to advance our file pointer until we catch up with our offset
                    if (use_offset && bit_counter++ < bit_offset)
                    {
                        continue;
                    }

                    if (use_offset)
                    {
                        bit_array.push_back(((c >> i) & 1) == 1);
                        bit_offset++; //E.g: 11101010 >> 2 -> 111010 ; 111010 & 1 -> 0 & 1 == 0
                    }
                    else
                    {
                        bit_array.push_back(((c >> i) & 1) == 1); //E.g: 11101010 >> 2 -> 111010 ; 111010 & 1 -> 0 & 1 == 0
                        bit_counter++;
                    }
                }
            }

            loaded_file.close();
            return 1;
        }
        catch (exception &e)
        {
            cout << "An exception occurred when reading from the given file. Exception  " << e.what() << "\n";
        }

        return 0;
    };

    int read_bits(bool use_offset = true)
    {
        /********************************************/ /**
        * Function used to read the entire file (or what's left of it if we have an offset)
        *
        * @param use_offset The value we want to change our offset to
        ***********************************************/

        if (use_offset)
        {
            int bits_to_read = file_size - bit_offset;
            return read_bits(bits_to_read, use_offset) * bits_to_read;
        }
        return read_bits(file_size, use_offset) * file_size;
    }

    /* WRITE BITS */
    bool write_bits(string file_path, int no_of_bits)
    {
        /********************************************/ /**
        * Function used to write our current bit_array into a file
        *
        * @param file_path The name of the file we want to write to
        * @param no_of_bits The amount of bits we want to write
        ***********************************************/

        //Verify that the number of bits is correct
        if (no_of_bits < 0)
        {
            cout << "Invalid number of bits. Values must be positive\n";
            return 0;
        }

        try
        {
            ofstream write_file(file_path, ios_base::app);

            int remainder = no_of_bits % 8;
            char c = 0;

            //int array_size = distance(begin(bit_array), end(bit_array)); what
            //cout << array_size;

            bool bit;

            for (int i = 0; i < no_of_bits - remainder; i++)
            {

                bit = bit_array[i];

                if (i % 8 == 0 && i != 0)
                {
                    write_file << c;
                    c = 0;
                }
                c |= int(bit) << (7 - i % 8);
            }

            delete_bits(no_of_bits - remainder);
            write_file << c; 
            write_file.close();

            return 1;
        }
        catch (exception &e)
        {
            cout << "An exception occurred when reading from the given file. Exception  " << e.what() << "\n";
        }

        return 0;
    };

    bool write_bits(string file_path)
    {
        /********************************************/ /**
        * Function used to write the entirety of our bit_array into a file
        *
        * @param file_path The name of the file we want to write to
        ***********************************************/
        return write_bits(file_path, bit_array.size());
    }

    void close(string file_path)
    {
        ofstream write_file(file_path, ios_base::app);
        char c = 0;
        for (int i = 0; i < bit_array.size(); i++)
        {
            bool bit = bit_array.at(i);
            c |= int(bit) << (7 - i % 8);
        }
        write_file << c;
        write_file.close();
    }
};

/*
int main()
{
    BitStream *test_stream = new BitStream("../../a_love_story.txt");
    cout << "First read through the 16 bits\n";
    test_stream->read_bits(16);
    vector<bool> oof = test_stream->get_bit_array();
    cout << "Second read through the 16 bits\n";
    test_stream->read_bits(16, 0);
    vector<bool> oof_2 = test_stream->get_bit_array();
    cout << "Third read, getting the next 16 bits\n";
    test_stream->read_bits(16);
    vector<bool> oof_3 = test_stream->get_bit_array();
    for (int i = 0; i < 16; i++)
    {
        cout << oof[i];
        cout << oof_2[i];
        cout << oof_3[i] << "\n";
    }

    for (int i = 0; i < 32; i++)
    {
        cout << oof_3[i];
    }    
    cout << "\n";

    test_stream->write_bits("../../a_poop_story.txt", 16);

    test_stream->write_bits("../../a_poop_story_2.txt");

}
*/