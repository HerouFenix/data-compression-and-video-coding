import numpy as np
import cv2 as cv2
from Frame import *
from Golomb import Golomb
from BitStream import BitStream
from time import time


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
                    if cv2.waitKey(25) & 0xFF == ord('q'):
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
            counter_bits = 0
            while read_stream.read_bits(5000):
                got_number = self.gomby.add_bits(read_stream.get_bit_array())
                
                read_stream.delete_bits(5000)
                counter_bits += 1


                if got_number:
                    nums = self.gomby.decode_nums()
                    number_of_numbers += len(nums)
                    array_of_nums += nums
                    print("Decompressed", number_of_numbers)
                    print("Need to get", self.frame.limit_to_convert)
                
                if number_of_numbers >= self.frame.limit_to_convert:
                    counter += 1
                    print("Decompressing frame: ", counter)
                    
                    array_of_nums = self.frame.set_frame_by_array(array_of_nums)
                    y,u,v = self.frame.decompress_frame(self.decompress_mode)

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
                start_time = time()
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
                start = time()
                compressed_frame = self.frame.compress_frame(mode)
                print("Compressed in ", time() - start)
                y = compressed_frame[0]
                u = compressed_frame[1]
                v = compressed_frame[2]
    
                for x in np.nditer(y):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                #bit_stream.write_allbits(compress_path)

                print("Finished compressing Y")

                for x in np.nditer(u):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                #bit_stream.write_allbits(compress_path)
                
                print("Finished compressing U")

                for x in np.nditer(v):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))
                
                bit_stream.write_allbits(compress_path)

                print("Finished compressing in", time() - start_time)
            
            bit_stream.close(compress_path)

if __name__ == "__main__":
    file_name = input("Insira o path para um ficheiro .y4m\n")

    #Play Video
    codec = VideoCodec(file_name) #"../../tests/vids/ducks_take_off_1080p50.y4m"
    codec.play_video()
    
    #Compress Video
    compress_path = input("Insira o path onde quer guardar o ficheiro comprimido (.c4m)\n")
    compress_type = input("Insira o modo de compressão que quer usar (JPEG-1..7 ou JPEG-LS)\n")
    
    start_timer = time()
    codec.compress_video(compress_path,compress_type)
    print("It took ", time() - start_timer, " to Compress the video\n")


    #Decompress Video
    decompress_name = input("Insira o path para onde quer decomprimir o ficheiro (y4m)\n")

    compressed_codec = VideoCodec(compress_path)
    start_timer = time()
    compressed_codec.decompress_video(decompress_name)
    print("It took ", time() - start_timer, " to Decompress the video\n")
    
    #Play Decompressed Video
    codec = VideoCodec(decompress_name)
    codec.play_video()

