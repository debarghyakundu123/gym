
import cv2
import mediapipe
import math
N = 0
# h = 0
r = 0
theta = 0
setp = []
points = []

drawingModule = mediapipe.solutions.drawing_utils
poseModule = mediapipe.solutions.pose
pose = poseModule.Pose(
    static_image_mode=True,
    min_detection_confidence=0.5)

capture = cv2.VideoCapture(0)
capture.set(3, 1200)  # 3 for width
capture.set(4, 900)  # 4 for height
capture.set(10, 100)  # 10 for brightness

# with poseModule: #(mode=False, upBody=False, smooth=True, detectionCon=0.5):
while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    img2 = frame.copy()
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image_height, image_width, _ = frame.shape

    if results.pose_landmarks:
        drawingModule.draw_landmarks(frame, results.pose_landmarks, poseModule.POSE_CONNECTIONS)
        for ids, lm in enumerate(results.pose_landmarks.landmark):
            cx, cy = lm.x * image_width, lm.y * image_height
            #print(ids, cx, cy)
            setp.append([cx, cy])

    if bool(setp):
        # h = setp[16][1] - setp[12][1]
        abx = setp[14][0] - setp[12][0]
        aby = setp[14][1] - setp[12][1]
        acx = setp[24][0] - setp[12][0]
        acy = setp[24][1] - setp[12][1]
        theta = math.acos((abx*acx + aby*acy)/((math.sqrt(abx**2 + aby**2))*(math.sqrt(acx**2 + acy**2))))
        #print(h)

    if theta < math.pi/4:
        theta1 = theta
    if theta > 3*math.pi/4:
        if theta1 < math.pi/4:
            N = N + 1
            theta1 = theta

    # if h > 0:
    #     h1 = h
    # if h < 0:
    #     if h1 > 0:
    #         N = N+1
    #         h1 = h

    # TO RESET THE COUNTER
    if bool(setp):
        r = math.sqrt((setp[12][0] - setp[19][0]) ** 2 + (setp[12][1] - setp[19][1]) ** 2)
    if r < 20:
        N = 0

    print(N)
    cv2.putText(frame, str("Jumping Jack Count"), (20, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    cv2.putText(frame, str(int(N)), (150, 250), cv2.FONT_HERSHEY_COMPLEX, 4, (0, 255, 0), 4)
    setp.clear()

    cv2.imshow('JJ_C', frame)
    #cv2.imshow('JJC', img2)

    if cv2.waitKey(1) == 27:  # ESC key
        break

cv2.destroyAllWindows()
capture.release()
