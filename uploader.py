import Networking
from Networking import client

localhost='localhost'
port=10002
client_directory=r'/home/shivam/Work/Projects/test/client/'    
secret='shivam'
filenm='1.mp4'

clin=client(host=localhost,port=port,filenm=filenm,secret=secret).begin(client_directory=client_directory)
