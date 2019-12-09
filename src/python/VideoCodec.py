import numpy
import cv2

"""
class VideoCodec:

    def __init__(self, file_path):
        self.capture = cv2.VideoCapture(file_path)

    def play_video(self):
        while(True):
            # Capture frame-by-frame
            ret, frame = self.capture.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print(frame)

            # Display the resulting frame
            cv2.imshow('frame',frame)    
            break
            # Display the resulting frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()  
"""
"""

        with open(self.file_path, "rb") as frame_reader:

            line = frame_reader.readline()
            control = 0
            print(line)
            while True:
                line = frame_reader.readline()
                print(line)
                y = frame_reader.read(1)
                if y == b'x/20':
                    while True:
                        y = frame_reader.read(1)
                        if y == b'x/0A':
                            y = frame_reader.read(1)
                            break
            
                u = frame_reader.read(1)
                v = frame_reader.read(1)
                y = int.from_bytes(y, 'big')/255.0
                u = int.from_bytes(u, 'big')/255.0
                v = int.from_bytes(v, 'big')/255.0
                YUV= [y,u,v]
                for i in range(self.height):
                    for j in range(self.width):
                        if i==0 and j == 0:
                            continue
                        y = frame_reader.read(1)
                        u = frame_reader.read(1)
                        v = frame_reader.read(1)
                        y = int.from_bytes(y, 'big')/255.0
                        u = int.from_bytes(u, 'big')/255.0
                        v = int.from_bytes(v, 'big')/255.0
                        YUV+= [y,u,v]
                px = self.width*self.height
                YUV = numpy.array(YUV)
                Y = YUV[0:self.width*self.height].reshape(self.height, self.width)
                U = YUV[px:(px*5)//4].reshape(self.height//2,self.width//2)
                V = YUV[(px*5)//4:(px*6)//4].reshape(self.height//2,self.width//2)
                Ubull = U.copy().resize((self.height, self.width ))
                Vbull = V.copy().resize((self.height, self.width ))
                frame = numpy.append(Y, Ubull)
                frame = numpy.append(frame, Vbull)
                print("ika", type(frame))
                cv2.imshow('frame', frame[:-2])
                cv2.waitKey()
                control += 1
                if control == 1:
                    break"""

class VideoCodec:

    def __init__(self, file_path):
        self.file_path = file_path

        # Get our header info
        with open(self.file_path, "rb") as frame_reader:
            header = (frame_reader.readline()).decode("UTF-8")
        header_info = header.split(" ")
        self.width = int(header_info[1].replace("W", ""))
        self.height = int(header_info[2].replace("H", ""))
        self.fps = header_info[3].replace("F", "")


    def play_video(self):

#"""

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    codec.play_video()
