import Networking
from Networking import client
localhost='localhost'
port=10001
client_directory=r'/home/shivam/Work/Projects/test/client/'    
secret='shivam'
filenm='1.mp4'

clin=client(host=localhost,port=10001,filenm=filenm)
clin.begin(client_directory=client_directory)

clin.handshake(secret)