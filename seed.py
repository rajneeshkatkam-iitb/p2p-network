import socket
import sys
import time
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
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
    for _ in range(NUMBER_OF_THREADS):
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        if x == 2:
            start_shell()

        queue.task_done()


# 2nd thread functions below
def start_shell():

    global thread_run
    thread_run=True

    while thread_run:
        cmd=input("shell> ")
        if cmd == 'list':
            list_connections()

        elif 'exit' in cmd:
            exit_command()
            thread_run=False
            break
        else:
            print("Command not recognised")



def list_connections():
    print("------- My Peer List ------")
    for i, address in enumerate(all_address):
        print(str(i) + ". "+ str(address))

def exit_command():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    s.close()



# creating object of socket
def create_socket():
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(5)
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
        time.sleep(5) # Time to sleep before reattempting the bind connection
        bind_socket()


# Handling connections from multiple clients and saving to a list
# Closing previous connections if any
def accepting_connections():

    global thread_run
    thread_run=True
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while thread_run:
        try:
            conn, address = s.accept()
            #s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)
            out_string=f"Connection established with {address} \n"

            if(len(all_address)==1):
                file1 = open("outputfile.txt", "w")  # append mode 
            else:
                file1 = open("outputfile.txt", "a")  # append mode
            
            file1.write(out_string) 
            file1.close()

            print(out_string,end="")  # Displaying IP and Port
            # print(str(all_connections))
            conn.send(str.encode(str(all_address)))

        except socket.error :
            continue


create_and_run_threads()
convert_list_to_thread_queue()







# delete_index = all_connections.index(conn, 0, len(all_connections))
# del all_address[delete_index]
# del all_connections[delete_index]
# conn.close()
