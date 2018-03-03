import cv2
import socket
import numpy as np

HOST, PORT = "localhost", 9999

cap = cv2.VideoCapture(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        #cv2.imshow('frame', frame)

        sock.sendall(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
