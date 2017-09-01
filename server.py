try:
    import socket,sys,time,os,logging
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    try:
        logging.stream=sys.stdout
        logging.basicConfig(filename='log'+time.strftime("%m%d%s")+'.log',level=logging.DEBUG,format='%(module)s %(levelname)s %(threadName)s %(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
    except ValueError as e:
        logging.info("Cannot Create log files: Program Exiting.\nError: ")
        Logger.exception(e)
        os._exit(0)
    finally:
        logging.info("Loggers set, imports completed")



class server():
    def __init__(self,host,port,packetsize,lm=1):
        logging.info("Initalizing Attributes")
        logging.info("Checking if host and port are avaible: ")        
        self.host=host
        self.port=port
        self.lm=lm
        self.packetsize=packetsize
        self.recvstuff=None
        #creating a socket with IP4 config and TCP stream protocol
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #to connect to a host and port and listen for connections
    def connect(self):
        nf=False
        try:
            logging.info("Binding the Socket to host and Port: ")
            self.sock.bind((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot Bind the socket to Host % and Port %: \n" %(self.host,self.port))
            logging.error(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            logging.info("The Server Socket is now being binded to host: %s and port: %d "%(self.host,self.port))
            #Socket listining to max 1 connection
            logging.info("Server socket is listing for 1 connections")
            self.sock.listen(1)
    def start(self):
        self.connect()
        i=0
        while i<self.lm:
            logging.info("Waiting for the connection: ")
            conn,addr=self.sock.accept()
            logging.info("Connection Recieved from connection %s and address %s"%(conn,addr))
            self.recvstuff=b""           
            data=conn.recv(self.packetsize)
            logging.info("Started Recieving Data: ")
            st=time.time()
            while data:                
                print("Data Recieved: "+str((sys.getsizeof(data)/1024**2)/time.time()-st)+" MBPS",end="\r")
                self.recvstuff+=data
                data=conn.recv(self.packetsize)
            et=time.time()
            print("Speed of data transfer is "+str((sys.getsizeof(self.recvstuff)/1024**2)/(et-st))+" MBPS")
            print("Closing Socket")
            conn.close()
            i+=1
if __name__=="__main__":
    serv=server(host='192.168.43.9',port=10001,lm=1,packetsize=65536)
    serv.start()