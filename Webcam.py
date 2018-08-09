import cv2
import os


class Webcam:
    def __init__(self, device_id=0):
        self.cam = cv2.VideoCapture(device_id)


    def get_possible_resolutions(self):
        import v4l2
        from fcntl import ioctl

        fd = os.open("/dev/video0", os.O_RDWR)

        fmt = v4l2.v4l2_fmtdesc()
        fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE

        formats = []

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
                formats.append((fmt.description, (frm.discrete.width, frm.discrete.height)))

            fmt.index += 1

        return formats


    def get_possible_framerates(self):
        # TODO: Possibly the same like with `get_possible_resolutins()`
        pass


    def get_effective_resolution(self):
        return (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))


    def get_effective_framerate(self):
        return int(self.cam.get(cv2.CAP_PROP_FPS))


    def set_resolution(self, width, height):
        previous_resolution = self.get_effective_resolution()

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if (width, height) != self.get_effective_resolution():
            self.set_resolution(*previous_resolution)
            raise ValueError("Resolution not supported by camera.")


    def set_framerate(self, framerate):
        previous_framerate = self.get_effective_framerate()

        self.cam.set(cv2.CAP_PROP_FPS, framerate)

        if framerate != self.get_effective_framerate():
            self.set_framerate(previous_framerate)
            raise ValueError("Framerate not supported by camera.")
