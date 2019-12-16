import numpy


class Frame:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.YUV = None
        self.Y = None
        self.U = None
        self.V = None

    def predictor(self, mode, a=0, b=0, c=0):
        if mode == "JPEG-1":
            return a
        if mode == "JPEG-2":
            return b
        if mode == "JPEG-3":
            return c
        if mode == "JPEG-4":
            return a+b-c
        if mode == "JPEG-5":
            return a+(b-c)/2
        if mode == "JPEG-6":
            return b+(a-c)/2
        if mode == "JPEG-7":
            return (a+b)/2
        
        if c >= max(a,b):
            return min(a,b)
        if c<=min(a,b):
            return max(a,b)
        return a+b-c


    def compress_frame(self, mode="JPEG-1"):
        if self.Y is None or self.U is None or self.V is None:
            print("Impossible to compress None")
            return None

        compress_y = numpy.zeros((self.height, self.width))
        compress_u = numpy.zeros((self.height, self.width))
        compress_v = numpy.zeros((self.height, self.width))

        for i in range(self.height -1, -1, -1):
            
            for j in range(self.width -1, -1, -1):
                if mode == "JPEG-1":
                    if j-1>=0:
                        predictor_y = int(self.Y[i, j-1])
                        predictor_u = int(self.U[i, j-1])
                        predictor_v = int(self.V[i, j-1])
                    else:
                        predictor_y = 0
                        predictor_u = 0
                        predictor_v = 0
                elif mode == "JPEG-2":
                    if i-1>=0:
                        predictor_y = int(self.Y[i-1,j])
                        predictor_u = int(self.U[i-1,j])
                        predictor_v = int(self.V[i-1,j])
                    else:
                        predictor_y = 0
                        predictor_u = 0
                        predictor_v = 0
                else:
                    if i-1>=0 and j-1>=0:
                        predictor_y = self.predictor(mode, a=int(self.Y[i, j-1]), b=int(self.Y[i-1,j]), c=int(self.Y[i-1,j-1]))
                        predictor_u = self.predictor(mode, a=int(self.U[i, j-1]), b=int(self.U[i-1,j]), c=int(self.V[i-1,j-1]))
                        predictor_v = self.predictor(mode, a=int(self.V[i, j-1]), b=int(self.V[i-1,j]), c=int(self.V[i-1,j-1]))
                    else:
                        predictor_y = 0
                        predictor_u = 0
                        predictor_v = 0
                compress_y[i,j] = int(self.Y[i,j]) - predictor_y
                compress_u[i,j] = int(self.U[i,j]) - predictor_u
                compress_v[i,j] = int(self.V[i,j]) - predictor_v

        return numpy.dstack((compress_y, compress_u, compress_v))[
            :self.height, :self.width, :].astype(numpy.float)
    
    def decompress_frame(self, frame, mode="JPEG-1"):
        compressed_y = frame[:,:,0]
        compressed_u = frame[:,:,1]
        compressed_v = frame[:,:,2]
    
        for i in range(self.height):
            for j in range(self.width):
                predictor_y = compressed_y[i, j-1] if j-1 >= 0 else 0
                predictor_u = compressed_u[i, j-1] if j-1 >= 0 else 0
                predictor_v = compressed_v[i, j-1] if j-1 >= 0 else 0
                
                compressed_y[i,j] = compressed_y[i,j] + predictor_y
                compressed_u[i,j] = compressed_u[i,j] + predictor_u
                compressed_v[i,j] = compressed_v[i,j] + predictor_v

        self.YUV = numpy.dstack((compressed_y, compressed_u, compressed_v))[
            :self.height, :self.width, :].astype(numpy.float)

        return self.YUV


    def show_frame(self):
        if self.YUV is None:
            return None
        self.YUV[:, :, 0] = self.YUV[:, :, 0] - 16   # Offset Y by 16
        self.YUV[:, :, 1:] = self.YUV[:, :, 1:] - 128  # Offset UV by 128
        M = numpy.array([[1, 1.172,  0.000],    # B
                         [1, -0.344, -0.714],    # G
                         [1,  0.000,  1.402]])   # R

        # Take the dot product with the matrix to produce BGR output
        BGR = self.YUV.dot(M.T).clip(0, 255).astype(numpy.uint8)
        return BGR


class Frame444(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))

        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))

        self.YUV = numpy.dstack((self.Y, self.U, self.V))[
            :self.height, :self.width, :].astype(numpy.float)


class Frame422(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2)).repeat(2, axis=0).repeat(2, axis=1)

        self.YUV = numpy.dstack((self.Y, self.U, self.V))[
            :self.height, :self.width, :].astype(numpy.float)


class Frame420(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2)).repeat(2, axis=0).repeat(2, axis=1)
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2)).repeat(2, axis=0).repeat(2, axis=1)

        self.YUV = numpy.dstack((self.Y, self.U, self.V))[
            :self.height, :self.width, :].astype(numpy.float)
