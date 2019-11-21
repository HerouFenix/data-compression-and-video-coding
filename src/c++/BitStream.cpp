#include <string>
#include <iostream>
#include <exception>
#include <fstream>
#include <iterator>
//#include "headers/BitStream.h"

using namespace std;

class BitStream
{
private:
    bool *bit_array;
    int bit_offset;

    string file_path;
    int file_size;

public:
    BitStream(string fp)
    {
        file_path = fp;

        ifstream loaded_file(file_path, ios::binary | ios::ate);
        file_size = loaded_file.tellg() * 8 + 8;
        loaded_file.close();

        bit_array = new bool[file_size];
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
            cout << "Error. Can't have an offset bigger than the file's size";
            return 0;
        }
        bit_offset = value;
        return 1;
    }

    bool *get_bit_array()
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
    bool read_bits(int no_of_bits, bool use_offset = 1)
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
            cout << "Invalid number of bits. Values must be positive";
            return NULL;
        }

        int bit_counter = 0; //Used to count how many bits we've read
        
        try
        {
            ifstream loaded_file(file_path);

            if (use_offset && bit_offset + no_of_bits > file_size)
            {
                cout << bit_offset << "\n";
                cout << no_of_bits << "\n";
                cout << "Total "<<no_of_bits+bit_offset<<"\n";
                cout << "Error. Operation would cause an overflow (Tried to read more bits than the file has)";
                return 0;
            }
            int initial_offset = bit_offset;
            if (loaded_file.is_open())
            {
                char c;
                while (loaded_file.get(c))
                {
                    for (int i = 7; i >= 0; i--)
                    {
                        if (bit_counter >= no_of_bits + use_offset*initial_offset)
                        {
                            loaded_file.close();
                            return 1;
                        }

                        //Used to advance our file pointer until we catch up with our offset
                        if (use_offset && bit_counter++ < bit_offset)
                        {
                            continue;
                        }
                        cout << "Advancing bit " << bit_counter << "\n";

                        if (use_offset)
                        {
                            bit_array[bit_offset++] = ((c >> i) & 1) == 1; //E.g: 11101010 >> 2 -> 111010 ; 111010 & 1 -> 0 & 1 == 0
                        }
                        else
                        {
                            bit_array[bit_counter++] = ((c >> i) & 1) == 1; //E.g: 11101010 >> 2 -> 111010 ; 111010 & 1 -> 0 & 1 == 0
                        }
                    }
                }

                loaded_file.close();
                return 1;
            }
            else
            {
                cout << "File could not be found";
            }

            loaded_file.close();
        }
        catch (exception &e)
        {
            cout << "An exception occurred when reading from the given file. Exception  " << e.what();
        }

        return 0;
    };

    bool read_bits(bool use_offset = 1)
    {
        /********************************************/ /**
        * Function used to read the entire file (or what's left of it if we have an offset)
        *
        * @param use_offset The value we want to change our offset to
        ***********************************************/

        if (use_offset)
        {
            return read_bits(file_size - bit_offset, use_offset);
        }
        return read_bits(file_size, use_offset);
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
            cout << "Invalid number of bits. Values must be positive";
            return 0;
        }

        try
        {
            ofstream write_file(file_path);

            int remainder = no_of_bits % 8;
            char c = 0;

            //int array_size = distance(begin(bit_array), end(bit_array)); what
            //cout << array_size;

            for (int i = 0; i < no_of_bits; i++)
            {
                bool bit;
                /*if (i >= array_size)
                {
                    cout << "\nout of bounds";
                    bit = 0;
                }
                else
                {*/
                bit = bit_array[i];
                //}

                c |= bit << (7 - i % 8);

                if (i % 8 == 0 && i != 0)
                {
                    write_file.write(&c, 1);
                    c = 0;
                }
            }

            for (int i = remainder; i < 8; i++)
            {
                c |= 0 << (7 - i % 8);
            }
            write_file.write(&c, 1);
            write_file.close();

            return 1;
        }
        catch (exception &e)
        {
            cout << "An exception occurred when reading from the given file. Exception  " << e.what();
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
        return write_bits(file_path, bit_offset);
    }
};

/*
int main()
{
    BitStream *test_stream = new BitStream("../../a_love_story.txt");
    cout << "First read through the 16 bits";
    test_stream->read_bits(16);
    bool *oof = test_stream->get_bit_array();
    cout << "Second read through the 16 bits";
    test_stream->read_bits(16, 0);
    bool *oof_2 = test_stream->get_bit_array();
    cout << "Third read, getting the next 16 bits";
    test_stream->read_bits(16);
    bool *oof_3 = test_stream->get_bit_array();
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