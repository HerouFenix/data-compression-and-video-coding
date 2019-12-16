import numpy as np
import cv2 as cv2
from Frame import *

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
        with open(self.file_path, "rb") as stream:

            line = stream.readline()
            #print(line)
            frame = Frame420(self.height, self.width)
            while True:
                line = stream.readline()
                frame.set_frame(stream)
                BGR = frame.show_frame()

                # Display the image with OpenCV
                cv2.imshow('image', BGR)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
    
    def decompress_frame(self, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1,8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        with open(self.file_path, "rb") as stream:
            line = stream.readline()
            
            frame = Frame420(self.height, self.width)
            while True:
                line = stream.readline()
                frame.set_frame(stream)

    def compress_video(self, compress_path, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1,8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        with open(self.file_path, "rb") as stream:
            line = stream.readline()
            
            frame = Frame420(self.height, self.width)
            while True:
                line = stream.readline()
                frame.set_frame(stream)

                compressed_frame = frame.compress_frame(mode)
                
                for f in compressed_frame:
                    for x in np.nditer(a):
                        print(x, end=' ')
                

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    codec.compress_video("../../tests/vids/ducks_take_off_1080p50.c4m")
