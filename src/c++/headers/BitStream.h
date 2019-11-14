#include <string>

/********************************************/ /**
 * Class containing methods to read and write data from and into an 
 * encoded file.
 ***********************************************/
class BitStream
{
    /********************************************/ /**
    * Function used to load bits from a given file
    *
    * @param file_path The File's path from where we want to get the bits from
    * @param no_bits Number of bits we want to read. By default it's set to NULL, meaning we want to read all the bits from the file
    * @return An array of Booleans representing each bit read
    ***********************************************/
    public:
        bool * read_bits(std::string file_path, int no_bits = NULL);

    /********************************************/ /**
    * Function used to save bits to a given file
    *
    * @param file_path The File's path to which we want to save the bits
    * @param no_bits Number of bits we want to save. By default it's set to NULL, meaning we want to save all the bits from the file
    * @return True in case the operation completed successfully. Else False
    ***********************************************/
    public:
        bool write_bits(std::string file_path, int no_bits = NULL);
};