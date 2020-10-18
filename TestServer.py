import socket
# create an INET, STREAMing socket

# now connect to the web server on port 80 - the normal http port
#s.connect(("www.python.org", 80))
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(("localhost", 5550))
# become a server socket
serversocket.listen(5)
def client_thread(socket):

    print(socket.recv(1024).decode())
addr = ""
count = 0
while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    addr = address

    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    client_thread(clientsocket)
    # ct.run()
    count += 1
    if(count >= 30):
        print("MANUAL TRIGGER")
        count = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr[0],5554))
        s.send(b"TRIGGER_MANUAL")
        s.close()