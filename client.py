import socket,time,logging,os
from sendfile import sendfile
host='192.168.43.1'
port=8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("The Server Socket is now being binded to host: %s and port: %d "%(host,port))
sock.connect((host,port))
print("Opening large file: ")
infile=open("2.bytes",'rb')
print("Reading large file: ")
infile=infile.read()
print("Sending large file: ")
st=time.time()
sock.sendall(infile)
et=time.time()
print("Total time to send the required file: "+str(et-st))
print("Closing Socket")
sock.close()
