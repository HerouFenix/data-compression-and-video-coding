#include <opencv2/core/mat.hpp>
#include <opencv2/core.hpp>
#include <math.h>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Frame
{
protected:
    int height;
    int limit_to_convert;
    int width;
    cv::Mat Y;
    cv::Mat U;
    cv::Mat V;

public:
    Frame(int h, int w)
    {
        height = h;
        width = w;
    }

    virtual void set_frame(ifstream &stream) = 0;

    virtual void set_frame_with_arr(vector<int> stream) = 0;

    cv::Mat Y_frame()
    {
        return Y;
    }

    cv::Mat U_frame()
    {
        return U;
    }

    cv::Mat V_frame()
    {
        return V;
    }

    int predictor(char mode, int a, int b, int c)
    {
        if (mode == '1')
            return a;
        if (mode == '2')
            return b;
        if (mode == '3')
            return c;
        if (mode == '4')
            return a + b - c;
        if (mode == '5')
            return a + (b - c) / 2;
        if (mode == '6')
            return b + (a - c) / 2;
        if (mode == '7')
            return (a + b) / 2;

        //JPEG LS
        if (c >= max(a, b))
            return min(a, b);
        if (c <= min(a, b))
            return max(a, b);
        return a + b - c;
    }

    void compress_frame(char mode)
    {
        cout << mode << endl;
        bool u_skip = Y.rows != U.rows;
        bool v_skip = Y.rows != V.rows;

        int predictor_y, predictor_u, predictor_v;

        for (int i = height - 1; i >= 0; i--)
        {
            for (int j = width - 1; j >= 0; j--)
            {
                if (mode == '1')
                {
                    if (j > 0)
                    {
                        predictor_y = Y.at<int>(i, j - 1);
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = U.at<int>(i, j - 1);
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = V.at<int>(i, j - 1);
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }
                else if (mode == '2')
                {
                    if (i > 0)
                    {
                        predictor_y = Y.at<int>(i - 1, j);
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = U.at<int>(i - 1, j);
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = V.at<int>(i - 1, j);
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }
                else
                {
                    if (i > 0 && j > 0)
                    {
                        predictor_y = predictor(mode, Y.at<int>(i, j - 1), Y.at<int>(i - 1, j), Y.at<int>(i - 1, j - 1));
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = predictor(mode, U.at<int>(i, j - 1), U.at<int>(i - 1, j), U.at<int>(i - 1, j - 1));
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = predictor(mode, V.at<int>(i, j - 1), V.at<int>(i - 1, j), V.at<int>(i - 1, j - 1));
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }

                Y.at<int>(i, j) -= predictor_y;
                if (!u_skip || ((j < U.cols) && (i < U.rows)))
                    U.at<int>(i, j) -= predictor_u;
                if (!v_skip || ((j < V.cols) && (i < V.rows)))
                    V.at<int>(i, j) -= predictor_v;
            }
        }
    }

    void decompress_frame(char mode)
    {
        bool u_skip = Y.rows != U.rows;
        bool v_skip = Y.rows != V.rows;

        int predictor_y, predictor_u, predictor_v;
        cout << "starting decompression process\n";
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {

                if (mode == '1')
                {
                    if (j > 0)
                    {
                        predictor_y = Y.at<int>(i, j - 1);
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = U.at<int>(i, j - 1);
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = V.at<int>(i, j - 1);
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }
                else if (mode == '2')
                {
                    if (i > 0)
                    {
                        predictor_y = Y.at<int>(i - 1, j);
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = U.at<int>(i - 1, j);
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = V.at<int>(i - 1, j);
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }
                else
                {
                    if (i > 0 && j > 0)
                    {
                        predictor_y = predictor(mode, Y.at<int>(i, j - 1), Y.at<int>(i - 1, j), Y.at<int>(i - 1, j - 1));
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = predictor(mode, U.at<int>(i, j - 1), U.at<int>(i - 1, j), U.at<int>(i - 1, j - 1));
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = predictor(mode, V.at<int>(i, j - 1), V.at<int>(i - 1, j), V.at<int>(i - 1, j - 1));
                    }
                    else
                    {
                        predictor_y = 0;
                        if (!u_skip || ((j < U.cols) && (i < U.rows)))
                            predictor_u = 0;
                        if (!v_skip || ((j < V.cols) && (i < V.rows)))
                            predictor_v = 0;
                    }
                }

                Y.at<int>(i, j) += predictor_y;
                if (!u_skip || ((j < U.cols) && (i < U.rows)))
                    U.at<int>(i, j) += predictor_u;
                if (!v_skip || ((j < V.cols) && (i < V.rows)))
                    V.at<int>(i, j) += predictor_v;
            }
        }
    }
    /*
    virtual cv::Mat show_frame()
    {
        float M_data[9] = {1, 1.172, 0, 1, -0.344, -0.714, 1, 0, 1.402};
        cv::Mat M = cv::Mat(3, 3, CV_32F, M_data);

        vector<Mat> channels;
        channels.push_back(Y);
        channels.push_back(U);
        channels.push_back(V);
        merge(channels, YUV);

        int sz[] = {height, width};
        cv::Mat BGR(2, sz, CV_32SC1C3);
        int y_value, u_value, v_value;
        int b_value, g_value, r_value;
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                y_value = Y.at<int>(i, j) - 16;
                u_value = U.at<unsigned char>(i, j) - 128;
                v_value = V.at<unsigned char>(i, j) - 128;
                
                b_value = y_value + u_value*1.172;
                if (b_value<=0) b_value = 0;
                if (b_value>255) b_value = 255;

                g_value = y_value - u_value*0.344 - 0.714*v_value;
                if (g_value <= 0) g_value = 0;
                if (g_value > 255) g_value = 255;

                r_value = y_value +1.402*v_value;
                if (r_value <= 0) r_value = 0;
                if (r_value > 255) r_value = 255;

                BGR.at<unsigned char>(i, j, 0) = b_value;
                BGR.at<unsigned char>(i, j, 1) = g_value;
                BGR.at<unsigned char>(i, j, 2) = r_value;
                
            }
        }
        
        return BGR;
    }*/

    int get_limit()
    {
        return limit_to_convert;
    }
};

class Frame444 : public Frame
{
public:
    Frame444(int h, int w) : Frame(h, w)
    {
        limit_to_convert = h * w * 3;
    }

    void set_frame(ifstream &stream)
    {
        int y_data[height * width], u_data[height * width], v_data[height * width];
        for (int i = 0; i < height * width; i++)
            y_data[i] = int((unsigned char)stream.get());
        Y = cv::Mat(height, width, CV_32SC1, y_data);
        for (int i = 0; i < height * width; i++)
            u_data[i] = int((unsigned char)stream.get());
        U = cv::Mat(height, width, CV_32SC1, u_data);

        for (int i = 0; i < height * width; i++)
            v_data[i] = int((unsigned char)stream.get());
        V = cv::Mat(height, width, CV_32SC1, v_data);
    }

    void set_frame_with_arr(vector<int> stream)
    {
        vector<int> y_data(stream.begin(), stream.begin() + height * width);
        vector<int> u_data(stream.begin() + height * width, stream.begin() + 2 * height * width);
        vector<int> v_data(stream.begin() + 2 * height * width, stream.begin() + 3 * height * width);

        Y = cv::Mat(height, width, CV_32SC1, y_data.data());
        U = cv::Mat(height, width, CV_32SC1, u_data.data());
        V = cv::Mat(height, width, CV_32SC1, v_data.data());
    }
};

class Frame422 : public Frame
{
public:
    Frame422(int h, int w) : Frame(h, w)
    {
        limit_to_convert = h * w * 2 + (h / 2) * (w / 2);
    }

    void set_frame(ifstream &stream)
    {
        int y_data[height * width], u_data[height * width], v_data[height / 2 * width / 2];
        cout << "getting frame422 from stream \n";
        for (int i = 0; i < height * width; i++)
            y_data[i] = int((unsigned char)stream.get());
        Y = cv::Mat(height, width, CV_32SC1, y_data);
        for (int i = 0; i < height * width; i++)
            u_data[i] = int((unsigned char)stream.get());
        U = cv::Mat(height, width, CV_32SC1, u_data);

        for (int i = 0; i < height / 2 * width / 2; i++)
            v_data[i] = int((unsigned char)stream.get());
        V = cv::Mat(height / 2, width / 2, CV_32SC1, v_data);
    }

    void set_frame_with_arr(vector<int> stream)
    {
        vector<int> y_data(stream.begin(), stream.begin() + height * width);
        vector<int> u_data(stream.begin() + height * width, stream.begin() + 2 * height * width);
        vector<int> v_data(stream.begin() + 2 * height * width, stream.begin() + limit_to_convert);

        Y = cv::Mat(height, width, CV_32SC1, y_data.data());
        U = cv::Mat(height, width, CV_32SC1, u_data.data());
        V = cv::Mat(height / 2, width / 2, CV_32SC1, v_data.data());
    }
    /*
    cv::Mat show_frame()
    {
        V = cv::repeat(V, 2, 2);
        return Frame::show_frame();
    }*/
};

class Frame420 : public Frame
{
public:
    Frame420(int h, int w) : Frame(h, w)
    {
        limit_to_convert = h * w + (h / 2) * (w / 2) * 2;
    }

    void set_frame(ifstream &stream)
    {
        cout << "about to make some arrays\n";
        int *y_data = new int[height * width];
        int *u_data = new int[height / 2 * width / 2];
        int *v_data = new int[height / 2 * width / 2];
        cout << "getting frame420 from stream \n";
        int i;
        for (i = 0; i < height * width; i++)
            y_data[i] = int((unsigned char)stream.get());

        Y = cv::Mat(height, width, CV_32SC1, y_data);

        for (i = 0; i < height / 2 * width / 2; i++)
            u_data[i] = int((unsigned char)stream.get());
        U = cv::Mat(height / 2, width / 2, CV_32SC1, u_data);

        for (i = 0; i < height / 2 * width / 2; i++)
            v_data[i] = int((unsigned char)stream.get());
        V = cv::Mat(height / 2, width / 2, CV_32SC1, v_data);
    }

    void set_frame_with_arr(vector<int> stream)
    {
        vector<int> y_data(stream.begin(), stream.begin() + height * width);
        vector<int> u_data(stream.begin() + height * width, stream.begin() + height * width + height / 2 * width / 2);
        vector<int> v_data(stream.begin() + height * width + height / 2 * width / 2, stream.begin() + limit_to_convert);

        Y = cv::Mat(height, width, CV_32SC1, y_data.data());
        U = cv::Mat(height / 2, width / 2, CV_32SC1, u_data.data());
        V = cv::Mat(height / 2, width / 2, CV_32SC1, v_data.data());

    }
    /*

    cv::Mat show_frame()
    {
        U = cv::repeat(U, 2, 2);
        V = cv::repeat(V, 2, 2);
        
        return Frame::show_frame();
    }*/
};