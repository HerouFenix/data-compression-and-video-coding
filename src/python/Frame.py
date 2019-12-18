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
    
    def compress_frame(self, mode):
        if self.Y is None or self.U is None or self.V is None:
            print("Impossible to compress None")
            return None

        compress_y = numpy.zeros(self.Y.shape)
        compress_u = numpy.zeros(self.U.shape)
        compress_v = numpy.zeros(self.V.shape)

        u_skip = None
        v_skip = None

        if(compress_y.size != compress_u.size):
            #420
            #u metade ; v metade
            print("Compressing 420")
            u_skip = 0
            u_index = [0,0]

            v_skip = 0
            v_index = [0,0]
        elif (compress_y.size != compress_v.size):
            #422
            #v metade
            print("Compressing 422")
            v_skip = 0
            v_index = [0,0]

        for i in range(self.height -1, -1, -1):
            
            for j in range(self.width -1, -1, -1):
                if mode == "JPEG-1":
                    if j-1>=0:
                        predictor_y = int(self.Y[i, j-1])
                        if u_skip is None:
                            predictor_u = int(self.U[i, j-1])
                        if v_skip is None:
                            predictor_v = int(self.V[i, j-1])
                    else:
                        predictor_y = 0
                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[1]-1>=0:
                                predictor_u = int(self.U[u_index[0], u_index[1]-1])
                            else:
                                predictor_u = 0
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = int(self.V[v_index[0], v_index[1]-1])
                            else:
                                predictor_v = 0
                            v_skip = 0

                elif mode == "JPEG-2":
                    if i-1>=0:
                        predictor_y = int(self.Y[i-1,j])
                        if u_skip is None:
                            predictor_u = int(self.U[i-1,j])
                        if v_skip is None:
                            predictor_v = int(self.V[i-1,j])
                    
                    else:
                        predictor_y = 0
                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0:
                                predictor_u = int(self.U[u_index[0]-1, u_index[1]])
                            else:
                                predictor_u = 0
                        
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = int(self.V[v_index[0]-1, v_index[1]])
                            else:
                                predictor_v = 0
                            
                            v_skip = 0
                else:
                    if i-1>=0 and j-1>=0:
                        predictor_y = self.predictor(mode, a=int(self.Y[i, j-1]), b=int(self.Y[i-1,j]), c=int(self.Y[i-1,j-1]))
                        if u_skip is None:
                            predictor_u = self.predictor(mode, a=int(self.U[i, j-1]), b=int(self.U[i-1,j]), c=int(self.U[i-1,j-1]))
                        if v_skip is None:
                            predictor_v = self.predictor(mode, a=int(self.V[i, j-1]), b=int(self.V[i-1,j]), c=int(self.V[i-1,j-1]))
                    else:
                        predictor_y = 0

                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0
                    
                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0 and u_index[1]-1>=0:
                                predictor_u = self.predictor(mode, a=int(self.U[u_index[0], u_index[1]-1]), b=int(self.U[u_index[0]-1,u_index[1]]), c=int(self.U[u_index[0]-1,u_index[1]-1]))

                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = self.predictor(mode, a=int(self.V[v_index[0], v_index[1]-1]), b=int(self.V[v_index[0]-1,v_index[1]]), c=int(self.V[v_index[0]-1,v_index[1]-1]))
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                compress_y[i,j] = int(self.Y[i,j]) - predictor_y

                if u_skip is None:
                    compress_u[i,j] = int(self.U[i,j]) - predictor_u
                elif u_skip == 0:
                    compress_u[u_index[0],u_index[1]] = int(self.U[u_index[0],u_index[1]]) - predictor_u
                    u_index[1] += 1

                if v_skip is None:
                    compress_v[i,j] = int(self.V[i,j]) - predictor_v
                elif v_skip == 0:
                    compress_v[v_index[0],v_index[1]] = int(self.V[v_index[0],v_index[1]]) - predictor_v
                    v_index[1] += 1
    
            if v_skip is not None:
                if v_skip == 2:
                    v_skip = 0
                else:
                    v_index[0] += 1
                    v_index[1] = 0
                    v_skip = 2
            if u_skip is not None:
                if u_skip == 2:
                    u_skip = 0
                else:
                    u_index[0] += 1
                    u_index[1] = 0
                    u_skip = 2

        self.Y = compress_y
        self.U = compress_u
        self.V = compress_v

        return (self.Y, self.U, self.V)
    
    def decompress_frame(self, mode):
        decompressed_y = self.Y
        decompressed_u = self.U
        decompressed_v = self.V

        u_skip = False
        v_skip = False

        if(decompressed_y.size != decompressed_u.size):
            #420
            #u metade ; v metade
            print("Decompressing 420")
            u_skip = True
            u_index = [0,0]

            v_skip = True
            v_index = [0,0]
        elif (decompressed_y.size != decompressed_v.size):
            #422
            #v metade
            print("Decompressing 422")
            v_skip = 0
            v_index = [0,0]

    
        for i in range(self.height):
            for j in range(self.width):
                if mode == "JPEG-1":
                    predictor_y = decompressed_y[i, j-1] if j-1 >= 0 else 0
                    predictor_u = decompressed_u[i, j-1] if u_skip is None and j-1 >= 0 else 0
                    predictor_v = decompressed_v[i, j-1] if v_skip is None and j-1 >= 0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[1]-1>=0:
                                predictor_u = decompressed_u[u_index[0], u_index[1]-1] 
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = decompressed_v[v_index[0], v_index[1]-1] 
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                elif mode == "JPEG-2":
                    predictor_y = decompressed_y[i-1, j] if i-1 >= 0 else 0
                    predictor_u = decompressed_u[i-1, j] if u_skip is None and i-1 >= 0 else 0
                    predictor_v = decompressed_v[i-1, j] if v_skip is None and i-1 >= 0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0:
                                predictor_u = decompressed_u[u_index[0]-1, u_index[1]] 
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[0]-1>=0:
                                predictor_v = decompressed_v[v_index[0]-1, v_index[1]] 
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                else:
                    predictor_y = self.predictor(mode, a=int(decompressed_y[i, j-1]), b=int(decompressed_y[i-1,j]), c=int(decompressed_y[i-1,j-1])) if i-1>=0 and j-1>=0 else 0
                    predictor_u = self.predictor(mode, a=int(decompressed_u[i, j-1]), b=int(decompressed_u[i-1,j]), c=int(decompressed_u[i-1,j-1])) if u_skip is None and i-1>=0 and j-1>=0 else 0
                    predictor_v = self.predictor(mode, a=int(decompressed_v[i, j-1]), b=int(decompressed_v[i-1,j]), c=int(decompressed_v[i-1,j-1])) if v_skip is None and i-1>=0 and j-1>=0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0 and u_index[1]-1>=0:
                                predictor_u = self.predictor(mode, a=int(decompressed_u[u_index[0], u_index[1]-1]), b=int(decompressed_u[u_index[0]-1,u_index[1]]), c=int(decompressed_u[u_index[0]-1,u_index[1]-1]))
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[0]-1>=0 and v_index[1]-1>=0:
                                predictor_v = self.predictor(mode, a=int(decompressed_v[v_index[0], v_index[1]-1]), b=int(decompressed_v[v_index[0]-1,v_index[1]]), c=int(decompressed_v[v_index[0]-1,v_index[1]-1]))
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                decompressed_y[i,j] = decompressed_y[i,j] + predictor_y
                
                if u_skip is None:
                    decompressed_u[i,j] = decompressed_u[i,j] + predictor_u
                elif u_skip == 0:
                    decompressed_u[u_index[0],u_index[1]] = decompressed_u[u_index[0],u_index[1]] + predictor_u
                    u_index[1] += 1

                if v_skip is None:
                    decompressed_v[i,j] = decompressed_v[i,j] + predictor_v
                elif v_skip == 0:
                    decompressed_v[v_index[0],v_index[1]] = decompressed_v[v_index[0],v_index[1]] + predictor_v
                    v_index[1] += 1
                
            if v_skip is not None:import numpy


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
    
    def compress_frame(self, mode):
        if self.Y is None or self.U is None or self.V is None:
            print("Impossible to compress None")
            return None

        compress_y = numpy.zeros(self.Y.shape)
        compress_u = numpy.zeros(self.U.shape)
        compress_v = numpy.zeros(self.V.shape)

        u_skip = None
        v_skip = None

        if(compress_y.size != compress_u.size):
            #420
            #u metade ; v metade
            print("Compressing 420")
            u_skip = 0
            u_index = [0,0]

            v_skip = 0
            v_index = [0,0]
        elif (compress_y.size != compress_v.size):
            #422
            #v metade
            print("Compressing 422")
            v_skip = 0
            v_index = [0,0]

        for i in range(self.height -1, -1, -1):
            
            for j in range(self.width -1, -1, -1):
                if mode == "JPEG-1":
                    if j-1>=0:
                        predictor_y = int(self.Y[i, j-1])
                        if u_skip is None:
                            predictor_u = int(self.U[i, j-1])
                        if v_skip is None:
                            predictor_v = int(self.V[i, j-1])
                    else:
                        predictor_y = 0
                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[1]-1>=0:
                                predictor_u = int(self.U[u_index[0], u_index[1]-1])
                            else:
                                predictor_u = 0
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = int(self.V[v_index[0], v_index[1]-1])
                            else:
                                predictor_v = 0
                            v_skip = 0

                elif mode == "JPEG-2":
                    if i-1>=0:
                        predictor_y = int(self.Y[i-1,j])
                        if u_skip is None:
                            predictor_u = int(self.U[i-1,j])
                        if v_skip is None:
                            predictor_v = int(self.V[i-1,j])
                    
                    else:
                        predictor_y = 0
                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0:
                                predictor_u = int(self.U[u_index[0]-1, u_index[1]])
                            else:
                                predictor_u = 0
                        
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = int(self.V[v_index[0]-1, v_index[1]])
                            else:
                                predictor_v = 0
                            
                            v_skip = 0
                else:
                    if i-1>=0 and j-1>=0:
                        predictor_y = self.predictor(mode, a=int(self.Y[i, j-1]), b=int(self.Y[i-1,j]), c=int(self.Y[i-1,j-1]))
                        if u_skip is None:
                            predictor_u = self.predictor(mode, a=int(self.U[i, j-1]), b=int(self.U[i-1,j]), c=int(self.U[i-1,j-1]))
                        if v_skip is None:
                            predictor_v = self.predictor(mode, a=int(self.V[i, j-1]), b=int(self.V[i-1,j]), c=int(self.V[i-1,j-1]))
                    else:
                        predictor_y = 0

                        if u_skip is None:
                            predictor_u = 0
                        if v_skip is None:
                            predictor_v = 0
                    
                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0 and u_index[1]-1>=0:
                                predictor_u = self.predictor(mode, a=int(self.U[u_index[0], u_index[1]-1]), b=int(self.U[u_index[0]-1,u_index[1]]), c=int(self.U[u_index[0]-1,u_index[1]-1]))

                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = self.predictor(mode, a=int(self.V[v_index[0], v_index[1]-1]), b=int(self.V[v_index[0]-1,v_index[1]]), c=int(self.V[v_index[0]-1,v_index[1]-1]))
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                compress_y[i,j] = int(self.Y[i,j]) - predictor_y

                if u_skip is None:
                    compress_u[i,j] = int(self.U[i,j]) - predictor_u
                elif u_skip == 0:
                    compress_u[u_index[0],u_index[1]] = int(self.U[u_index[0],u_index[1]]) - predictor_u
                    u_index[1] += 1

                if v_skip is None:
                    compress_v[i,j] = int(self.V[i,j]) - predictor_v
                elif v_skip == 0:
                    compress_v[v_index[0],v_index[1]] = int(self.V[v_index[0],v_index[1]]) - predictor_v
                    v_index[1] += 1
    
            if v_skip is not None:
                if v_skip == 2:
                    v_skip = 0
                else:
                    v_index[0] += 1
                    v_index[1] = 0
                    v_skip = 2
            if u_skip is not None:
                if u_skip == 2:
                    u_skip = 0
                else:
                    u_index[0] += 1
                    u_index[1] = 0
                    u_skip = 2

        self.Y = compress_y
        self.U = compress_u
        self.V = compress_v

        return (self.Y, self.U, self.V)
    
    def decompress_frame(self, mode):
        decompressed_y = self.Y
        decompressed_u = self.U
        decompressed_v = self.V

        print("Decompressed Y be like")
        print(decompressed_y)
        print("Decompressed U be like")
        print(decompressed_u)
        print("Decompressed V be like")
        print(decompressed_v)

        u_skip = False
        v_skip = False

        if(decompressed_y.size != decompressed_u.size):
            #420
            #u metade ; v metade
            print("Decompressing 420")
            u_skip = True
            u_index = [0,0]

            v_skip = True
            v_index = [0,0]
        elif (decompressed_y.size != decompressed_v.size):
            #422
            #v metade
            print("Decompressing 422")
            v_skip = 0
            v_index = [0,0]

    
        for i in range(self.height):
            for j in range(self.width):
                if mode == "JPEG-1":
                    predictor_y = decompressed_y[i, j-1] if j-1 >= 0 else 0
                    predictor_u = decompressed_u[i, j-1] if u_skip is None and j-1 >= 0 else 0
                    predictor_v = decompressed_v[i, j-1] if v_skip is None and j-1 >= 0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[1]-1>=0:
                                predictor_u = decompressed_u[u_index[0], u_index[1]-1] 
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[1]-1>=0:
                                predictor_v = decompressed_v[v_index[0], v_index[1]-1] 
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                elif mode == "JPEG-2":
                    predictor_y = decompressed_y[i-1, j] if i-1 >= 0 else 0
                    predictor_u = decompressed_u[i-1, j] if u_skip is None and i-1 >= 0 else 0
                    predictor_v = decompressed_v[i-1, j] if v_skip is None and i-1 >= 0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0:
                                predictor_u = decompressed_u[u_index[0]-1, u_index[1]] 
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[0]-1>=0:
                                predictor_v = decompressed_v[v_index[0]-1, v_index[1]] 
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                else:
                    predictor_y = self.predictor(mode, a=int(decompressed_y[i, j-1]), b=int(decompressed_y[i-1,j]), c=int(decompressed_y[i-1,j-1])) if i-1>=0 and j-1>=0 else 0
                    predictor_u = self.predictor(mode, a=int(decompressed_u[i, j-1]), b=int(decompressed_u[i-1,j]), c=int(decompressed_u[i-1,j-1])) if u_skip is None and i-1>=0 and j-1>=0 else 0
                    predictor_v = self.predictor(mode, a=int(decompressed_v[i, j-1]), b=int(decompressed_v[i-1,j]), c=int(decompressed_v[i-1,j-1])) if v_skip is None and i-1>=0 and j-1>=0 else 0

                    if u_skip is not None and u_skip != 2:
                        if u_skip == 0:
                            u_skip = 1
                        else:
                            if u_index[0]-1>=0 and u_index[1]-1>=0:
                                predictor_u = self.predictor(mode, a=int(decompressed_u[u_index[0], u_index[1]-1]), b=int(decompressed_u[u_index[0]-1,u_index[1]]), c=int(decompressed_u[u_index[0]-1,u_index[1]-1]))
                            else:
                                predictor_u = 0
                            
                            u_skip = 0

                    if v_skip is not None and v_skip != 2:
                        if v_skip == 0:
                            v_skip = 1
                        else:
                            if v_index[0]-1>=0 and v_index[1]-1>=0:
                                predictor_v = self.predictor(mode, a=int(decompressed_v[v_index[0], v_index[1]-1]), b=int(decompressed_v[v_index[0]-1,v_index[1]]), c=int(decompressed_v[v_index[0]-1,v_index[1]-1]))
                            else:
                                predictor_v = 0
                            
                            v_skip = 0

                decompressed_y[i,j] = decompressed_y[i,j] + predictor_y
                
                if u_skip is None:
                    decompressed_u[i,j] = decompressed_u[i,j] + predictor_u
                elif u_skip == 0:
                    decompressed_u[u_index[0],u_index[1]] = decompressed_u[u_index[0],u_index[1]] + predictor_u
                    u_index[1] += 1

                if v_skip is None:
                    decompressed_v[i,j] = decompressed_v[i,j] + predictor_v
                elif v_skip == 0:
                    decompressed_v[v_index[0],v_index[1]] = decompressed_v[v_index[0],v_index[1]] + predictor_v
                    v_index[1] += 1
                
            if v_skip is not None:
                if v_skip == 2:
                    v_skip = 0
                else:
                    v_index[0] += 1
                    v_index[1] = 0
                    v_skip = 2
            if u_skip is not None:
                if u_skip == 2:
                    u_skip = 0
                else:
                    u_index[0] += 1
                    u_index[1] = 0
                    u_skip = 2


        self.Y = decompressed_y
        self.U = decompressed_u
        self.V = decompressed_v

        return (self.Y, self.U, self.V)

    def show_frame(self):
        
        self.YUV = numpy.dstack((self.Y, self.U, self.V))[
            :self.height, :self.width, :].astype(numpy.float)
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
        self.limit_to_convert = height*width*3

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))

        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
    
    def set_frame_by_array(self, nums):
        self.Y = numpy.array(nums[:self.width*self.height], dtype=numpy.int8)\
            .reshape((self.height, self.width))
        
        self.U = numpy.array(nums[self.width*self.height:self.width*self.height*2], dtype=numpy.int8)\
            .reshape((self.height, self.width//2))
        
        self.V = numpy.array(nums[self.width*self.height*2:self.width*3*self.height], dtype=numpy.int8)\
            .reshape((self.height//2, self.width//2))



class Frame422(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)
        self.limit_to_convert = height*width*2+(self.width//2)*(self.height//2)


    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        self.limit_to_convert = height*width*2
        
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2))
    
    def set_frame_by_array(self, nums):
        self.Y = numpy.array(nums[:self.width*self.height])\
            .reshape((self.height, self.width))
        
        self.U = numpy.array(nums[self.width*self.height:self.width*self.height*2])\
            .reshape((self.height, self.width//2))
        
        self.V = numpy.array(nums[self.width*self.height*2:(self.width*self.height*2+(self.width//2)*(self.height//2))])\
            .reshape((self.height//2, self.width//2))

    def show_frame(self):
        self.V = self.V.repeat(2,axis=0).repeat(2,axis=1)
        return super().show_frame()

class Frame420(Frame):
    def __init__(self, height, width):
        Frame.__init__(self, height, width)
        self.limit_to_convert = height*width + (width//2)*(height//2) + (width//2)*(height//2)

    def set_frame(self, stream):
        self.Y = numpy.fromfile(stream, dtype=numpy.uint8, count=self.width *
                                self.height).reshape((self.height, self.width))
        
        # Load the UV (chrominance) data from the stream, and double its size
        self.U = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2))
        self.V = numpy.fromfile(stream, dtype=numpy.uint8, count=(
            self.width//2)*(self.height//2)).reshape((self.height//2, self.width//2))

    def set_frame_by_array(self, nums):

        self.Y = numpy.array(nums[:self.width*self.height], dtype=numpy.float)\
            .reshape((self.height, self.width))
        print("set up Y frame")

        self.U = numpy.array(nums[self.width*self.height:((self.width//2)*(self.height//2)+self.width*self.height)], dtype=numpy.float)\
            .reshape((self.height//2, self.width//2))
        print("set up U frame")
        
        self.V = numpy.array(nums[((self.width//2)*(self.height//2)+self.width*self.height):self.limit_to_convert], dtype=numpy.float)\
            .reshape((self.height//2, self.width//2))
        print("set up V frame")
        return nums[self.limit_to_convert:]

    def show_frame(self):
        self.U = self.U.repeat(2,axis=0).repeat(2,axis=1)
        self.V = self.V.repeat(2,axis=0).repeat(2,axis=1)
        return super().show_frame()
