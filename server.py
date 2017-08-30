import socket,sys,time,os
lm=65536
host='localhost'
port=10001
#creating a socket with IP4 config and TCP stream protocol
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("The Server Socket is now being binded to host: %s and port: %d "%(host,port))
sock.bind((host,port))
#Socket listining to max 1 connection
sock.listen(1)
i=0
while i<1:
    print("Waiting for the connection: ")
    conn,addr=sock.accept()
    print("Connection Recieved from connection %s and address %s"%(conn,addr))
    a=b""
    print("Start Recieving Data: ")
    st=time.time()
    data=conn.recv(lm)
    while data:
#        print("Data Recieved: "+str(sys.getsizeof(data)/1024**2)+" bytes")
        a+=data
        data=conn.recv(lm)
    et=time.time()
    print("Speed of data transfer is "+str(sys.getsizeof(a)/1024**2/(et-st))+"MBPS")
#    print("Data Recieved of size: %s , type is %s and total time taken to recieve is: %d"%(sys.getsizeof(a),type(data),et-st))
    print("Closing Socket")
    conn.close()
    i+=1
