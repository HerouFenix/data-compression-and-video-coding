import numpy
import cv2


class VideoCodec:

    def __init__(self):
        self.capture = cv2.VideoCapture(
            "../../tests/vids/ducks_take_off_1080p50.y4m")

    def playstation(self):
        while(True):
            # Capture frame-by-frame
            ret, frame = self.capture.read()

            # Our operations on the frame come here
            yuv = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)
            y,u,v = cv2.split(yuv)

            # Display the resulting frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    codec = VideoCodec()
    codec.playstation()
