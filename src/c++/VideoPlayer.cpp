#include "Golomb.cpp"
#include "Frame.cpp"
#include <stdio.h>
#include <string.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <regex>
#include <chrono>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

class VideoPlayer
{
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
    VideoPlayer(string file)
    {
        file_path = file;

        ifstream read;
        read.open(file);
        getline(read, header);
        read.close();

        stringstream ss(header);
        string info;
        frame_type = "420";

        while (getline(ss, info, ' '))
        {
            char c = info.at(0);
            info.replace(0, 1, "");
            switch (c)
            {
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
        VideoCapture cap(file_path);

        while (1)
        {

            Mat frame;
            // Capture frame-by-frame
            cap >> frame;

            // If the frame is empty, break immediately
            if (frame.empty())
                break;

            // Display the resulting frame
            imshow("Frame", frame);

            // Press  ESC on keyboard to exit
            char c = (char)waitKey(25);
            if (c == 27)
                break;
        }

        // When everything done, release the video capture object
        cap.release();

        // Closes all the frames
        destroyAllWindows();

    }

    bool decompress_video(string decompress_path)
    {

        cout << "Starting to decompress\n";
        cout << header << "\n";

        Frame *frame;
        char c = frame_type.at(frame_type.size() - 1);
        if (c == '4')
            frame = new Frame444(height, width);
        if (c == '2')
            frame = new Frame422(height, width);
        if (c == '0')
            frame = new Frame420(height, width);

        Golomb *gomby = new Golomb(gomby_param);

        BitStream *read_stream = new BitStream(file_path);
        read_stream->set_offset(header.size() * 8 + 8);

        ofstream write_stream(decompress_path, ios::binary);
        write_stream << header << "\n";
        write_stream << "FRAME\n";

        int number_of_numbers = 0, counter = 0, counter_bits = 0;
        vector<int> array_of_nums;
        bool got_number;

        while (read_stream->read_bits(5000))
        {
            got_number = gomby->add_bits(read_stream->get_bit_array());
            read_stream->delete_bits(5000);

            if (got_number){
                gomby->decode_nums(&array_of_nums);
                cout << "Have decoded " << array_of_nums.size() << endl;
            }

            if (array_of_nums.size() >= frame->get_limit())
            {
                counter += 1;
                cout << "Decompressing frame: " << counter << "\n";
                frame->set_frame_with_arr(array_of_nums);

                array_of_nums.erase(array_of_nums.begin(), array_of_nums.begin() + frame->get_limit());
                array_of_nums.shrink_to_fit();

                frame->decompress_frame(decompress_mode, counter > 1);
                cout << "Finisheed decompressing frame, now moved on to write\n";

                Mat M = frame->Y_frame();
                M.convertTo(M, CV_8UC1);
                write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));
                
                M = frame->U_frame();
                M.convertTo(M, CV_8UC1);
                write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));

                M = frame->V_frame();
                M.convertTo(M, CV_8UC1);
                write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));

                write_stream << "FRAME\n";

                cout << "Finished compressing frame\n";
            }
        }

        read_stream->read_bits();
        got_number = gomby->add_bits(read_stream->get_bit_array());

        if (got_number)
        {
            gomby->decode_nums(&array_of_nums);

            frame->set_frame_with_arr(array_of_nums);
            frame->decompress_frame(decompress_mode, false);

            Mat M = frame->Y_frame();
            M.convertTo(M, CV_8UC1);
            write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));

            M = frame->U_frame();
            M.convertTo(M, CV_8UC1);
            write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));

            M = frame->V_frame();
            M.convertTo(M, CV_8UC1);
            write_stream.write(M.ptr<char>(0), (M.dataend - M.datastart));
            
        }

        cout << "Finished decompressing frame \n";
        write_stream.close();
    }

    bool compress_video(string compress_path, string mode = "JPEG-1")
    {
        if (!(regex_match(mode, regex("(JPEG-)([1-7])")) || mode.compare("JPEG-LS") == 0))
            return false;

        string buffer;
        Frame *frame;
        char c = frame_type.at(frame_type.size() - 1);
        if (c == '4')
            frame = new Frame444(height, width);
        if (c == '2')
            frame = new Frame422(height, width);
        if (c == '0')
            frame = new Frame420(height, width);

        ifstream stream(file_path, ios::binary);
        getline(stream, buffer);

        Golomb *gomby = new Golomb(4);
        BitStream *bit_stream = new BitStream();

        ofstream writer(compress_path);
        writer << header << " G" << gomby->enconding_parameter() << " M" << mode << "\n";
        writer.close();

        int counter = 0;
        while (counter <= 2)
        {
            counter += 1;
            cout << "Compressing frame " << counter << "\n";
            getline(stream, buffer);

            frame->set_frame(stream);
            frame->compress_frame(mode.at(mode.size() - 1));

            Mat M = frame->Y_frame();
            for (int i = 0; i < M.rows; i++)
                for (int j = 0; j < M.cols; j++)
                    bit_stream->add_to_bit_array(gomby->encode(M.at<int>(i, j)));
            
            M = frame->U_frame();
            for (int i = 0; i < M.rows; i++)
                for (int j = 0; j < M.cols; j++)
                    bit_stream->add_to_bit_array(gomby->encode(M.at<int>(i, j)));
            M = frame->V_frame();
            for (int i = 0; i < M.rows; i++)
                for (int j = 0; j < M.cols; j++)
                    bit_stream->add_to_bit_array(gomby->encode(M.at<int>(i, j)));
            
            bit_stream->write_bits(compress_path);

        }
        bit_stream->close(compress_path); 


        writer.close();
        return true;
    }
  
};

int main()
{
    //VideoPlayer vp("../../tests/vids/ducks_take_off_1080p50.y4m");
    //vp.compress_video("../../tests/vids/ducks_take_off.c4m", "JPEG-1");

    VideoPlayer vp2("../../tests/vids/ducks_take_off.c4m");
    vp2.decompress_video("ducks_take_off_c.y4m");
    cout << "finshed compressing\n";
    
    return 1;

    //VideoPlayer vp("../../tests/vids/ducks_take_off_1080p50.y4m");
    //vp.play_video();
    //cout << vp.compress_video("../../tests/vids/ducks_take_off.c4m", "JPEG-L") << "\n";

    return 0;
}