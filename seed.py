import socket
import sys
import time
import threading
from queue import Queue

# cite : https://github.com/attreyabhatt/Reverse-Shell
NUMBER_OF_THREADS = 1
JOB_NUMBER = [1]
queue = Queue()
host = ''
port = 9999
all_connections = []
all_address = []


def convert_list_to_thread_queue():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def create_and_run_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x=queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        queue.task_done()


# creating object of socket
def create_socket():
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: "+str(msg))


# binding the socket
def bind_socket():
    try:
        print("Binding the port: "+str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error: "+str(msg))
        bind_socket()


# Handling connections from multiple clients and saving to a list
# Closing previous connections if any
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection established with " + address[0] + "Port: " + str(address[1]))  # Displaying IP and Port
            # print(str(all_connections))
            conn.send(str.encode(str(all_address)))

            # delete_index = all_connections.index(conn, 0, len(all_connections))
            # del all_address[delete_index]
            # del all_connections[delete_index]
            # conn.close()

        except socket.error as msg:
            print("Socket Accepting error: "+str(msg))

        except KeyboardInterrupt:
            print("Keyboard Interrupt found..Exiting!!")

            for c in all_connections:
                c.close()

            del all_connections[:]
            del all_address[:]
            sys.exit()


create_and_run_threads()
convert_list_to_thread_queue()
