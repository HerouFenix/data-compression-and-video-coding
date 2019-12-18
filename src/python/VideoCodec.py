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
            while True:
                try:
                    line = stream.readline()
                    self.frame.set_frame(stream)
                    BGR = self.frame.show_frame()

                    # Display the image with OpenCV
                    cv2.imshow('image', BGR)
                    if cv2.waitKey() & 0xFF == ord('q'):
                        break

                except ValueError:
                    print("Finished showing video")
                    break

            cv2.destroyAllWindows()

    def decompress_video(self, decompress_path):       
        with open(decompress_path, "wb") as write_stream:
            #Get the bitstream to read the compression
            read_stream = BitStream(self.file_path)
            read_stream.set_offset(len(self.header)*8)

            #Write the header for the video
            write_stream.write(self.header.encode())
            write_stream.write("FRAME\n".encode())

            #This marks the start of decompression
            number_of_numbers = 0
            array_of_nums = []

            counter = 0
            while read_stream.read_bits(5000):
                got_number = self.gomby.add_bits(read_stream.get_bit_array())
                read_stream.delete_bits(5000)

                if got_number:
                    nums = self.gomby.decode_nums()
                    number_of_numbers += len(nums)
                    array_of_nums += nums
                
                if number_of_numbers >= self.frame.limit_to_convert:
                    counter += 1
                    print("Decompressing frame: ", counter)
                    
                    array_of_nums = self.frame.set_frame_by_array(array_of_nums)
                    y,u,v = self.frame.decompress_frame(self.decompress_mode)

                    #read_stream.clear_padding()
                    print("Stream offset at", read_stream.bit_offset)

                    write_stream.write(y.astype(np.uint8))
                    write_stream.write(u.astype(np.uint8))
                    write_stream.write(v.astype(np.uint8))
                    write_stream.write("FRAME\n".encode())
                    number_of_numbers -= self.frame.limit_to_convert
                    print("Finished writing decompressed frame, now only have", number_of_numbers)


            
            num_bits = read_stream.read_allbits()
            got_number = self.gomby.add_bits(read_stream.get_bit_array())
            if got_number:
                nums = self.gomby.decode_nums()
                array_of_nums += nums
                
                ## At this point we have all of the frame saved in memory, we will now start to divide it in frames to proceed to decompressing
                array_of_nums = self.frame.set_frame_by_array(array_of_nums)
                
                y,u,v = self.frame.decompress_frame(self.decompress_mode)

                write_stream.write(y.astype(np.uint8))
                write_stream.write(u.astype(np.uint8))
                write_stream.write(v.astype(np.uint8))
                print("Finished writing decompressed frame")
                #girar
            print("Finished writing decompressed frame")

            


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

            counter = 0


            while True:
                if counter > 2:
                    break
                counter += 1
                print("Compressing frame: ", counter)
                try:
                    line = stream.readline()
                except ValueError:
                    print("Finished compressing")
                    break
                line = stream.readline()
                self.frame.set_frame(stream)

                compressed_frame = self.frame.compress_frame(mode)
                
                y = compressed_frame[0]
                u = compressed_frame[1]
                v = compressed_frame[2]

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
                
                bit_stream.write_allbits(compress_path)
                bit_stream.reset_bit_array()
                print("Finished compressing Frame")

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    #codec.play_video()
    codec.compress_video("../../tests/vids/ducks_take_off_1080p50.c4m","JPEG-LS")
    compressed_codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.c4m")
    compressed_codec.decompress_video("ducks_take_off.y4m")

    codec = VideoCodec("ducks_take_off.y4m")
    codec.play_video()
