import cv2
import time
import datetime

# camera = cv2.VideoCapture(0)  # 0 because we only have one camera

# write the cascade classifier as they are trained to detect faces and bodies

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# get the matching frame size of the existing camera
# frame_size = (int(cap.get(3)), int(cap.get(4)))
# video saving format use fourcc

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# make an outstream


while cap.isOpened():
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    # _, frame1 = camera.read()
    # # convert the image to gray scale so I can be able to apply the defined cascades
    # gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    #
    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # detect the faces that exist in the image
    # bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    # check the length of faces and bodies to check the number of faces and bodies we have in the image

    if len(faces) + len(bodies) > 0: # if we detect a face or body
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    #below is the code to draw contours
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)
    for (x, y, width, height) in bodies:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 5)

    cv2.imshow("security camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break


out.release()
# frame.release()
cv2.destroyAllWindows()
