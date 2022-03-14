# have computer vision
# detect motion
# alarm user when motion is detected

# import the package opencv
import os
import cv2
import datetime
import winsound

# define the camera capture
filename = 'recorded.avi'
frames_per_seconds = 10.0
my_res = '720p'


def change_res(cam, width, height):
    cam.set(3, width)
    cam.set(4, height)


# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


def get_dim(cam, res='720p'):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(cam, width, height)
    return width, height
# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    '.avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    '.mp4': cv2.VideoWriter_fourcc(*'H264'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


cam = cv2.VideoCapture(0)
dims = get_dim(cam, res=my_res)
video_type_cv2 = get_video_type(filename)

out = cv2.VideoWriter(filename, video_type_cv2, frames_per_seconds, dims)
# loop to turn the camera on

while cam.isOpened():
    ret, frame1 = cam.read()  # frame1
    ret, frame2 = cam.read()  # frame2

    difference = cv2.absdiff(frame1, frame2)  # find the difference between the frames
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # create threshold

    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0,255,0),2)
    out.write(frame1)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # winsound.Beep(500, 200)
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Security Camera with motion detection', frame1)

out.release()
