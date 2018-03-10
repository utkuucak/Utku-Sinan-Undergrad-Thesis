import cv2

cap = cv2.VideoCapture(0)
try:
    while (True):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        cv2.waitKey(5)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
