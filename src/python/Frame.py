import numpy

class Frame:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.YUV = None

    def show_frame(self):
        if self.YUV is None:
            return None
        self.YUV[:, :, 0]  = self.YUV[:, :, 0]  - 16   # Offset Y by 16
        self.YUV[:, :, 1:] = self.YUV[:, :, 1:] - 128  # Offset UV by 128
        M = numpy.array([[1, 1.172,  0.000],    # B
                    [1, -0.344, -0.714],    # G
                    [1,  0.000,  1.402]])   # R
        # Take the dot product with the matrix to produce BGR output, clamp the
        # results to byte range and convert to bytes
        BGR = self.YUV.dot(M.T).clip(0, 255).astype(numpy.uint8)
        return BGR

class Frame444(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))

        self.YUV = numpy.dstack((self.Y, self.U, self.V))[:self.height, :self.width, :].astype(numpy.float) 

class Frame422(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(self.width//2)*(self.height//2)).\
                reshape((self.height//2, self.width//2)).\
                repeat(2, axis=0).repeat(2, axis=1)

        self.YUV = numpy.dstack((self.Y, self.U, self.V))[:self.height, :self.width, :].astype(numpy.float) 
    
class Frame420(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)
    
    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width*self.height).\
                reshape((self.height, self.width))
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=(self.width//2)*(self.height//2)).\
                reshape((self.height//2, self.width//2)).\
                repeat(2, axis=0).repeat(2, axis=1)
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(self.width//2)*(self.height//2)).\
                reshape((self.height//2, self.width//2)).\
                repeat(2, axis=0).repeat(2, axis=1)
        
        self.YUV = numpy.dstack((self.Y, self.U, self.V))[:self.height, :self.width, :].astype(numpy.float)