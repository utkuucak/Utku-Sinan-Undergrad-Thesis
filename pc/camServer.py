import socketserver
import cv2
import numpy as np

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):

        self.data = self.rfile.read()

        cv2.imshow('frame', self.data)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
