#include <stdio.h>
#include <iostream>
#include <math.h>
#include <opencv2/opencv.hpp>
#include <opencv2/core/mat.hpp>

using namespace cv;

class Frame
{
public:
    int height;
    int width;
    Mat YUV;

    Mat Y;
    Mat U;
    Mat V;

public:
    Frame(int height, int width)
    {
        this->height = height;
        this->width = width;
        this->YUV = nullptr;

        this->Y = nullptr;
        this->U = nullptr;
        this->V = nullptr;
    }

    Mat show_frame()
    {
        if (this->YUV == nullptr)
        {
            return nullptr;
        }

        cvSubS(this->Y, 16, this->Y);
        cvSubS(this->U, 128, this->U);
        cvSubS(this->V, 128, this->V);
    }
};
