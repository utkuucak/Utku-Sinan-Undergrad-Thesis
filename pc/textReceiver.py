import socketserver
import time

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):

        # get the time in a string form to use as file name
        current_time = time.strftime("%Y_%m_%d_%H%M%S", time.localtime())

        # construct the file path
        file_path = "./" + current_time +".txt"

        # get the data sent over socket
        self.data = self.rfile.read().strip()

        # convert bytes data to string and print to console
        print(str(self.data, "utf-8"))

        # write received data to a new file
        with  open(file_path, 'w') as f:
            f.write(str(self.data, "utf-8"))
        
if __name__ == "__main__" :
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
