import Networking
from Networking import server


localhost='localhost'
port=10002
sever_directory=r'/home/shivam/Work/Projects/test/server/'
secret='shivam'
filenm='s.mp4'

serv=Networking.server(host=localhost,port=port,filenm=filenm,sever_directory=sever_directory).handshake(secret)

