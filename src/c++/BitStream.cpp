#include <string>
#include <iostream>
#include <exception>
#include <fstream>
//#include "headers/BitStream.h"

using namespace std;

class BitStream
{
    public:
        bool * read_bits(string file_path, int no_bits = NULL){
            try{
                ifstream loaded_file(file_path);
                string line;

                if (loaded_file.is_open()){

                    while (getline (loaded_file,line)){
                        cout << line << '\n';
                    }
                }
                else{
                    cout << "File could not be found";
                }

                loaded_file.close();

            }catch(exception& e){
                cout << "An exception occurred when reading from the given file. Exception  " << e.what();
            }

            return NULL;
        };

    
    public:
        bool write_bits(std::string file_path, int no_bits = NULL){
            return 0;
        };
};


int main(){
    BitStream* test_stream = new BitStream();
    test_stream->read_bits("../../a_love_story.txt");
}