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
        frame_type = "420"
        print(self.header[:-1])

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
            elif info[0] == "G":
                self.gomby = Golomb(int(info[1:]))

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

    def decompress_video(self, decompress_path, mode="JPEG-1"):
        if mode not in ["JPEG-"+str(i) for i in range(1, 8)] and mode != "JPEG-LS":
            print("Invalid mode")
            return None
        
        with open(decompress_path, "wb") as write_stream:
            read_stream = BitStream(self.file_path)
            read_stream.set_offset(len(self.header)*8)
            write_stream.write(self.header.encode())
            write_stream.write("FRAME\n".encode())
            number_of_numbers = 0
            control = 0
            old_c = 0

            while read_stream.read_bits(10000):
                
                got_number = self.gomby.add_bits(read_stream.get_bit_array()[-10000:])
                old_c = control
                
                if got_number:
                    nums = self.gomby.decode_nums()
                    number_of_numbers += len(nums)
                    control += 1
                    for num in nums:
                        write_stream.write(str(num).encode())
                if old_c != control:
                    print("ay lmao", number_of_numbers)
                
            
            num_bits = read_stream.read_allbits()
            got_number = self.gomby.add_bits(read_stream.get_bit_array()[-num_bits:])
            old_c = control
            
            if got_number:
                nums = self.gomby.decode_nums()
                number_of_numbers += len(nums)
                control += 1
                for num in nums:
                    write_stream.write(str(num).encode())

                

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

                compressed_frame = self.frame.compress_frame(mode)
                
                y = compressed_frame[:,:,0]
                u = compressed_frame[:,:,1]
                v = compressed_frame[:,:,2]

                for x in np.nditer(y):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                bit_stream.write_allbits(compress_path)

                print("Finished compressing Y")

                bit_stream.reset_bit_array()
                for x in np.nditer(u):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                bit_stream.write_allbits(compress_path)
                
                print("Finished compressing U")

                bit_stream.reset_bit_array()
                for x in np.nditer(v):
                    bit_stream.add_to_bit_array(gomby.encode(int(x)))

                bit_stream.write_allbits(compress_path)

                print("Finished compressing.")

                break

if __name__ == "__main__":
    codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.y4m")
    codec.compress_video("../../tests/vids/ducks_take_off_1080p50.c4m")
    compressed_codec = VideoCodec("../../tests/vids/ducks_take_off_1080p50.c4m")
    compressed_codec.decompress_video("ducks_take_off.y4m")
    