import numpy as np
import cv2 as cv2
from Frame import *
from Golomb import Golomb
from BitStream import BitStream


class VideoCodec:

    def __init__(self, file_path):
        self.file_path = file_path

        # Get our header info
        with open(self.file_path, "rb") as frame_reader:
            header = (frame_reader.readline()).decode("UTF-8")
        header_info = header.split(" ")

        frame_type = "420"

        for info in header_info:
            if info[0] == "W":
                self.width = int(info.replace("W", ""))
            elif info[0] == "H":
                self.height = int(info.replace("H", ""))
            elif info[0] == "F":
                self.fps = info.replace("F", "")
            elif info[0] == "C":
                info = info.replace("C", "")
                if info.startswith("420"):
                    frame_type = "420"
                if info.startswith("422"):
                    frame_type = "422"
                if info.startswith("444"):
                    frame_type = "444"

        if frame_type == "420":
            self.frame = Frame420(self.height, self.width)
        if frame_type == "422":
            frame_type = Frame422(self.height, self.width)
        if frame_type == "444":
            frame_type = Frame444(self.height, self.width)

    def play_video(self):
        with open(self.file_path, "rb") as stream:

            line = stream.readline()
            # print(line)

            while True:
                line = stream.readline()
                self.frame.set_frame(stream)
                BGR = self.frame.show_frame()

                # Display the image with OpenCV
                cv2.imshow('image', BGR)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()

    def decompress_frame(self, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1, 8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        with open(self.file_path, "rb") as stream:
            line = stream.readline()

            while True:
                line = stream.readline()
                self.frame.set_frame(stream)

    def compress_video(self, compress_path, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1, 8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        with open(self.file_path, "rb") as stream:
            line = stream.readline()
            
            frame = Frame420(self.height, self.width)

            gomby = Golomb(4)
            bit_stream = BitStream()

            while True:
                line = stream.readline()
                self.frame.set_frame(stream)

                compressed_frame = self.frame.compress_frame(mode)

                compressed_frame = frame.compress_frame(mode)
                
                y = compressed_frame[:,:,0]
                u = compressed_frame[:,:,1]
                v = compressed_frame[:,:,2]

                #bit_array =[]
                for x in np.nditer(y):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))
                    #print(gomby.encode(int(x)))
                bit_stream.write_allbits(compress_path)

                print("Finished compressing Y")

                bit_stream.reset_bit_array()
                #bit_array =[]
                for x in np.nditer(u):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))
                    #print(gomby.encode(int(x)))
                bit_stream.write_allbits(compress_path)
                
                print("Finished compressing U")

                bit_stream.reset_bit_array()
                #bit_array =[]
                for x in np.nditer(v):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))
                    #print(gomby.encode(int(x)))
                bit_stream.write_allbits(compress_path)

                print("Finished compressing.")

                break

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    codec.compress_video("../../tests/vids/ducks_take_off_1080p50.c4m")
