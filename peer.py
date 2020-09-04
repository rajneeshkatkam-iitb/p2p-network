import socket
import sys

s = socket.socket()
host = "192.168.0.192"
port = 9999

s.connect((host, port))

while True:
    try:
        data = s.recv(1024)
        print(data[:].decode("utf-8"))

    except socket.error as msg:
        print("Server closed the connection..exiting")
        sys.exit()

    except KeyboardInterrupt:
        s.close()

