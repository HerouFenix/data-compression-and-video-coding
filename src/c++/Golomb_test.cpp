#include <chrono>
#include <stdio.h>
#include <iostream>
#include "Golomb.cpp"

int main()
{
    Golomb *gomby = new Golomb(4);
    BitStream *bity = new BitStream();

    ofstream write_file("test.bin");
    write_file << "";
    write_file.close();

    for (int i = -16; i < 0; i++)
    {
        vector<bool> testis = gomby->encode(i);
        bity->add_to_bit_array(testis);
    }

    bity->write_bits("test.bin");

    for (int i = 0; i < 16; i++)
    {
        vector<bool> testis = gomby->encode(i);
        bity->add_to_bit_array(testis);
    }
    bity->write_bits("test.bin");
    bity->close("test.bin");

    chrono::steady_clock::time_point begin = chrono::steady_clock::now();

    BitStream *bity2 = new BitStream("test.bin");
    vector<int> array_of_nums;
    int number_of_numbers = 0;
    vector<int> nums;
    bool got_number;

    while (bity2->read_bits(20))
    {

        got_number = gomby->add_bits(bity2->get_bit_array());

        bity2->delete_bits(20);

        if (got_number)
        {
            gomby->decode_nums(&array_of_nums);
        }
    }

    bity2->read_bits();
    got_number = gomby->add_bits(bity2->get_bit_array());
    gomby->decode_nums(&array_of_nums);

    chrono::steady_clock::time_point end = chrono::steady_clock::now();

    cout << "Time difference = " << chrono::duration_cast<chrono::microseconds>(end - begin).count() << "[µs]\n";

    for (auto i = array_of_nums.begin(); i != array_of_nums.end(); i++)
    {
        cout << *i << ",";
    }

    cout << "\n";

    return 0;
}