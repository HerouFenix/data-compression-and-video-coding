#include <stdio.h>
#include <string>
#include <iostream>
#include <exception>
#include <fstream>
#include <opencv2/opencv.hpp>
using namespace std;

class VideoCodec
{
private:
    string file_path;
    int height;
    int width;
public:
    VideoCodec(string fp){
        file_path = fp;
        ifstream loaded_file(file_path);
        string line;
        getline(loaded_file, line);
        char type[10], smth[20];
        int succ = sscanf(line.c_str(), "%s W%d H%d %s\n", type, &width, &height, smth);
    };

    void play_video(){
        
    }

};

int main(int argc, char** argv )
{
    if ( argc != 2 )
    {
        printf("usage: VideoCodec.out <Video_Path>\n");
        return -1;
    }
    
    VideoCodec* vc = new VideoCodec(argv[1]);
    
    return 0;
}