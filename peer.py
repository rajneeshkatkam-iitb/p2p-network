import socket
import sys
import threading
import time
from queue import Queue


class Peer:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.message_list = {}

    def add_message(self, key_message, new_value):
        self.message_list[key_message] = new_value


class Seed:
    def __init__(self, ip, port):
        self.ip=ip
        self.port=port


# Socket Functionalities Below --------------------------

# Global Variables for socket
client_socket = socket.socket()
host = ''

if len(sys.argv) >1:
    port = int(sys.argv[1])
else:
    print("Please provide port number as argument")
    sys.exit()

# creating object of socket
def create_socket():
    try:
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.settimeout(5)
    except socket.error as msg:
        print("Socket creation error: "+str(msg))


# binding the socket
def bind_socket():
    try:
        print("Binding the port: "+str(port))
        server_socket.bind((host, port))
        server_socket.listen(5)

    except socket.error as msg:
        print("Socket Binding error: "+str(msg))
        time.sleep(5) # Time to sleep before reattempting the bind connection
        bind_socket()


# Handling connections from multiple clients and saving to a list
# Closing previous connections if any
def accepting_connections():

    global thread_run
    thread_run=True

    while thread_run:
        try:
            conn, address = server_socket.accept()
            #s.setblocking(1)  # prevents timeout

            # Read the response. If response MSG is "Request Connection"
            # check if len(final_peer_list)<4
            # If true then add connection to the final_peer_list array
            # and send reply MSG = "Connection Accepted"
            # If false then send reply MSG = "Connections Full"
            # and close the connection (discarded and not added to the final_peer_list) 


            out_string=f"Connection established with {address} \n"
            

            print(out_string,end="")  # Displaying IP and Port
            # print(str(all_connections))
            conn.send(str.encode(str("Hello Peer")))

        except socket.error :
            continue


def server_socket_listening_thread():
    create_socket()
    bind_socket()
    accepting_connections()

# Socket Functionalities End --------------------------


# Thread functionalities Below ------------------------

# Global Variables for Threads
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

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
        if x == 1:             #Thread 1 tasks
            server_socket_listening_thread()

        if x == 2:
            print("Thread 2")  #Thread 2 tasks

    queue.task_done()


create_and_run_threads()
convert_list_to_thread_queue()

# Thread functionalities End ----------------



finals_seed_list=[]

union_peer_obj_list=[]

final_peer_obj_list=[]

def connecting_to_seeds_and_union_list():
    print("Function: connecting_to_seeds_and_union_list")
    #Loop till (n/2)+1 finals_seed
        #client_socket.connect(host,port)
        #client_socket.send(bytes("New connection","utf-8"));
        #response = client_socket.recv() ---List is received from seed
        #parsing -- Decode the data..Extract the list of address and then append to the peer_union_list
        #loop in for each peer object received from seed
            #obj1= new peers()
            #obj.ip: 
            #obj.port:     
            #union_peer_obj_list.append(obj1)
        #client_socket.close()


connecting_to_seeds_and_union_list() #This is the first task to be executed. After this final_peer_obj_list is loaded with peer objects that are needed to be connected



def creating_final_peer_list():
    print("Function: creating_final_peer_list")
    #connect and send MSG="Request Connection"
    # wait for response
    # if it already has >= 4 peers connected to it
    # it will reject the connection ..i.e. it will send response MSG= "Connections Full"
    # If rejected, then randomly choose another IP from the union list and start from the above steps again
    # else it will accept the connection, add it to its final_peer_list array
    # and send response MSG = "Connection Accepted" 
    # If you recieve respose MSG = "Connection Accepted", then add its address to your final_peer_list array as well
    

print("Manually adding entering of final peer nodes")

peer_obj_1=Peer("192.168.0.192",'9999')
peer_obj_2=Peer("192.168.0.192",'9998')
peer_obj_3=Peer("192.168.0.192",'9997')
peer_obj_4=Peer("192.168.0.192",'9996')

final_peer_obj_list.append(peer_obj_1)
final_peer_obj_list.append(peer_obj_2)
final_peer_obj_list.append(peer_obj_3)
final_peer_obj_list.append(peer_obj_4)

print("Completed: Manually adding entering of final peer nodes")


creating_final_peer_list()

print("Completed Function: creating_final_peer_list")





# client_socket.connect((host, port))

# while True:
#     try:
#         data = client_socket.recv(1024)
#         if len(data) <= 0:
#             break
#         print(data.decode("utf-8"))

#     except socket.error as msg:
#         print("Server closed the connection..exiting")
#         sys.exit()

#     except KeyboardInterrupt:
#         client_socket.close()

