import cv2
import os


class Webcam:
    def __init__(self, device_id=0):
        if type(device_id) == int:
            self.__device_path = f"/dev/video{device_id}"
        elif type(device_id) == str:
            self.__device_path = device_id
        else:
            raise ValueError(f"Unkmown device {device_id}")

        if not os.path.exists(self.__device_path):
            raise FileNotFoundError(self.__device_path)

        self.__cam = cv2.VideoCapture(self.__device_path)


    def get_possible_resolutions(self):
        import v4l2
        from fcntl import ioctl

        fd = os.open(self.__device_path, os.O_RDWR)
        fmt = v4l2.v4l2_fmtdesc()
        fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        resolutions = set()

        # Special thanks to @Rirush for this solution
        while True:
            try:
                ioctl(fd, v4l2.VIDIOC_ENUM_FMT, fmt)
            except OSError:
                break
            frm = v4l2.v4l2_frmsizeenum()
            frm.pixel_format = fmt.pixelformat

            while True:
                try:
                    ioctl(fd, v4l2.VIDIOC_ENUM_FRAMESIZES, frm)
                except OSError:
                    break
                frm.index += 1
                resolutions.add((frm.discrete.width, frm.discrete.height))

            fmt.index += 1

        os.close(fd)
        return resolutions


    def get_possible_framerates(self):
        # TODO: Possibly the same like with `get_possible_resolutins()`
        pass


    def get_effective_resolution(self):
        return (int(self.__cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.__cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))


    def get_effective_framerate(self):
        return int(self.__cam.get(cv2.CAP_PROP_FPS))


    def set_resolution(self, width, height):
        previous_resolution = self.get_effective_resolution()

        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if (width, height) != self.get_effective_resolution():
            self.set_resolution(*previous_resolution)
            raise ValueError("Resolution not supported by camera.")


    def set_framerate(self, framerate):
        previous_framerate = self.get_effective_framerate()

        self.__cam.set(cv2.CAP_PROP_FPS, framerate)

        if framerate != self.get_effective_framerate():
            self.set_framerate(previous_framerate)
            raise ValueError("Framerate not supported by camera.")


    def next_frame(self):
        status, frame = self.__cam.read()
        if status:
            return frame
        else:
            raise IOError("Could not get frame")


    def close(self):
        self.__cam.release()
        del(self.__cam)
