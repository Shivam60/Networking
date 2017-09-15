import Networking
from Networking import server
localhost='localhost'
port=10001
sever_directory=r'/home/shivam/Work/Projects/test/server/'
secret='shivam'

serv=Networking.server(host=localhost,port=port,packetsize=65536,filenm='s.mp4',sever_directory=sever_directory)    
serv.handshake(secret)
serv.start()
serv.end()