#include <stdio.h>
#include <iostream>
#include <math.h> 

using namespace std;

class Golomb
{
private:
    int encoding_parameter;
    int b_param;

public:
    /* Constructor of the Golomb converter */
    Golomb(int m)
    {
        encoding_parameter = m;
        b_param = ceil(log2(m));
    }

    bool *encode(int m)
    {
        int q = m/encoding_parameter, r=m%encoding_parameter;
    
        bool *code = new bool[q + 1 + b_param];
        int i;
        for (i = 0; i < q; i++){
            code[i] = (bool) 1;
        }
        code[i] = (bool)(0);
        for (int j = rest_size-1, n = m%encoding_parameter; j >= 0; j--, ++i) {
            cout << "index: " << i;
            int k = n >> j;
            code[i] = k & 1;
        }
        return code;
    }

    /* GETTERS & SETTERS */
};

int main()
{
    Golomb *g = new Golomb(5);

    for (int i = 0; i < 16; i++){
        bool *test = g->encode(i);
        cout << "Testing " << i << "\t";
        for (int j = 0; j <= i/5 + g->rest_size; j++){
            cout << test[j];
        }
        cout << "\n";
    }
        

    return 0;
}
