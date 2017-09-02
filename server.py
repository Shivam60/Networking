try:
    import socket,sys,time,os,logging
    from Networking import Network
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



class server(Network):
    def __init__(self,host,port,packetsize,path,filenm,lm=1):
        logging.info("Initalizing Attributes")
        logging.info("Checking if host and port are available: ")        
        self.host=host
        self.port=port
        self.lm=lm
        self.packetsize=packetsize
        self.recvstuff=None
        Network.__init__(self,path=path,file=filenm)
        #creating a socket with IP4 config and TCP stream protocol
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #to connect to a host and port and listen for connections
    def connect_client(self):
        nf=False
        try:
            logging.info("connecting the Socket to server on port: ")
            self.sock.connect((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot connect the socket to server %s on Port %s: \n" %(self.host,self.port))
            logging.error(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            logging.info("The Client Socket has been connected to server: %s on port: %d "%(self.host,self.port))
    def connect(self):
        nf=False
        try:
            logging.info("Binding the Socket to host and Port: ")
            self.sock.bind((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot Bind the socket to Host %s and Port %d \n" %(self.host,self.port))
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
    def handshake(self):
        logging.info("Connecting...")
        self.connect()
        logging.info("Connection recieved.")        
        conn,addr=self.sock.accept()    
        logging.info("Waiting for handshake reply.")  
        data=conn.recv(self.packetsize)
        logging.info("Handshake reply recieved.") 
        self.crc,self.file_no=self.find_crc_fno(data)
        logging.info("Sending handshake back") 
        conn.send((self.crc+'/\\'+str(self.file_no)+'/\\').encode('utf-8'))
        logging.info("Handshake back sent")
        self.sock.close()
if __name__=="__main__":
#    192.168.43.9
    serv=server(host='localhost',port=10001,lm=2,packetsize=65536,path=os.getcwd(),filenm='s.bytes')
    serv.handshake()
    serv.sock.close()
    #serv.start()
