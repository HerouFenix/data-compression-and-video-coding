#include <string>
#include <iostream>
#include <exception>
#include <fstream>
#include <iterator>
//#include "headers/BitStream.h"

using namespace std;

class BitStream
{
public:
    bool *read_bits(string file_path, int no_of_bits)
    {
        //Verify that the number of bits is correct
        if (no_of_bits < 0)
        {
            cout << "Invalid number of bits. Values must be positive";
            return NULL;
        }

        bool *bit_array = new bool[no_of_bits]; //Initialize bit array

        int bit_counter = 0; //Used to count how many bits we've read

        try
        {
            ifstream loaded_file(file_path);
            string line;

            if (loaded_file.is_open())
            {
                char c;
                while (loaded_file.get(c))
                {
                    for (int i = 7; i >= 0; i--)
                    {
                        if (bit_counter >= no_of_bits)
                        {
                            loaded_file.close();
                            return bit_array;
                        }
                        bit_array[bit_counter++] = ((c >> i) & 1) == 1; //E.g: 11101010 >> 2 -> 111010 ; 111010 & 1 -> 0 & 1 == 0
                    }
                }

                loaded_file.close();
                return bit_array;
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

        return NULL;
    };

    bool *read_bits(string file_path)
    {
        try
        {
            ifstream loaded_file(file_path, ios::binary | ios::ate);
            int file_size = loaded_file.tellg() * 8 + 8;
            loaded_file.close();

            return read_bits(file_path, file_size);
        }
        catch (exception &e)
        {
            cout << "An exception occurred when reading from the given file. Exception  " << e.what();
        }

        return NULL;
    }

    bool write_bits(string file_path, bool *bit_array, int no_of_bits)
    {
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

            for (int i = remainder; i <8; i++)
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
};

int main()
{
    BitStream *test_stream = new BitStream();
    bool *oof = test_stream->read_bits("../../a_love_story.txt", 16);
    for (int i = 0; i < 10; i++)
    {
        cout << oof[i];
    }

    bool oof_tsts = test_stream->write_bits("../../a_poop_story", oof, 14);

    cout << "\n"
         << oof_tsts;

    cout << "\n";

    oof = test_stream->read_bits("../../a_love_story.txt");

    for (int i = 0; i < 57 * 8; i++)
    {
        cout << oof[i];
    }

    cout << "\n";
}