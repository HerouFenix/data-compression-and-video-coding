#include "Golomb.cpp"
#include "Frame.cpp"
#include <stdio.h>
#include <string.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace std;
using namespace cv;

class VideoPlayer{
    private:
        string file_path;
        string header;
        int width;
        int height;
        string fps;
        string frame_type;
        char decompress_mode;
        int gomby_param;

    public:
        VideoPlayer(string file){
            file_path = file;

            ifstream read;
            read.open(file);
            getline(read, header);
            read.close();

            stringstream ss(header);
            string info;
            frame_type = "420";

            while (getline(ss, info, ' ')){
                char c = info.at(0);
                info.replace(0, 1, "");
                switch(c){
                    case 'W':
                        width = stoi(info);
                        break;
                    case 'H':
                        height = stoi(info);
                        break;
                    case 'F':
                        fps = string(info);
                        break;
                    case 'C':
                        frame_type = info.substr(0, 3);
                        break;
                    case 'G':
                        gomby_param = stoi(info);
                        break;
                    case 'M':
                        decompress_mode = info.at(info.size() - 1);
                }
            }

        }

    void play_video(){
        string buffer;
        Frame *frame;
        char c = frame_type.at(frame_type.size() -1 );
        if (c== '4') frame = new Frame444(height, width);
        if (c== '2') frame = new Frame422(height, width);
        if (c== '0') frame = new Frame420(height, width);

        ifstream stream(file_path, ios::binary);
        getline(stream, buffer);
        while (true){
            try{
                getline(stream, buffer);
                frame->set_frame(stream);
                namedWindow( "Display window" );
                imshow("Display window", frame->show_frame());
            }
            catch (exception e){
                cout << e.what() << "\n";
            }
        }
        stream.close();
    }

};

int main(){
    VideoPlayer vp("../../tests/vids/ducks_take_off_1080p50.y4m");
    return 0;
}