import sys,socket
try:
   import _pickle as cPickle
except:
   print("Importing Pickle Failed, Make sure the Requirements are met. Program exiting")
   sys.exit(0)
finally:
    pass
class Network():
    def __init__(self,ip,port):
        self.port=port
        self.ip=ip
    def tobytes(self,stuff): #returns serialized item passed in as a parameter
        try:
            stuff=pickle.dumps(stuff)
        except e:
            print("Error in Serialisation of the Object. Object could not be converted to byetes. Make Sure the Datatype supports serialization.")
        finally:
            return stuff
    def frombytes(self,stuff): #returns deserialized item passed in as a parameter
        try:
            stuff=pickle.loads(stuff)
        except e:
            print("Error in Deserialisation of the Object. Object could not be converted to bytes. Make Sure the Datatype supports serialization.")
        finally:
            return stuff
class TCPserver(Network):
    def __init__(self,port,connection_limit=1):
        try:
            self.serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serversocket.bind((socket.gethostname(),port))
            self.serversocket.listen(connection_limit)
        except socket.error as err:
            print(err)
        finally:
            print("Server Socket Created at: "+str(connection_limit)+" Port number: "+port)
            print("Maximum Connections limit set to: "+ str(connection_limit))
    def run(self):
        while True:
            try:
                (conn, (ip,port))=self.serversocket.accept()
                newclient=ClientThread(ip)
            except socket.error as err:
                print(err)
            finally:
                pass
