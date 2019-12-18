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
            self.header = (frame_reader.readline()).decode("UTF-8")

        header_info = self.header.split(" ")
        self.frame_type = "420"
        print(self.header)

        for info in header_info:
            info = info.rstrip()
            if info[0] == "W":
                self.width = int(info.replace("W", ""))
            elif info[0] == "H":
                self.height = int(info.replace("H", ""))
            elif info[0] == "F":
                self.fps = info.replace("F", "")
            elif info[0] == "C":
                info = info.replace("C", "")
                if info.startswith("420"):
                    self.frame_type = "420"
                if info.startswith("422"):
                    self.frame_type = "422"
                if info.startswith("444"):
                    self.frame_type = "444"
            elif info[0] == "G":
                self.gomby = Golomb(int(info[1:]))
            elif info[0] == "M":
                self.decompress_mode = info[1:]

        if self.frame_type == "420":
            self.frame = Frame420(self.height, self.width)
        if self.frame_type == "422":
            self.frame = Frame422(self.height, self.width)
        if self.frame_type == "444":
            self.frame = Frame444(self.height, self.width)
        
        self.test_y = None
        self.test_u = None
        self.test_v = None

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

    def decompress_video(self, decompress_path):       
        with open(decompress_path, "wb") as write_stream:
            #Get the bitstream to read the compression
            read_stream = BitStream(self.file_path)
            read_stream.set_offset(len(self.header)*8 + 8)

            #Write the header for the video
            write_stream.write(self.header.encode())
            write_stream.write("FRAME\n".encode())

            #This marks the start of decompression
            number_of_numbers = 0
            array_of_nums = []

            while read_stream.read_bits(5000):
                
                got_number = self.gomby.add_bits(read_stream.get_bit_array())
                read_stream.delete_bits(5000)

                if got_number:
                    nums = self.gomby.decode_nums()
                    number_of_numbers += len(nums)
                    array_of_nums += nums
                
                if number_of_numbers >= self.frame.limit_to_convert:
                    print("Converted", number_of_numbers)
                    self.frame.set_frame_by_array(array_of_nums)
                    print("Finished writing to frame")
                    self.frame.decompress_frame(self.decompress_mode)
                    print("Done")
                    return 1
            
            num_bits = read_stream.read_allbits()
            print(num_bits)
            got_number = self.gomby.add_bits(read_stream.get_bit_array())

            nums = self.gomby.decode_nums()
            print(len(self.gomby.bit_feed))
            array_of_nums += nums
            print("Finished loadiiiiiing file")
            
            ## At this point we have all of the frame saved in memory, we will now start to divide it in frames to proceed to decompressing
            self.frame.set_frame_by_array(array_of_nums)
            
            y,u,v = self.frame.decompress_frame(self.decompress_mode)
            print(y)
            print(u)
            print(v)

            BGR = self.frame.show_frame()

            # Display the image with OpenCV
            cv2.imshow('image', BGR)
            if cv2.waitKey() & 0xFF == ord('q'):
                return

                

    def compress_video(self, compress_path, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1, 8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        with open(self.file_path, "rb") as stream:
            line = stream.readline()
        
            gomby = Golomb(4)
            bit_stream = BitStream()

            header = self.header[:-1] + " G" + str(gomby.encoding_parameter) + " M" + mode + "\n"

            with open(compress_path, "wb") as file_path:
                file_path.write(header.encode())

            while True:
                line = stream.readline()
                self.frame.set_frame(stream)
                print(self.frame.Y)
                print(self.frame.U)
                print(self.frame.V)

                compressed_frame = self.frame.compress_frame(mode)
                
                y = compressed_frame[0]
                u = compressed_frame[1]
                v = compressed_frame[2]
                print(y)
                print(u)
                print(v)
    
                number_of_numbers = 0
                for x in np.nditer(y):
                    number_of_numbers += 1
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                #bit_stream.write_allbits(compress_path)

                print("Finished compressing Y")

                #bit_stream.reset_bit_array()
                for x in np.nditer(u):
                    number_of_numbers += 1

                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                #bit_stream.write_allbits(compress_path)
                
                print("Finished compressing U")

                #bit_stream.reset_bit_array()
                for x in np.nditer(v):
                    number_of_numbers += 1
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))
                print(number_of_numbers)
                bit_stream.write_allbits(compress_path)

                print("Finished compressing.")
                break

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    codec.compress_video("../../tests/vids/ducks_take_off_1080p50.c4m")
    compressed_codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.c4m")
    compressed_codec.decompress_video("ducks_take_off.y4m")
    